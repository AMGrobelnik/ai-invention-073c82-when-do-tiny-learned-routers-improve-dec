#!/usr/bin/env python3
"""Script to create mixed datasets and test the hypothesis properly."""

import json
import numpy as np
from pathlib import Path
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

def create_mixed_datasets():
    """Create mixed datasets with controlled sampling optimal ratios."""
    logger.info("Creating mixed datasets from cached oracle labels")
    
    # Load cached oracle labels
    cache_file = Path("cache/oracle_labels.json")
    if not cache_file.exists():
        logger.error("No cached oracle labels found. Run method.py first.")
        return
    
    with open(cache_file, 'r') as f:
        cached_data = json.load(f)
    
    # Convert to list
    oracle_results = [OracleResult(**v) for v in cached_data.values()]
    
    # Separate by sampling optimal
    sampling_optimal = [r for r in oracle_results if r.sampling_optimal == 1]
    greedy_optimal = [r for r in oracle_results if r.sampling_optimal == 0]
    
    logger.info(f"Total cached: {len(oracle_results)}")
    logger.info(f"Sampling optimal: {len(sampling_optimal)}")
    logger.info(f"Greedy optimal: {len(greedy_optimal)}")
    
    # Create mixed datasets with different ratios
    ratios = [0.3, 0.4, 0.5, 0.6, 0.7]
    mixed_datasets = {}
    
    for target_ratio in ratios:
        if len(greedy_optimal) == 0:
            logger.warning("No greedy optimal examples available")
            break
        
        # Calculate sizes
        n_total = min(200, len(sampling_optimal) + len(greedy_optimal))
        n_sampling = int(n_total * target_ratio)
        n_greedy = n_total - n_sampling
        
        # Adjust if not enough examples
        n_sampling = min(n_sampling, len(sampling_optimal))
        n_greedy = min(n_greedy, len(greedy_optimal))
        n_total = n_sampling + n_greedy
        
        if n_total < 20:
            logger.warning(f"Not enough examples for ratio {target_ratio}")
            continue
        
        # Sample examples
        np.random.seed(42)
        sampled_sampling = np.random.choice(sampling_optimal, n_sampling, replace=False)
        sampled_greedy = np.random.choice(greedy_optimal, n_greedy, replace=False)
        
        mixed = list(sampled_sampling) + list(sampled_greedy)
        np.random.shuffle(mixed)
        
        actual_ratio = sum(1 for r in mixed if r.sampling_optimal) / len(mixed)
        mixed_datasets[target_ratio] = {
            'examples': mixed,
            'actual_ratio': actual_ratio,
            'n_examples': len(mixed)
        }
        
        logger.info(f"Ratio {target_ratio}: Created dataset with {len(mixed)} examples, "
                   f"actual ratio: {actual_ratio:.2f}")
    
    return mixed_datasets

def test_routing_on_mixed_datasets(mixed_datasets):
    """Test routing performance on mixed datasets."""
    logger.info("Testing routing on mixed datasets")
    
    results = []
    for target_ratio, data in mixed_datasets.items():
        mixed = data['examples']
        
        # Extract embeddings
        from method import extract_embeddings
        prompts = [r.prompt for r in mixed]
        embeddings = extract_embeddings(prompts)
        
        # Train classifier
        from method import train_classifier
        X = embeddings
        y = np.array([r.sampling_optimal for r in mixed])
        
        config = ExperimentConfig()
        clf, metrics = train_classifier(X, y, config)
        
        # Evaluate routing
        from method import evaluate_routing
        eval_results = evaluate_routing(mixed, clf, embeddings)
        
        results.append({
            'target_ratio': target_ratio,
            'actual_ratio': data['actual_ratio'],
            'classifier_accuracy': metrics['accuracy'],
            'router_accuracy': eval_results['router_accuracy'],
            'routing_benefit': eval_results['routing_benefit']
        })
        
        logger.info(f"Ratio {target_ratio}: benefit={eval_results['routing_benefit']:.3f}")
    
    return results

if __name__ == "__main__":
    # Need to import from method.py
    from method import OracleResult, ExperimentConfig
    
    mixed_datasets = create_mixed_datasets()
    if mixed_datasets:
        results = test_routing_on_mixed_datasets(mixed_datasets)
        
        # Save results
        output = {
            'mixed_dataset_results': results,
            'hypothesis_test': 'Routing benefit should be positive only for 30-70% ratios'
        }
        
        Path("mixed_dataset_results.json").write_text(json.dumps(output, indent=2))
        logger.info("Mixed dataset results saved to mixed_dataset_results.json")
