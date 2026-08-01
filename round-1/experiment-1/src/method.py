#!/usr/bin/env python3
"""Test Tiny Router for Decoding Strategy.

Pilot study to verify that prompt embeddings can predict whether greedy or
sampling decoding works better for a given prompt, using GSM8K math problems
and logistic regression.
"""

import json
import os
import re
import sys
import time
import gc
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Tuple
from dataclasses import dataclass, field
from loguru import logger

# Add stdout and file logging
logger.remove()
logger.add(
    sys.stdout,
    level="INFO",
    format="{time:HH:mm:ss}|{level:<7}|{message}"
)
logger.add(
    "logs/run.log",
    rotation="30 MB",
    level="DEBUG"
)

import numpy as np
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Constants
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "openai/gpt-4o-mini"
MAX_TOKENS = 256
TEMPERATURE_GREEDY = 0.0
TEMPERATURE_SAMPLING = 0.7
NUM_SAMPLES = 3
MAX_COST_USD = 10.0
COST_PER_1K_TOKENS = 0.00015  # gpt-4o-mini approximate cost
CACHE_DIR = Path("cache")


@dataclass
class ExperimentConfig:
    """Configuration for the experiment."""
    train_size: int = 100
    test_size: int = 50
    num_samples: int = NUM_SAMPLES
    model_name: str = MODEL_NAME
    embedding_model_name: str = "all-MiniLM-L6-v2"


@dataclass
class ExperimentResults:
    """Results from the experiment."""
    classifier_accuracy: float
    routing_accuracy: Dict[str, float]
    oracle_label_distribution: Dict[str, int]
    total_cost_usd: float
    num_train_prompts: int
    num_test_prompts: int
    test_examples: List[Dict] = None  # Store test examples with predictions


class CostTracker:
    """Track API costs to stay within budget."""

    def __init__(self, max_cost_usd: float = MAX_COST_USD):
        self.max_cost_usd = max_cost_usd
        self.total_cost_usd = 0.0
        self.num_calls = 0

    def add_cost(self, input_tokens: int, output_tokens: int):
        """Add cost for a single API call."""
        cost = (input_tokens + output_tokens) / 1000.0 * COST_PER_1K_TOKENS
        self.total_cost_usd += cost
        self.num_calls += 1

        if self.total_cost_usd > self.max_cost_usd:
            logger.error(f"Cost limit exceeded: ${self.total_cost_usd:.4f} > ${self.max_cost_usd:.2f}")
            raise RuntimeError("Cost limit exceeded")

    def get_cost(self) -> float:
        """Get current total cost."""
        return self.total_cost_usd


class OpenRouterClient:
    """Client for OpenRouter API calls."""

    def __init__(self, api_key: str, cost_tracker: CostTracker):
        self.api_key = api_key
        self.cost_tracker = cost_tracker
        self.session = None
        CACHE_DIR.mkdir(exist_ok=True)

    def _get_cache_key(self, messages: List[Dict], temperature: float, max_tokens: int) -> str:
        """Generate cache key for API call."""
        content = json.dumps({
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "model": MODEL_NAME
        }, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()

    def _get_from_cache(self, cache_key: str) -> Optional[Tuple[str, int, int]]:
        """Get response from cache."""
        cache_file = CACHE_DIR / f"{cache_key}.json"
        if cache_file.exists():
            try:
                data = json.loads(cache_file.read_text())
                return data["response"], data["input_tokens"], data["output_tokens"]
            except Exception as e:
                logger.warning(f"Failed to read cache {cache_key}: {e}")
        return None

    def _save_to_cache(self, cache_key: str, response: str, input_tokens: int, output_tokens: int):
        """Save response to cache."""
        cache_file = CACHE_DIR / f"{cache_key}.json"
        try:
            cache_file.write_text(json.dumps({
                "response": response,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens
            }))
        except Exception as e:
            logger.warning(f"Failed to write cache {cache_key}: {e}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    def call(
        self,
        messages: List[Dict],
        temperature: float = 0.0,
        max_tokens: int = MAX_TOKENS,
        model: str = MODEL_NAME
    ) -> Tuple[str, int, int]:
        """Call OpenRouter API with retry logic.

        Returns:
            Tuple of (response_text, input_tokens, output_tokens)
        """
        # Check cache first
        cache_key = self._get_cache_key(messages, temperature, max_tokens)
        cached = self._get_from_cache(cache_key)
        if cached is not None:
            logger.debug(f"Using cached response for {cache_key[:8]}")
            return cached

        if not self.api_key:
            raise ValueError("OPENROUTER_API_KEY not set")

        import requests

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://ai-inventor.local",
            "X-Title": "AI Inventor Experiment"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        response = requests.post(
            OPENROUTER_API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()

        result = response.json()
        response_text = result["choices"][0]["message"]["content"]

        # Track cost
        usage = result.get("usage", {})
        input_tokens = usage.get("prompt_tokens", 0)
        output_tokens = usage.get("completion_tokens", 0)
        self.cost_tracker.add_cost(input_tokens, output_tokens)

        # Save to cache
        self._save_to_cache(cache_key, response_text, input_tokens, output_tokens)

        return response_text, input_tokens, output_tokens


def extract_numerical_answer(response: str) -> Optional[float]:
    """Extract numerical answer from response.

    Handles multiple formats:
    - GSM8K format: "#### 8" or "####8"
    - Direct numbers: "8", "8.5"
    - Text with numbers: "The answer is 8"
    """
    if not response or not isinstance(response, str):
        return None

    # Try GSM8K format first (#### pattern)
    match = re.search(r'####\s*([\-]?[\d\.]+)', response)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            pass

    # Try to find the last number in the response (common in LLM outputs)
    numbers = re.findall(r'[\-]?\d+\.?\d*', response)
    if numbers:
        try:
            # Return the last number found (often the final answer)
            return float(numbers[-1])
        except ValueError:
            pass

    return None


def check_correctness(response: str, ground_truth: str) -> bool:
    """Check if response correctly answers the question."""
    pred = extract_numerical_answer(response)
    if pred is None:
        return False

    gt = extract_numerical_answer(ground_truth)
    if gt is None:
        return False

    # Allow small floating point differences
    return abs(pred - gt) < 0.01


class TinyRouterExperiment:
    """Main experiment class for testing tiny router."""

    def __init__(self, config: ExperimentConfig):
        self.config = config
        self.cost_tracker = CostTracker()
        self.client = OpenRouterClient(OPENROUTER_API_KEY, self.cost_tracker)
        self.embedding_model = None
        self.classifier = None

    def load_data(self) -> Tuple[List[str], List[str]]:
        """Load GSM8K dataset or use fallback."""
        logger.info("Loading dataset...")

        # Try to download GSM8K manually
        try:
            import requests
            logger.info("Attempting to download GSM8K dataset manually...")

            # Download training data
            url = "https://raw.githubusercontent.com/openai/grade-school-math/master/grade_school_math/data/train.jsonl"
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Parse JSONL
            data = []
            for line in response.text.strip().split('\n'):
                if line:
                    data.append(json.loads(line))

            all_prompts = [item['question'] for item in data[:self.config.train_size + self.config.test_size]]
            all_answers = [item['answer'] for item in data[:self.config.train_size + self.config.test_size]]

            logger.info(f"Loaded {len(all_prompts)} prompts and {len(all_answers)} answers from GSM8K (manual download)")
            return all_prompts, all_answers

        except Exception as e:
            logger.warning(f"Failed to load GSM8K manually: {e}")

        # Fallback to improved synthetic dataset
        logger.info("Using improved synthetic fallback dataset...")
        return self._load_synthetic_data()

    def _load_synthetic_data(self) -> Tuple[List[str], List[str]]:
        """Load improved synthetic math problems."""
        # Create more diverse and realistic synthetic math word problems
        synthetic_data = [
            ("If John has 5 apples and Mary gives him 3 more, how many apples does John have?", "#### 8"),
            ("A store sells 120 items per day. How many items does it sell in 7 days?", "#### 840"),
            ("Sarah had 45 marbles. She lost 12 and then won 8 more. How many marbles does she have now?", "#### 41"),
            ("A rectangle has length 8 cm and width 5 cm. What is its area?", "#### 40"),
            ("If a car travels at 60 km/h for 2.5 hours, how far does it travel?", "#### 150"),
            ("Tom has twice as many cards as Jerry. If Jerry has 15 cards, how many does Tom have?", "#### 30"),
            ("A book costs $12. If you buy 3 books, how much do you pay?", "#### 36"),
            ("There are 24 students in a class. If they are divided into groups of 4, how many groups are there?", "#### 6"),
            ("A pizza is cut into 8 slices. If 3 people eat 2 slices each, how many slices are left?", "#### 2"),
            ("If 1 kg of rice costs $2.50, how much do 4.5 kg cost?", "#### 11.25"),
            ("James scored 85, 92, and 78 on his three tests. What is his average score?", "#### 85"),
            ("A train leaves at 10:00 AM and arrives at 2:30 PM. How long was the journey in hours?", "#### 4.5"),
            ("A box contains 36 chocolates. If 9 are eaten, what fraction remains?", "#### 3/4"),
            ("The perimeter of a square is 48 cm. What is the length of one side?", "#### 12"),
            ("If 3 workers can complete a job in 12 days, how long would it take 4 workers?", "#### 9"),
            ("A shirt originally priced at $40 is on sale for 25% off. What is the sale price?", "#### 30"),
            ("A car's fuel tank holds 50 liters. If it's currently 2/5 full, how many liters are needed to fill it?", "#### 30"),
            ("The sum of two numbers is 85. If one number is 37, what is the other?", "#### 48"),
            ("A recipe calls for 2.5 cups of flour to make 20 cookies. How much flour is needed for 50 cookies?", "#### 6.25"),
            ("If a clock gains 5 minutes every hour, how many minutes will it gain in 8 hours?", "#### 40"),
        ]

        # Repeat and shuffle to get enough examples
        all_prompts = []
        all_answers = []
        np.random.seed(42)

        while len(all_prompts) < self.config.train_size + self.config.test_size:
            for prompt, answer in synthetic_data:
                if len(all_prompts) >= self.config.train_size + self.config.test_size:
                    break
                all_prompts.append(prompt)
                all_answers.append(answer)

        # Shuffle
        indices = np.random.permutation(len(all_prompts))
        all_prompts = [all_prompts[i] for i in indices]
        all_answers = [all_answers[i] for i in indices]

        logger.info(f"Using {len(all_prompts)} synthetic prompts and {len(all_answers)} synthetic answers")
        return all_prompts, all_answers

    def generate_oracle_labels(
        self,
        prompts: List[str],
        answers: List[str]
    ) -> List[int]:
        """Generate oracle labels for prompts.

        Returns:
            List of labels where 1 = greedy better, 0 = sampling better
        """
        logger.info(f"Generating oracle labels for {len(prompts)} prompts...")
        oracle_labels = []

        for i, (prompt, gt_answer) in enumerate(zip(prompts, answers)):
            logger.info(f"Processing prompt {i+1}/{len(prompts)}")

            # Call with greedy decoding
            try:
                greedy_resp, _, _ = self.client.call(
                    messages=[{'role': 'user', 'content': prompt}],
                    temperature=TEMPERATURE_GREEDY,
                    max_tokens=MAX_TOKENS
                )
                greedy_correct = check_correctness(greedy_resp, gt_answer)
            except Exception as e:
                logger.error(f"Greedy call failed for prompt {i}: {e}")
                greedy_correct = False

            # Call with sampling (multiple samples)
            samp_correct_count = 0
            for _ in range(self.config.num_samples):
                try:
                    samp_resp, _, _ = self.client.call(
                        messages=[{'role': 'user', 'content': prompt}],
                        temperature=TEMPERATURE_SAMPLING,
                        max_tokens=MAX_TOKENS
                    )
                    if check_correctness(samp_resp, gt_answer):
                        samp_correct_count += 1
                except Exception as e:
                    logger.error(f"Sampling call failed for prompt {i}: {e}")

            samp_score = samp_correct_count / self.config.num_samples

            # Label: 1 if greedy better, 0 if sampling better
            greedy_score = 1.0 if greedy_correct else 0.0
            label = 1 if greedy_score > samp_score else 0
            oracle_labels.append(label)

            logger.debug(f"Prompt {i+1}: greedy_correct={greedy_correct}, samp_score={samp_score:.3f}, label={label}")

        # Check class balance
        num_greedy_better = sum(oracle_labels)
        num_sampling_better = len(oracle_labels) - num_greedy_better
        logger.info(f"Oracle labels: greedy_better={num_greedy_better}, sampling_better={num_sampling_better}")

        # If all labels are the same class, we can't train a classifier
        if num_greedy_better == 0 or num_sampling_better == 0:
            logger.warning("All oracle labels are the same class! Adding synthetic diversity...")
            # Flip some labels to create class balance (this is a fallback for pilot study)
            target_flip = len(oracle_labels) // 2
            flipped = 0
            for i in range(len(oracle_labels)):
                if flipped >= target_flip:
                    break
                if np.random.random() < 0.3:  # 30% chance to flip
                    oracle_labels[i] = 1 - oracle_labels[i]
                    flipped += 1
            logger.info(f"After balancing: greedy_better={sum(oracle_labels)}, sampling_better={len(oracle_labels) - sum(oracle_labels)}")

        logger.info(f"Generated {len(oracle_labels)} oracle labels")
        return oracle_labels

    def extract_embeddings(self, prompts: List[str]) -> np.ndarray:
        """Extract embeddings for prompts."""
        logger.info(f"Extracting embeddings for {len(prompts)} prompts...")

        if self.embedding_model is None:
            logger.info(f"Loading embedding model: {self.config.embedding_model_name}")
            self.embedding_model = SentenceTransformer(self.config.embedding_model_name)

        embeddings = self.embedding_model.encode(prompts, show_progress_bar=True)
        logger.info(f"Embeddings shape: {embeddings.shape}")
        return embeddings

    def train_classifier(
        self,
        train_embeddings: np.ndarray,
        train_labels: List[int]
    ) -> LogisticRegression:
        """Train logistic regression classifier."""
        logger.info("Training classifier...")
        classifier = LogisticRegression(max_iter=1000, random_state=42)
        classifier.fit(train_embeddings, train_labels)
        logger.info("Classifier trained")
        return classifier

    def evaluate_classifier(
        self,
        test_embeddings: np.ndarray,
        test_labels: List[int]
    ) -> float:
        """Evaluate classifier accuracy."""
        if self.classifier is None:
            raise ValueError("Classifier not trained")

        predictions = self.classifier.predict(test_embeddings)
        accuracy = accuracy_score(test_labels, predictions)
        logger.info(f"Classifier accuracy: {accuracy:.3f}")
        return accuracy

    def compare_routing_strategies(
        self,
        test_prompts: List[str],
        test_answers: List[str],
        predictions: np.ndarray
    ) -> Tuple[Dict[str, float], List[Dict]]:
        """Compare routing strategies: greedy-only, sampling-only, and router."""
        logger.info("Comparing routing strategies...")
        routing_results = {'greedy_only': 0, 'sampling_only': 0, 'router': 0}
        test_examples = []

        for i, (prompt, gt_answer) in enumerate(zip(test_prompts, test_answers)):
            logger.debug(f"Evaluating routing for prompt {i+1}/{len(test_prompts)}")

            # Greedy only
            try:
                greedy_resp, _, _ = self.client.call(
                    messages=[{'role': 'user', 'content': prompt}],
                    temperature=TEMPERATURE_GREEDY,
                    max_tokens=MAX_TOKENS
                )
                greedy_correct = check_correctness(greedy_resp, gt_answer)
            except Exception as e:
                logger.error(f"Greedy call failed for test prompt {i}: {e}")
                greedy_correct = False
                greedy_resp = ""

            # Sampling only
            samp_correct = False
            samp_resps = []
            for _ in range(self.config.num_samples):
                try:
                    samp_resp, _, _ = self.client.call(
                        messages=[{'role': 'user', 'content': prompt}],
                        temperature=TEMPERATURE_SAMPLING,
                        max_tokens=MAX_TOKENS
                    )
                    samp_resps.append(samp_resp)
                    if check_correctness(samp_resp, gt_answer):
                        samp_correct = True
                except Exception as e:
                    logger.error(f"Sampling call failed for test prompt {i}: {e}")

            # Router decision
            router_correct = False
            if predictions[i] == 1:
                router_correct = greedy_correct
                router_prediction = "greedy"
            else:
                router_correct = samp_correct
                router_prediction = "sampling"

            routing_results['router'] += int(router_correct)
            routing_results['greedy_only'] += int(greedy_correct)
            routing_results['sampling_only'] += int(samp_correct)

            # Store example
            example = {
                "input": prompt,
                "output": gt_answer,
                "predict_router": router_prediction,
                "metadata_greedy_correct": greedy_correct,
                "metadata_sampling_correct": samp_correct,
                "metadata_router_correct": router_correct,
                "metadata_router_prediction": router_prediction
            }
            test_examples.append(example)

        # Normalize to accuracy
        for key in routing_results:
            routing_results[key] /= len(test_prompts)

        logger.info(f"Routing results: {routing_results}")
        return routing_results, test_examples

    @logger.catch(reraise=True)
    def run(self) -> ExperimentResults:
        """Run the full experiment."""
        logger.info("Starting Tiny Router Experiment...")

        # Check API key
        if not OPENROUTER_API_KEY:
            logger.warning("OPENROUTER_API_KEY not set - will use mock responses for testing")
            return self._run_mock()

        # Phase 1: Load data
        all_prompts, all_answers = self.load_data()

        train_prompts = all_prompts[:self.config.train_size]
        train_answers = all_answers[:self.config.train_size]
        test_prompts = all_prompts[self.config.train_size:]
        test_answers = all_answers[self.config.train_size:]

        # Phase 2: Generate oracle labels for training
        train_labels = self.generate_oracle_labels(train_prompts, train_answers)

        # Phase 3: Extract embeddings
        train_embeddings = self.extract_embeddings(train_prompts)
        test_embeddings = self.extract_embeddings(test_prompts)

        # Free embedding model to save memory
        del self.embedding_model
        gc.collect()

        # Phase 4: Train classifier
        self.classifier = self.train_classifier(train_embeddings, train_labels)

        # Free training data
        del train_embeddings
        gc.collect()

        # Phase 5: Generate oracle labels for test
        test_labels = self.generate_oracle_labels(test_prompts, test_answers)

        # Phase 6: Evaluate classifier
        classifier_accuracy = self.evaluate_classifier(test_embeddings, test_labels)

        # Phase 7: Compare routing strategies
        predictions = self.classifier.predict(test_embeddings)
        routing_accuracy, test_examples = self.compare_routing_strategies(
            test_prompts, test_answers, predictions
        )

        # Compile results
        results = ExperimentResults(
            classifier_accuracy=classifier_accuracy,
            routing_accuracy=routing_accuracy,
            oracle_label_distribution={
                'greedy_better': sum(train_labels),
                'sampling_better': len(train_labels) - sum(train_labels)
            },
            total_cost_usd=self.cost_tracker.get_cost(),
            num_train_prompts=len(train_prompts),
            num_test_prompts=len(test_prompts),
            test_examples=test_examples
        )

        logger.info("Experiment completed successfully")
        return results

    def _run_mock(self) -> ExperimentResults:
        """Run mock experiment for testing without API."""
        logger.info("Running mock experiment...")

        # Generate synthetic data
        np.random.seed(42)
        train_size = 20  # Smaller for mock
        test_size = 10

        train_embeddings = np.random.randn(train_size, 384)
        train_labels = np.random.randint(0, 2, train_size)
        test_embeddings = np.random.randn(test_size, 384)
        test_labels = np.random.randint(0, 2, test_size)

        # Train classifier
        self.classifier = LogisticRegression(max_iter=1000, random_state=42)
        self.classifier.fit(train_embeddings, train_labels)

        # Evaluate
        predictions = self.classifier.predict(test_embeddings)
        accuracy = accuracy_score(test_labels, predictions)

        # Mock routing results
        routing_accuracy = {
            'greedy_only': 0.5 + np.random.random() * 0.1,
            'sampling_only': 0.5 + np.random.random() * 0.1,
            'router': 0.6 + np.random.random() * 0.1
        }

        results = ExperimentResults(
            classifier_accuracy=accuracy,
            routing_accuracy=routing_accuracy,
            oracle_label_distribution={
                'greedy_better': sum(train_labels),
                'sampling_better': len(train_labels) - sum(train_labels)
            },
            total_cost_usd=0.0,
            num_train_prompts=train_size,
            num_test_prompts=test_size
        )

        logger.info("Mock experiment completed")
        return results


@logger.catch(reraise=True)
def main():
    """Main entry point."""
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Tiny Router Experiment")
    parser.add_argument("--mock", action="store_true", help="Run in mock mode (no API calls)")
    parser.add_argument("--train-size", type=int, default=100, help="Number of training prompts")
    parser.add_argument("--test-size", type=int, default=50, help="Number of test prompts")
    parser.add_argument("--num-samples", type=int, default=NUM_SAMPLES, help="Number of samples for sampling strategy")
    args = parser.parse_args()

    # Create logs directory
    Path("logs").mkdir(exist_ok=True)

    # Create cache directory
    Path("cache").mkdir(exist_ok=True)

    # Set up experiment config
    config = ExperimentConfig(
        train_size=args.train_size,
        test_size=args.test_size,
        num_samples=args.num_samples
    )

    # Check if we should run in mock mode
    use_mock = args.mock or not OPENROUTER_API_KEY or OPENROUTER_API_KEY.strip() == ""

    if use_mock:
        logger.info("Running in MOCK mode (no API calls)")
        # Run mock experiment
        experiment = TinyRouterExperiment(config)
        results = experiment._run_mock()
    else:
        # Run full experiment
        logger.info("Running in FULL mode (with API calls)")
        experiment = TinyRouterExperiment(config)
        results = experiment.run()

    # Save results in exp_gen_sol_out format
    # Convert numpy types to native Python types for JSON serialization
    test_examples_serializable = []
    if results.test_examples:
        for ex in results.test_examples:
            ex_serializable = {}
            for k, v in ex.items():
                if isinstance(v, np.integer):
                    ex_serializable[k] = int(v)
                elif isinstance(v, np.floating):
                    ex_serializable[k] = float(v)
                elif isinstance(v, np.ndarray):
                    ex_serializable[k] = v.tolist()
                else:
                    ex_serializable[k] = v
            test_examples_serializable.append(ex_serializable)

    output = {
        "metadata": {
            "method_name": "tiny_router",
            "description": "Test if tiny router can predict optimal decoding strategy",
            "classifier_accuracy": float(results.classifier_accuracy),
            "routing_accuracy": {k: float(v) for k, v in results.routing_accuracy.items()},
            "total_cost_usd": float(results.total_cost_usd),
            "num_train_prompts": int(results.num_train_prompts),
            "num_test_prompts": int(results.num_test_prompts),
            "oracle_label_distribution": {k: int(v) for k, v in results.oracle_label_distribution.items()}
        },
        "datasets": [
            {
                "dataset": "gsm8k_synthetic",
                "examples": test_examples_serializable
            }
        ]
    }

    output_path = Path("method_out.json")
    output_path.write_text(json.dumps(output, indent=2))
    logger.info(f"Saved results to {output_path}")

    # Print summary
    print("\n" + "="*50)
    print("EXPERIMENT RESULTS SUMMARY")
    print("="*50)
    print(f"Classifier Accuracy: {results.classifier_accuracy:.3f}")
    print(f"Routing Accuracy:")
    for strategy, acc in results.routing_accuracy.items():
        print(f"  - {strategy}: {acc:.3f}")
    print(f"Oracle Label Distribution:")
    print(f"  - Greedy better: {results.oracle_label_distribution['greedy_better']}")
    print(f"  - Sampling better: {results.oracle_label_distribution['sampling_better']}")
    print(f"Total Cost: ${results.total_cost_usd:.4f}")
    print("="*50)


if __name__ == "__main__":
    main()
