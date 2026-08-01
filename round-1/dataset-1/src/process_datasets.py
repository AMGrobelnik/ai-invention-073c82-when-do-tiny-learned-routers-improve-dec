#!/usr/bin/env python3
"""Process and standardize datasets for routing experiments."""
import json
from pathlib import Path
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")

INPUT_DIR = Path("temp/datasets")
OUTPUT_DIR = Path("processed_datasets")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def process_gsm8k(filepath):
    """Process GSM8K dataset."""
    data = json.loads(Path(filepath).read_text())
    examples = []
    for i, ex in enumerate(data["examples"]):
        # Extract answer after ####
        answer = ex.get("answer", "")
        if "####" in answer:
            correct = answer.split("####")[-1].strip()
        else:
            correct = answer.strip()
        
        examples.append({
            "id": f"gsm8k_{i}",
            "prompt": f"Question: {ex.get('question', '')}\nAnswer:",
            "correct_answer": correct,
            "task_type": "math_reasoning",
            "dataset_source": "openai/gsm8k",
            "subject": "math",
            "metadata": {"full_answer": answer}
        })
    return examples

def process_arc(filepath):
    """Process ARC-Challenge dataset."""
    data = json.loads(Path(filepath).read_text())
    examples = []
    for i, ex in enumerate(data["examples"]):
        choices = ex.get("choices", {})
        texts = choices.get("text", [])
        labels = choices.get("label", [])
        
        # Format choices
        choice_str = "\n".join([f"{l}. {t}" for l, t in zip(labels, texts)])
        prompt = f"Question: {ex.get('question', '')}\n{choice_str}\nAnswer:"
        
        examples.append({
            "id": f"arc_{ex.get('id', i)}",
            "prompt": prompt,
            "correct_answer": ex.get("answerKey", ""),
            "task_type": "science_reasoning",
            "dataset_source": "allenai/ai2_arc",
            "subject": "science",
            "metadata": {"choices": texts, "labels": labels}
        })
    return examples

def process_boolq(filepath):
    """Process BoolQ dataset."""
    data = json.loads(Path(filepath).read_text())
    examples = []
    for i, ex in enumerate(data["examples"]):
        examples.append({
            "id": f"boolq_{i}",
            "prompt": f"Question: {ex.get('question', '')}\nAnswer (yes or no):",
            "correct_answer": "yes" if ex.get("answer") else "no",
            "task_type": "boolean_questions",
            "dataset_source": "google/boolq",
            "subject": "general_knowledge",
            "metadata": {"passage": ex.get("passage", "")}
        })
    return examples

def process_commonsenseqa(filepath):
    """Process CommonsenseQA dataset."""
    data = json.loads(Path(filepath).read_text())
    examples = []
    for i, ex in enumerate(data["examples"]):
        choices = ex.get("choices", {})
        texts = choices.get("text", [])
        labels = choices.get("label", [])
        
        choice_str = "\n".join([f"{l}. {t}" for l, t in zip(labels, texts)])
        prompt = f"Question: {ex.get('question', '')}\n{choice_str}\nAnswer:"
        
        examples.append({
            "id": f"csqa_{ex.get('id', i)}",
            "prompt": prompt,
            "correct_answer": ex.get("answerKey", ""),
            "task_type": "commonsense_reasoning",
            "dataset_source": "tau/commonsense_qa",
            "subject": ex.get("question_concept", "commonsense"),
            "metadata": {"choices": texts, "labels": labels}
        })
    return examples

def process_piqa(filepath):
    """Process PIQA dataset."""
    data = json.loads(Path(filepath).read_text())
    examples = []
    for i, ex in enumerate(data["examples"]):
        prompt = f"Goal: {ex.get('goal', '')}\nA. {ex.get('sol1', '')}\nB. {ex.get('sol2', '')}\nAnswer:"
        examples.append({
            "id": f"piqa_{i}",
            "prompt": prompt,
            "correct_answer": "A" if str(ex.get("label", "")) == "0" else "B",
            "task_type": "physical_reasoning",
            "dataset_source": "baber/piqa",
            "subject": "physical_interaction",
            "metadata": {"sol1": ex.get("sol1", ""), "sol2": ex.get("sol2", "")}
        })
    return examples

def process_mmlu(filepath, subject):
    """Process MMLU dataset."""
    data = json.loads(Path(filepath).read_text())
    examples = []
    for i, ex in enumerate(data["examples"]):
        choices = ex.get("choices", [])
        choice_str = "\n".join([f"{chr(65+j)}. {c}" for j, c in enumerate(choices)])
        prompt = f"Question: {ex.get('question', '')}\n{choice_str}\nAnswer:"
        
        examples.append({
            "id": f"mmlu_{subject}_{i}",
            "prompt": prompt,
            "correct_answer": str(ex.get("answer", "")),
            "task_type": "multiple_choice",
            "dataset_source": "cais/mmlu",
            "subject": subject,
            "metadata": {"choices": choices}
        })
    return examples

def process_social_iqa(filepath):
    """Process Social IQa dataset."""
    data = json.loads(Path(filepath).read_text())
    examples = []
    for i, ex in enumerate(data["examples"]):
        # Social IQa has different format
        prompt = f"Context: {ex.get('context', '')}\nQuestion: {ex.get('question', '')}\nAnswer:"
        examples.append({
            "id": f"social_iqa_{i}",
            "prompt": prompt,
            "correct_answer": ex.get("answer", ""),
            "task_type": "social_reasoning",
            "dataset_source": "baber/social_i_qa",
            "subject": "social_intelligence",
            "metadata": {}
        })
    return examples



if __name__ == "__main__":
    all_examples = []
    
    # Process each dataset
    logger.info("Processing GSM8K...")
    gsm8k_examples = process_gsm8k(INPUT_DIR / "openai_gsm8k_main_train.json")
    all_examples.extend(gsm8k_examples)
    logger.info(f"  Added {len(gsm8k_examples)} examples")
    
    logger.info("Processing ARC-Challenge...")
    arc_examples = process_arc(INPUT_DIR / "allenai_ai2_arc_ARC-Challenge_train.json")
    all_examples.extend(arc_examples)
    logger.info(f"  Added {len(arc_examples)} examples")
    
    logger.info("Processing BoolQ...")
    boolq_examples = process_boolq(INPUT_DIR / "google_boolq_train.json")
    all_examples.extend(boolq_examples)
    logger.info(f"  Added {len(boolq_examples)} examples")
    
    logger.info("Processing CommonsenseQA...")
    csqa_examples = process_commonsenseqa(INPUT_DIR / "tau_commonsense_qa_train.json")
    all_examples.extend(csqa_examples)
    logger.info(f"  Added {len(csqa_examples)} examples")
    
    logger.info("Processing PIQA...")
    piqa_examples = process_piqa(INPUT_DIR / "baber_piqa_train.json")
    all_examples.extend(piqa_examples)
    logger.info(f"  Added {len(piqa_examples)} examples")
    
    logger.info("Processing Social IQa...")
    social_examples = process_social_iqa(INPUT_DIR / "baber_social_i_qa_train.json")
    all_examples.extend(social_examples)
    logger.info(f"  Added {len(social_examples)} examples")
    
    # Process MMLU subjects
    logger.info("Processing MMLU subjects...")
    mmlu_files = list(INPUT_DIR.glob("mmlu_*.json"))
    for mmlu_file in mmlu_files:
        subject = mmlu_file.stem.replace("mmlu_", "")
        logger.info(f"  Processing MMLU - {subject}...")
        mmlu_examples = process_mmlu(mmlu_file, subject)
        all_examples.extend(mmlu_examples)
        logger.info(f"    Added {len(mmlu_examples)} examples")
    
    # Save combined dataset
    output = {"total_examples": len(all_examples), "examples": all_examples}
    output_path = OUTPUT_DIR / "combined_dataset.json"
    output_path.write_text(json.dumps(output, indent=2))
    logger.info(f"Saved {len(all_examples)} total examples to {output_path}")
    
    # Create summary
    summary = {}
    for ex in all_examples:
        task = ex["task_type"]
        summary[task] = summary.get(task, 0) + 1
    logger.info(f"Dataset summary by task type: {summary}")
