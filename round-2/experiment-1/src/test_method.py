#!/usr/bin/env python3
"""Test script to verify method.py works with mini dataset without API calls."""

from loguru import logger
from pathlib import Path
import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from sentence_transformers import SentenceTransformer
import sys

# Configure logging
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

def test_data_loading():
    """Test data loading from mini dataset."""
    logger.info("Testing data loading...")
    
    data_path = Path("mini_data_out.json")
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    examples = []
    for dataset_info in data.get('datasets', []):
        dataset_name = dataset_info['dataset']
        for i, ex in enumerate(dataset_info.get('examples', [])):
            ex['dataset'] = dataset_name
            ex['example_id'] = f"{dataset_name}_{i}"
            examples.append(ex)
    
    logger.info(f"Loaded {len(examples)} examples from mini dataset")
    assert len(examples) == 12, f"Expected 12 examples, got {len(examples)}"
    
    # Check structure
    for ex in examples:
        assert 'input' in ex, "Missing 'input' field"
        assert 'output' in ex, "Missing 'output' field"
        assert 'dataset' in ex, "Missing 'dataset' field"
    
    logger.info("Data loading test PASSED")
    return examples

def test_embedding_extraction(examples):
    """Test embedding extraction."""
    logger.info("Testing embedding extraction...")
    
    prompts = [ex['input'] for ex in examples]
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(prompts, show_progress_bar=True)
    
    logger.info(f"Embeddings shape: {embeddings.shape}")
    assert embeddings.shape[0] == len(examples), "Wrong number of embeddings"
    assert embeddings.shape[1] == 384, f"Wrong embedding dimension: {embeddings.shape[1]}"
    
    logger.info("Embedding extraction test PASSED")
    return embeddings

def test_classifier_training(embeddings, examples):
    """Test classifier training with heuristic labels."""
    logger.info("Testing classifier training...")
    
    # Create heuristic labels based on dataset type
    # This is just for testing the pipeline
    labels = np.array([1 if 'gsm8k' in ex.get('dataset', '').lower() else 0 
                       for ex in examples])
    
    # Ensure we have at least 2 classes
    if len(np.unique(labels)) < 2:
        logger.warning("Only one class in labels, creating artificial second class")
        labels[0] = 1  # Make at least one example class 1
    
    X_train, X_test, y_train, y_test = train_test_split(
        embeddings, labels, test_size=0.3, random_state=42, stratify=labels
    )
    
    clf = LogisticRegression(max_iter=1000)
    clf.fit(X_train, y_train)
    
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    logger.info(f"Classifier test: accuracy={accuracy:.3f}, f1={f1:.3f}")
    logger.info("Classifier training test PASSED")
    return clf

def test_answer_parsing():
    """Test answer parsing function."""
    logger.info("Testing answer parsing...")
    
    # Import the parse function from method.py
    sys.path.insert(0, '.')
    from method import parse_answer
    
    # Test math reasoning
    assert parse_answer("The answer is 72", "math_reasoning", "72") == True
    assert parse_answer("I think it's 10", "math_reasoning", "10") == True
    assert parse_answer("Answer: 100", "math_reasoning", "50") == False
    
    # Test multiple choice
    assert parse_answer("A. dry palms", "science_reasoning", "A") == True
    assert parse_answer("The answer is B", "multiple_choice", "1") == True  # 1 -> B
    assert parse_answer("C", "science_reasoning", "D") == False
    
    # Test boolean
    assert parse_answer("Yes, they do", "boolean_questions", "yes") == True
    assert parse_answer("No, they don't", "boolean_questions", "no") == True
    assert parse_answer("Yes", "boolean_questions", "no") == False
    
    logger.info("Answer parsing test PASSED")

@logger.catch(reraise=True)
def main():
    """Run all tests."""
    logger.info("Starting method.py tests with mini dataset")
    
    # Test 1: Data loading
    examples = test_data_loading()
    
    # Test 2: Embedding extraction
    embeddings = test_embedding_extraction(examples)
    
    # Test 3: Classifier training
    clf = test_classifier_training(embeddings, examples)
    
    # Test 4: Answer parsing
    test_answer_parsing()
    
    logger.info("All tests PASSED! method.py is ready for full run.")
    
    # Save test results
    results = {
        "test": "mini_dataset",
        "num_examples": len(examples),
        "embedding_shape": list(embeddings.shape),
        "status": "passed"
    }
    Path("test_results.json").write_text(json.dumps(results, indent=2))
    logger.info("Test results saved to test_results.json")

if __name__ == "__main__":
    main()
