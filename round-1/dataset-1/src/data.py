#!/usr/bin/env python3
"""Convert processed datasets to exp_sel_data_out.json format."""
import json
from pathlib import Path
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

INPUT_FILE = Path("processed_datasets/combined_dataset.json")
OUTPUT_FILE = Path("full_data_out.json")

def convert_to_experiment_format(input_data):
    """Convert processed dataset to experiment format."""
    # Group examples by dataset_source
    datasets_dict = {}
    
    # Only include the 4 primary datasets from the artifact plan
    primary_datasets = ["openai/gsm8k", "allenai/ai2_arc", "google/boolq", "cais/mmlu"]
    
    for example in input_data["examples"]:
        dataset_name = example["dataset_source"]
        
        # Skip if not in primary datasets
        if dataset_name not in primary_datasets:
            continue
        
        if dataset_name not in datasets_dict:
            datasets_dict[dataset_name] = {
                "dataset": dataset_name,
                "examples": []
            }
        
        # Convert to required format
        converted_example = {
            "input": example["prompt"],
            "output": str(example["correct_answer"]),
            "metadata_task_type": example["task_type"],
            "metadata_subject": example["subject"],
            "metadata_id": example["id"]
        }
        
        # Add any additional metadata
        if "metadata" in example and example["metadata"]:
            for key, value in example["metadata"].items():
                if key not in ["full_answer", "choices", "labels"]:  # Skip large fields
                    converted_example[f"metadata_{key}"] = value
        
        datasets_dict[dataset_name]["examples"].append(converted_example)
    
    # Convert to list
    datasets_list = list(datasets_dict.values())
    
    return {
        "datasets": datasets_list
    }

if __name__ == "__main__":
    logger.info(f"Loading processed dataset from {INPUT_FILE}...")
    input_data = json.loads(INPUT_FILE.read_text())
    
    logger.info(f"Converting {input_data['total_examples']} examples to experiment format...")
    output_data = convert_to_experiment_format(input_data)
    
    logger.info(f"Saving to {OUTPUT_FILE}...")
    OUTPUT_FILE.write_text(json.dumps(output_data, indent=2))
    
    # Print summary
    logger.info(f"Conversion complete!")
    logger.info(f"Total datasets: {len(output_data['datasets'])}")
    for dataset in output_data["datasets"]:
        logger.info(f"  {dataset['dataset']}: {len(dataset['examples'])} examples")
