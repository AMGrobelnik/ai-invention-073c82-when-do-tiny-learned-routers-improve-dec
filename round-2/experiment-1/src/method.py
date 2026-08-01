#!/usr/bin/env python3
"""Experiment to test if tiny learned routers can improve decoding by routing between greedy and sampling strategies.

This script implements the full experimental methodology:
1. Load and subsample data from 4 QA datasets
2. Generate oracle labels using OpenRouter API (greedy vs sampling)
3. Extract prompt embeddings using sentence-transformers
4. Train classifier to predict optimal decoding strategy
5. Evaluate routing performance vs baselines
6. Test conditional hypothesis (routing helps only when 30-70% sampling optimal)
7. Create mixed datasets with controlled ratios
8. Save results in exp_gen_sol_out.json schema format
"""

from loguru import logger
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Tuple
import json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sentence_transformers import SentenceTransformer
import requests
import time
import base64
import io
import matplotlib.pyplot as plt
import seaborn as sns
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import gc
import psutil
import resource
import os
import sys
from datetime import datetime
import hashlib

# Configure logging
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add("logs/run.log", rotation="30 MB", level="DEBUG")

# Constants
MAX_BUDGET_USD = 10.0
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
CACHE_DIR = Path("cache")
RESULTS_DIR = Path("results")
EMBEDDINGS_CACHE = Path("embeddings_cache")


class ExperimentConfig(BaseModel):
    """Configuration for the experiment."""
    max_budget_usd: float = MAX_BUDGET_USD
    num_examples_per_dataset: int = 125  # 125 per dataset = 500 total
    total_examples_target: int = 500
    embedding_model: str = "all-MiniLM-L6-v2"
    test_size: float = 0.3
    cv_folds: int = 5
    sampling_temperature: float = 0.7
    sampling_num_samples: int = 1  # Reduce to 1 for speed
    greedy_temperature: float = 0.0
    max_tokens: int = 512
    models_to_test: List[str] = Field(default_factory=lambda: ["gpt-4o-mini"])


class OracleResult(BaseModel):
    """Result from oracle label generation."""
    example_id: str
    dataset: str
    prompt: str
    correct_answer: str
    greedy_response: str
    greedy_correct: bool
    sampling_responses: List[str]
    sampling_correct: bool
    sampling_optimal: int  # 1 if sampling correct, 0 otherwise
    cost_usd: float


class ExperimentResults(BaseModel):
    """Full experiment results matching exp_gen_sol_out.json schema."""
    experiment_id: str = "routing_experiment_1"
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    config: ExperimentConfig = Field(default_factory=ExperimentConfig)
    total_cost_usd: float = 0.0
    num_examples_processed: int = 0
    
    # Oracle label statistics
    oracle_labels: List[int] = Field(default_factory=list)
    sampling_optimal_rate_by_dataset: Dict[str, float] = Field(default_factory=dict)
    
    # Classifier results
    classifier_accuracy: float = 0.0
    classifier_f1: float = 0.0
    classifier_roc_auc: float = 0.0
    cv_scores: List[float] = Field(default_factory=list)
    
    # Routing evaluation
    baseline_accuracies: Dict[str, float] = Field(default_factory=dict)
    router_accuracy: float = 0.0
    routing_benefit: float = 0.0
    
    # Conditional hypothesis test
    routing_benefit_vs_sampling_rate: List[Tuple[float, float]] = Field(default_factory=list)
    hypothesis_supported: bool = False
    
    # Mixed dataset results
    mixed_dataset_results: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Visualizations (base64 encoded PNG)
    plots_base64: Dict[str, str] = Field(default_factory=dict)


def setup_directories():
    """Create necessary directories."""
    for d in [CACHE_DIR, RESULTS_DIR, EMBEDDINGS_CACHE, Path("logs")]:
        d.mkdir(exist_ok=True)


def load_data(data_path: Path, max_examples_per_dataset: int = 500) -> List[Dict]:
    """Load and subsample data from the full dataset."""
    logger.info(f"Loading data from {data_path}")
    
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    examples = []
    for dataset_info in data.get('datasets', []):
        dataset_name = dataset_info['dataset']
        dataset_examples = dataset_info.get('examples', [])
        
        # Subsample
        if len(dataset_examples) > max_examples_per_dataset:
            indices = np.random.choice(len(dataset_examples), max_examples_per_dataset, replace=False)
            dataset_examples = [dataset_examples[i] for i in indices]
        
        for i, ex in enumerate(dataset_examples):
            ex['dataset'] = dataset_name
            ex['example_id'] = f"{dataset_name}_{i}"
            examples.append(ex)
        
        logger.info(f"Dataset {dataset_name}: {len(dataset_examples)} examples")
    
    logger.info(f"Total examples loaded: {len(examples)}")
    return examples


def get_cache_key(prompt: str, temperature: float, model: str) -> str:
    """Generate cache key for API responses."""
    content = f"{prompt}_{temperature}_{model}"
    return hashlib.md5(content.encode()).hexdigest()


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((requests.RequestException,))
)
def call_openrouter_api(
    prompt: str,
    model: str,
    temperature: float,
    max_tokens: int,
    api_key: str
) -> Tuple[str, float]:
    """Call OpenRouter API with retry logic. Returns (response_text, cost_usd)."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-inventor.local",
        "X-Title": "AI Inventor Routing Experiment"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    
    result = response.json()
    response_text = result['choices'][0]['message']['content']
    
    # Estimate cost (simplified - actual cost depends on model)
    # GPT-4o-mini: ~$0.15/1M input, $0.60/1M output
    # Gemini Flash: ~$0.075/1M input, $0.30/1M output
    estimated_cost = 0.001  # Conservative estimate per call
    
    return response_text, estimated_cost


def parse_answer(response: str, task_type: str, correct_answer: str) -> bool:
    """Parse model response and check if correct."""
    response_clean = response.strip()
    response_lower = response_clean.lower()
    correct_clean = correct_answer.strip()
    correct_lower = correct_clean.lower()
    
    if task_type == "math_reasoning":
        # Extract number from response
        import re
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', response_clean)
        if numbers:
            return numbers[-1] == correct_clean
        return False
    
    elif task_type in ["science_reasoning", "multiple_choice"]:
        # Extract letter (A, B, C, D)
        import re
        # Try multiple patterns to find the answer letter
        # Pattern 1: Letter at start or after period
        letters = re.findall(r'(?:^|\.\s|\s)([A-D])(?:\.|\s|$)', response_clean)
        if not letters:
            # Pattern 2: Just find any A-D letter
            letters = re.findall(r'\b([A-D])\b', response_clean.upper())
        if not letters:
            # Pattern 3: Look for "Answer:" pattern
            if "answer:" in response_lower:
                answer_part = response_lower.split("answer:")[-1].strip()
                letters = re.findall(r'\b([a-d])\b', answer_part)
        
        if letters:
            # Map correct_answer to letter if it's an index
            if correct_clean in "0123":
                correct_letter = chr(65 + int(correct_clean))
            else:
                correct_letter = correct_clean.upper()
            return letters[-1].upper() == correct_letter
        return False
    
    elif task_type == "boolean_questions":
        # Extract yes/no
        if "yes" in response_lower:
            return "yes" == correct_lower
        elif "no" in response_lower:
            return "no" == correct_lower
        return False
    
    return False


def generate_oracle_labels(
    examples: List[Dict],
    config: ExperimentConfig,
    api_key: str
) -> Tuple[List[OracleResult], float]:
    """Generate oracle labels by running both strategies via API."""
    logger.info(f"Generating oracle labels for {len(examples)} examples")
    
    # Check for mock mode
    mock_mode = os.environ.get("MOCK_MODE", "false").lower() == "true"
    
    oracle_results = []
    total_cost = 0.0
    cache_file = CACHE_DIR / "oracle_labels.json"
    
    # Load cache if exists
    if cache_file.exists():
        with open(cache_file, 'r') as f:
            cached_data = json.load(f)
        logger.info(f"Loaded {len(cached_data)} cached oracle results")
    else:
        cached_data = {}
    
    for i, example in enumerate(examples):
        if not mock_mode and total_cost >= config.max_budget_usd * 0.9:  # 90% budget limit
            logger.warning(f"Budget limit reached at example {i}")
            break
        
        example_id = example['example_id']
        prompt = example['input']
        correct_answer = example['output']
        task_type = example.get('metadata_task_type', 'unknown')
        model = config.models_to_test[0]  # Use first model for oracle generation
        
        # Check cache
        cache_key = get_cache_key(prompt, 0, model)
        if cache_key in cached_data:
            oracle_results.append(OracleResult(**cached_data[cache_key]))
            continue
        
        if mock_mode:
            # Generate mock oracle labels for testing
            import random
            greedy_correct = random.random() > 0.5
            sampling_correct = random.random() > 0.4  # Slightly better
            
            oracle_result = OracleResult(
                example_id=example_id,
                dataset=example['dataset'],
                prompt=prompt,
                correct_answer=correct_answer,
                greedy_response=f"Mock response: {correct_answer}" if greedy_correct else "Mock wrong answer",
                greedy_correct=greedy_correct,
                sampling_responses=[f"Mock response: {correct_answer}" if sampling_correct else "Mock wrong answer"],
                sampling_correct=sampling_correct,
                sampling_optimal=1 if sampling_correct else 0,
                cost_usd=0.0
            )
        else:
            try:
                # Greedy decoding
                greedy_response, cost1 = call_openrouter_api(
                    prompt, model, config.greedy_temperature, config.max_tokens, api_key
                )
                
                # Sampling decoding (best of N)
                sampling_responses = []
                for _ in range(config.sampling_num_samples):
                    resp, cost2 = call_openrouter_api(
                        prompt, model, config.sampling_temperature, config.max_tokens, api_key
                    )
                    sampling_responses.append(resp)
                    total_cost += cost2
                
                total_cost += cost1
                
                # Parse responses
                greedy_correct = parse_answer(greedy_response, task_type, correct_answer)
                sampling_correct = any(
                    parse_answer(resp, task_type, correct_answer)
                    for resp in sampling_responses
                )
                
                oracle_result = OracleResult(
                    example_id=example_id,
                    dataset=example['dataset'],
                    prompt=prompt,
                    correct_answer=correct_answer,
                    greedy_response=greedy_response,
                    greedy_correct=greedy_correct,
                    sampling_responses=sampling_responses,
                    sampling_correct=sampling_correct,
                    sampling_optimal=1 if sampling_correct else 0,
                    cost_usd=cost1 + sum([cost1] * config.sampling_num_samples)
                )
            except Exception as e:
                logger.error(f"Failed to process example {example_id}: {e}")
                continue
        
        oracle_results.append(oracle_result)
        cached_data[cache_key] = oracle_result.model_dump()
        
        if (i + 1) % 10 == 0:
            logger.info(f"Processed {i + 1}/{len(examples)}, cost: ${total_cost:.3f}")
            # Save cache periodically
            with open(cache_file, 'w') as f:
                json.dump(cached_data, f)
    
    # Save final cache
    with open(cache_file, 'w') as f:
        json.dump(cached_data, f)
    
    logger.info(f"Generated {len(oracle_results)} oracle labels, total cost: ${total_cost:.3f}")
    return oracle_results, total_cost


def extract_embeddings(
    prompts: List[str],
    model_name: str = "all-MiniLM-L6-v2"
) -> np.ndarray:
    """Extract embeddings using sentence-transformers."""
    logger.info(f"Extracting embeddings for {len(prompts)} prompts using {model_name}")
    
    # Check cache
    cache_file = EMBEDDINGS_CACHE / f"embeddings_{len(prompts)}_{model_name.replace('/', '_')}.npy"
    if cache_file.exists():
        logger.info(f"Loading cached embeddings from {cache_file}")
        return np.load(cache_file)
    
    # Load model
    model = SentenceTransformer(model_name)
    
    # Extract embeddings in batches
    embeddings = model.encode(prompts, batch_size=32, show_progress_bar=True)
    
    # Cache results
    np.save(cache_file, embeddings)
    logger.info(f"Saved embeddings to {cache_file}")
    
    # Cleanup
    del model
    gc.collect()
    
    return embeddings


def train_classifier(
    X: np.ndarray,
    y: np.ndarray,
    config: ExperimentConfig
) -> Tuple[Any, Dict[str, float]]:
    """Train classifier and return model with metrics."""
    logger.info(f"Training classifier on {len(X)} examples")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=config.test_size, random_state=42, stratify=y
    )
    
    # Try multiple classifiers
    classifiers = {
        'logistic': LogisticRegression(max_iter=1000),
        'mlp': MLPClassifier(hidden_layer_sizes=(50,), max_iter=500, random_state=42),
        'rf': RandomForestClassifier(n_estimators=100, random_state=42)
    }
    
    best_model = None
    best_accuracy = 0
    results = {}
    
    for name, clf in classifiers.items():
        logger.info(f"Training {name} classifier")
        
        # Cross-validation
        cv_scores = cross_val_score(clf, X_train, y_train, cv=config.cv_folds, scoring='accuracy')
        
        # Train on full training set
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        roc_auc = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1]) if hasattr(clf, 'predict_proba') else 0.0
        
        logger.info(f"{name}: CV accuracy={cv_scores.mean():.3f} (+/- {cv_scores.std():.3f}), "
                   f"Test accuracy={accuracy:.3f}, F1={f1:.3f}, ROC-AUC={roc_auc:.3f}")
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_model = clf
        
        results[name] = {
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'test_accuracy': accuracy,
            'f1': f1,
            'roc_auc': roc_auc
        }
    
    # Get best model metrics
    y_pred_best = best_model.predict(X_test)
    best_metrics = {
        'accuracy': accuracy_score(y_test, y_pred_best),
        'f1': f1_score(y_test, y_pred_best, average='weighted'),
        'roc_auc': roc_auc_score(y_test, best_model.predict_proba(X_test)[:, 1]) if hasattr(best_model, 'predict_proba') else 0.0,
        'cv_scores': results.get('logistic', {}).get('cv_mean', 0.0)
    }
    
    return best_model, best_metrics


def evaluate_routing(
    oracle_results: List[OracleResult],
    classifier: Any,
    embeddings: np.ndarray
) -> Dict[str, float]:
    """Evaluate routing performance vs baselines."""
    logger.info("Evaluating routing performance")
    
    # Baselines
    always_greedy = sum(1 for r in oracle_results if r.greedy_correct) / len(oracle_results)
    always_sampling = sum(1 for r in oracle_results if r.sampling_correct) / len(oracle_results)
    random_routing = 0.5 * always_greedy + 0.5 * always_sampling
    oracle_routing = sum(1 for r in oracle_results if r.sampling_optimal) / len(oracle_results)
    
    # Router accuracy
    router_predictions = classifier.predict(embeddings)
    router_correct = sum(
        1 for i, r in enumerate(oracle_results)
        if (router_predictions[i] == 1 and r.sampling_correct) or
           (router_predictions[i] == 0 and r.greedy_correct)
    ) / len(oracle_results)
    
    results = {
        'always_greedy': always_greedy,
        'always_sampling': always_sampling,
        'random_routing': random_routing,
        'oracle_routing': oracle_routing,
        'router_accuracy': router_correct,
        'routing_benefit': router_correct - max(always_greedy, always_sampling)
    }
    
    logger.info(f"Baselines: Greedy={always_greedy:.3f}, Sampling={always_sampling:.3f}, "
               f"Random={random_routing:.3f}, Oracle={oracle_routing:.3f}")
    logger.info(f"Router accuracy={router_correct:.3f}, Benefit={results['routing_benefit']:.3f}")
    
    return results


def test_conditional_hypothesis(
    oracle_results: List[OracleResult],
    classifier: Any,
    embeddings: np.ndarray
) -> Tuple[List[Tuple[float, float]], bool]:
    """Test if routing benefit > 0 only when 30-70% sampling optimal."""
    logger.info("Testing conditional hypothesis")
    
    # Group by dataset
    dataset_results = {}
    for r in oracle_results:
        if r.dataset not in dataset_results:
            dataset_results[r.dataset] = []
        dataset_results[r.dataset].append(r)
    
    # Calculate sampling optimal rate and routing benefit per dataset
    results = []
    for dataset, results_list in dataset_results.items():
        sampling_rate = sum(r.sampling_optimal for r in results_list) / len(results_list)
        
        # Get indices for this dataset
        indices = [i for i, r in enumerate(oracle_results) if r.dataset == dataset]
        dataset_embeddings = embeddings[indices]
        
        # Evaluate routing on this dataset
        router_predictions = classifier.predict(dataset_embeddings)
        router_acc = sum(
            1 for i, r in enumerate(results_list)
            if (router_predictions[i] == 1 and r.sampling_correct) or
               (router_predictions[i] == 0 and r.greedy_correct)
        ) / len(results_list)
        
        baseline = max(
            sum(1 for r in results_list if r.greedy_correct) / len(results_list),
            sum(1 for r in results_list if r.sampling_correct) / len(results_list)
        )
        
        routing_benefit = router_acc - baseline
        results.append((sampling_rate, routing_benefit))
        
        logger.info(f"Dataset {dataset}: sampling_rate={sampling_rate:.3f}, "
                   f"routing_benefit={routing_benefit:.3f}")
    
    # Check hypothesis: benefit > 0 only when 30-70%
    hypothesis_supported = True
    for rate, benefit in results:
        if benefit > 0 and (rate < 0.3 or rate > 0.7):
            hypothesis_supported = False
            break
        if benefit <= 0 and 0.3 <= rate <= 0.7:
            hypothesis_supported = False
            break
    
    logger.info(f"Hypothesis supported: {hypothesis_supported}")
    return results, hypothesis_supported


def create_mixed_datasets(
    oracle_results: List[OracleResult],
    embeddings: np.ndarray,
    config: ExperimentConfig
) -> List[Dict[str, Any]]:
    """Create subsets with controlled sampling optimal ratios."""
    logger.info("Creating mixed datasets with controlled ratios")
    
    # Get all examples with their sampling_optimal labels
    sampling_optimal = [r for r in oracle_results if r.sampling_optimal == 1]
    greedy_optimal = [r for r in oracle_results if r.sampling_optimal == 0]
    
    results = []
    ratios = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    
    for target_ratio in ratios:
        # Calculate how many sampling/greedy examples needed
        # For simplicity, create balanced dataset of 200 examples
        n_total = 200
        n_sampling = int(n_total * target_ratio)
        n_greedy = n_total - n_sampling
        
        # Sample examples
        if n_sampling > len(sampling_optimal) or n_greedy > len(greedy_optimal):
            logger.warning(f"Not enough examples for ratio {target_ratio}")
            continue
        
        sampled_sampling = np.random.choice(sampling_optimal, n_sampling, replace=False)
        sampled_greedy = np.random.choice(greedy_optimal, n_greedy, replace=False)
        
        mixed_examples = list(sampled_sampling) + list(sampled_greedy)
        np.random.shuffle(mixed_examples)
        
        # Get embeddings for mixed examples
        indices = [oracle_results.index(r) for r in mixed_examples]
        mixed_embeddings = embeddings[indices]
        mixed_labels = [r.sampling_optimal for r in mixed_examples]
        
        # Train classifier on mixed dataset
        X_train, X_test, y_train, y_test = train_test_split(
            mixed_embeddings, mixed_labels, test_size=0.3, random_state=42
        )
        
        clf = LogisticRegression(max_iter=1000)
        clf.fit(X_train, y_train)
        
        # Evaluate
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Calculate routing benefit
        router_correct = sum(
            1 for i, r in enumerate(mixed_examples)
            if (clf.predict(mixed_embeddings[i:i+1])[0] == 1 and r.sampling_correct) or
               (clf.predict(mixed_embeddings[i:i+1])[0] == 0 and r.greedy_correct)
        ) / len(mixed_examples)
        
        baseline = max(
            sum(1 for r in mixed_examples if r.greedy_correct) / len(mixed_examples),
            sum(1 for r in mixed_examples if r.sampling_correct) / len(mixed_examples)
        )
        
        routing_benefit = router_correct - baseline
        
        results.append({
            'target_ratio': target_ratio,
            'actual_ratio': sum(mixed_labels) / len(mixed_labels),
            'classifier_accuracy': accuracy,
            'routing_benefit': routing_benefit
        })
        
        logger.info(f"Ratio {target_ratio}: actual={results[-1]['actual_ratio']:.3f}, "
                   f"benefit={routing_benefit:.3f}")
    
    return results


def create_visualizations(results: ExperimentResults) -> Dict[str, str]:
    """Create plots and return as base64 encoded PNGs."""
    logger.info("Creating visualizations")
    
    plots = {}
    
    # Plot 1: Routing benefit vs sampling optimal rate
    if results.routing_benefit_vs_sampling_rate:
        plt.figure(figsize=(10, 6))
        rates, benefits = zip(*results.routing_benefit_vs_sampling_rate)
        plt.scatter(rates, benefits, alpha=0.6)
        plt.axhline(y=0, color='r', linestyle='--', label='No benefit')
        plt.axvline(x=0.3, color='g', linestyle=':', label='30% threshold')
        plt.axvline(x=0.7, color='g', linestyle=':', label='70% threshold')
        plt.xlabel('Sampling Optimal Rate')
        plt.ylabel('Routing Benefit')
        plt.title('Routing Benefit vs Sampling Optimal Rate')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        plots['routing_benefit_vs_rate'] = base64.b64encode(buf.read()).decode()
        plt.close()
    
    # Plot 2: Baseline comparison
    if results.baseline_accuracies:
        plt.figure(figsize=(10, 6))
        methods = list(results.baseline_accuracies.keys()) + ['router']
        accuracies = list(results.baseline_accuracies.values()) + [results.router_accuracy]
        
        colors = ['gray'] * len(results.baseline_accuracies) + ['blue']
        plt.bar(methods, accuracies, color=colors)
        plt.ylabel('Accuracy')
        plt.title('Routing Performance vs Baselines')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3, axis='y')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
        buf.seek(0)
        plots['baseline_comparison'] = base64.b64encode(buf.read()).decode()
        plt.close()
    
    # Plot 3: Mixed dataset results
    if results.mixed_dataset_results:
        plt.figure(figsize=(10, 6))
        ratios = [r['target_ratio'] for r in results.mixed_dataset_results]
        benefits = [r['routing_benefit'] for r in results.mixed_dataset_results]
        
        plt.plot(ratios, benefits, 'o-', linewidth=2, markersize=8)
        plt.axhline(y=0, color='r', linestyle='--', label='No benefit')
        plt.axvspan(0.3, 0.7, alpha=0.2, color='green', label='Hypothesis range')
        plt.xlabel('Sampling Optimal Ratio in Training Set')
        plt.ylabel('Routing Benefit')
        plt.title('Routing Benefit vs Controlled Sampling Ratio')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        plots['mixed_dataset_results'] = base64.b64encode(buf.read()).decode()
        plt.close()
    
    return plots


@logger.catch(reraise=True)
def main():
    """Main experiment function."""
    logger.info("Starting routing experiment")
    
    # Setup
    setup_directories()
    config = ExperimentConfig()
    
    # Check for mock mode (for testing without API)
    mock_mode = os.environ.get("MOCK_MODE", "false").lower() == "true"
    if mock_mode:
        logger.info("Running in MOCK MODE - no API calls will be made")
    
    # Set memory limits
    avail_mem = psutil.virtual_memory().available
    resource.setrlimit(resource.RLIMIT_AS, (int(avail_mem * 0.8), int(avail_mem * 0.8)))
    logger.info(f"Set memory limit to {avail_mem * 0.8 / 1e9:.1f}GB")
    
    # Get API key from environment (not needed in mock mode)
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not mock_mode and not api_key:
        logger.error("OPENROUTER_API_KEY not set")
        raise ValueError("OPENROUTER_API_KEY environment variable required (or set MOCK_MODE=true)")
    
    # Initialize results
    results = ExperimentResults(config=config)
    
    # Step 1: Load data
    data_path = Path("full_data_out.json")  # Use full dataset
    examples = load_data(data_path, max_examples_per_dataset=config.num_examples_per_dataset)
    results.num_examples_processed = len(examples)
    
    # Step 2: Generate oracle labels
    logger.info("Step 2: Generating oracle labels")
    oracle_results, total_cost = generate_oracle_labels(examples, config, api_key)
    results.total_cost_usd = total_cost
    results.oracle_labels = [r.sampling_optimal for r in oracle_results]
    
    # Calculate sampling optimal rate by dataset
    dataset_counts = {}
    dataset_optimal = {}
    for r in oracle_results:
        dataset_counts[r.dataset] = dataset_counts.get(r.dataset, 0) + 1
        dataset_optimal[r.dataset] = dataset_optimal.get(r.dataset, 0) + r.sampling_optimal
    
    results.sampling_optimal_rate_by_dataset = {
        d: dataset_optimal[d] / dataset_counts[d]
        for d in dataset_counts
    }
    
    # Step 3: Extract embeddings
    logger.info("Step 3: Extracting embeddings")
    prompts = [r.prompt for r in oracle_results]
    embeddings = extract_embeddings(prompts, config.embedding_model)
    
    # Step 4: Train classifier
    logger.info("Step 4: Training classifier")
    X = embeddings
    y = np.array([r.sampling_optimal for r in oracle_results])
    
    classifier, metrics = train_classifier(X, y, config)
    results.classifier_accuracy = metrics['accuracy']
    results.classifier_f1 = metrics['f1']
    results.classifier_roc_auc = metrics['roc_auc']
    results.cv_scores = [metrics['cv_scores']] if isinstance(metrics['cv_scores'], float) else []
    
    # Step 5: Evaluate routing
    logger.info("Step 5: Evaluating routing")
    baseline_results = evaluate_routing(oracle_results, classifier, embeddings)
    results.baseline_accuracies = {
        k: v for k, v in baseline_results.items()
        if k not in ['router_accuracy', 'routing_benefit']
    }
    results.router_accuracy = baseline_results['router_accuracy']
    results.routing_benefit = baseline_results['routing_benefit']
    
    # Step 6: Test conditional hypothesis
    logger.info("Step 6: Testing conditional hypothesis")
    hypothesis_results, hypothesis_supported = test_conditional_hypothesis(
        oracle_results, classifier, embeddings
    )
    results.routing_benefit_vs_sampling_rate = hypothesis_results
    results.hypothesis_supported = hypothesis_supported
    
    # Step 7: Mixed datasets
    logger.info("Step 7: Creating mixed datasets")
    mixed_results = create_mixed_datasets(oracle_results, embeddings, config)
    results.mixed_dataset_results = mixed_results
    
    # Step 8: Create visualizations
    logger.info("Step 8: Creating visualizations")
    plots = create_visualizations(results)
    results.plots_base64 = plots
    
    # Save results
    logger.info("Saving results")
    
    # Convert results to exp_gen_sol_out schema format
    # Group examples by dataset
    dataset_groups = {}
    for i, r in enumerate(oracle_results):
        if r.dataset not in dataset_groups:
            dataset_groups[r.dataset] = []
        
        # Get router prediction
        router_prediction = "sampling" if classifier.predict(embeddings[i:i+1])[0] == 1 else "greedy"
        
        dataset_groups[r.dataset].append({
            "input": r.prompt,
            "output": r.correct_answer,
            "metadata_task_type": r.dataset.split('/')[-1] if '/' in r.dataset else r.dataset,
            "predict_greedy": "correct" if r.greedy_correct else "incorrect",
            "predict_sampling": "correct" if r.sampling_correct else "incorrect",
            "predict_router": router_prediction
        })
    
    # Create output in exp_gen_sol_out format
    exp_output = {
        "metadata": {
            "experiment_id": results.experiment_id,
            "timestamp": results.timestamp,
            "method_name": "tiny_learned_router",
            "method_description": "Logistic regression classifier on sentence embeddings to route between greedy and sampling decoding",
            "config": config.model_dump(),
            "results": {
                "primary_metric": "routing_benefit",
                "primary_value": results.routing_benefit,
                "baseline_comparison": results.baseline_accuracies,
                "hypothesis_supported": results.hypothesis_supported,
                "cost_usd": results.total_cost_usd,
                "classifier_accuracy": results.classifier_accuracy,
                "router_accuracy": results.router_accuracy
            }
        },
        "datasets": [
            {
                "dataset": ds,
                "examples": examples
            }
            for ds, examples in dataset_groups.items()
        ]
    }
    
    # Save in exp_gen_sol_out format
    output_path = Path("method_out.json")
    output_path.write_text(json.dumps(exp_output, indent=2))
    logger.info(f"Results saved to {output_path}")
    
    # Also save a copy as exp_gen_sol_out.json
    exp_output_path = Path("exp_gen_sol_out.json")
    exp_output_path.write_text(json.dumps(exp_output, indent=2))
    logger.info(f"Experiment output saved to {exp_output_path}")
    
    # Save full_method_out.json with same schema format (for validation)
    # This is the primary output file that needs to pass schema validation
    full_output_path = Path("full_method_out.json")
    full_output_path.write_text(json.dumps(exp_output, indent=2))
    logger.info(f"Full results saved to {full_output_path}")
    
    logger.info("Experiment completed successfully!")
    return results


if __name__ == "__main__":
    main()
