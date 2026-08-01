#!/usr/bin/env python3
"""Download datasets for routing experiments."""
import json
from pathlib import Path
from datasets import load_dataset
from loguru import logger

logger.remove()
logger.add(lambda msg: print(msg), level="INFO")

OUTPUT_DIR = Path("temp/datasets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def download_and_save(dataset_id, config=None, split="train", filename=None, max_examples=None):
    """Download dataset and save to JSON."""
    try:
        if config:
            ds = load_dataset(dataset_id, config, split=split)
        else:
            ds = load_dataset(dataset_id, split=split)
        
        if filename is None:
            config_str = f"_{config}" if config else ""
            filename = f"{dataset_id.replace('/', '_')}{config_str}_{split}.json"
        
        output_path = OUTPUT_DIR / filename
        data = {"dataset": dataset_id, "config": config, "split": split, "rows": len(ds), "examples": []}
        
        for i, row in enumerate(ds):
            data["examples"].append(row)
            if max_examples and i >= max_examples - 1:
                break
        
        output_path.write_text(json.dumps(data, indent=2))
        logger.info(f"Saved {len(data['examples'])} examples to {output_path}")
        return str(output_path)
    except Exception as e:
        logger.error(f"Failed to download {dataset_id}: {e}")
        return None

if __name__ == "__main__":
    # Download primary datasets (full datasets)
    logger.info("Downloading GSM8K...")
    download_and_save("openai/gsm8k", config="main", split="train")
    
    logger.info("Downloading ARC-Challenge...")
    download_and_save("allenai/ai2_arc", config="ARC-Challenge", split="train")
    
    logger.info("Downloading BoolQ...")
    download_and_save("google/boolq", split="train")
    
    # Download MMLU with multiple subjects
    logger.info("Downloading MMLU subjects...")
    mmlu_subjects = ["abstract_algebra", "anatomy", "astronomy", "business_ethics", 
                     "clinical_knowledge", "college_biology", "college_chemistry", 
                     "computer_science", "econometrics", "high_school_mathematics"]
    for subject in mmlu_subjects:
        logger.info(f"  Downloading MMLU - {subject}...")
        download_and_save("cais/mmlu", config=subject, split="test", 
                         filename=f"mmlu_{subject}.json")
    
    # Download secondary datasets
    logger.info("Downloading PIQA...")
    download_and_save("baber/piqa", split="train")
    
    logger.info("Downloading CommonsenseQA...")
    download_and_save("tau/commonsense_qa", split="train")
    
    logger.info("Downloading Social IQa...")
    download_and_save("baber/social_i_qa", split="train")
    
    logger.info("Download complete!")
