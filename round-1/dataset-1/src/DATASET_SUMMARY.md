# Dataset Collection Summary

## Task
Collect and standardize QA datasets for routing experiments where a learned router picks between decoding strategies.

## Collected Datasets

### Primary Datasets (from artifact plan)
1. **GSM8K** (openai/gsm8k) - 7,473 math word problems
   - Format: "Question: {q}\nAnswer:"
   - Answer: Numerical (extracted after "####")
   - Provenance: OpenAI paper (Cobbe et al., 2021), 945K+ downloads

2. **ARC-Challenge** (allenai/ai2_arc) - 1,119 science reasoning questions
   - Format: Multiple choice with A/B/C/D options
   - Provenance: AI2 paper (Clark et al., 2018), 443K+ downloads

3. **BoolQ** (google/boolq) - 9,427 yes/no questions
   - Format: "Question: {q}\nAnswer (yes or no):"
   - Provenance: Google Research paper (Clark et al., 2019), 62K+ downloads

4. **MMLU** (cais/mmlu) - 6 subjects downloaded (752 examples total)
   - Subjects: abstract_algebra, anatomy, astronomy, business_ethics, clinical_knowledge
   - Format: Multiple choice with A/B/C/D options
   - Provenance: UC Berkeley paper (Hendrycks et al., 2020), 475K+ downloads

### Secondary Datasets (additional diversity)
5. **CommonsenseQA** (tau/commonsense_qa) - 9,741 examples
   - Commonsense reasoning multiple choice
   - Provenance: AllenAI paper (Talmor et al., 2018), 66K+ downloads

6. **PIQA** (baber/piqa) - 16,113 examples
   - Physical interaction reasoning
   - Provenance: AllenAI paper (Bisk et al., 2019), 144K+ downloads

7. **Social IQa** (baber/social_i_qa) - 33,410 examples
   - Social intelligence reasoning
   - Provenance: AllenAI paper (Sap et al., 2019), 24K+ downloads

## Processing
- Standardized format: {id, prompt, correct_answer, task_type, dataset_source, subject, metadata}
- Total examples: 78,035
- All datasets verified with >100 downloads and published papers
- Answers are automatically verifiable (numerical, multiple choice, yes/no)

## Output Files
- `processed_datasets/combined_dataset.json` - Main standardized dataset (78,035 examples)
- `temp/datasets/` - Raw downloaded datasets

## Verification
- ✓ All datasets have >100 downloads (minimum 135 for MMLU anatomy)
- ✓ All datasets have published papers/established provenance
- ✓ Clear structure with relevant fields for routing experiments
- ✓ Quality examples matching requirements (diverse task types)
- ✓ Answers are automatically verifiable

## Task Type Distribution
- math_reasoning: 7,473
- science_reasoning: 1,119
- boolean_questions: 9,427
- commonsense_reasoning: 9,741
- physical_reasoning: 16,113
- social_reasoning: 33,410
- multiple_choice: 752 (MMLU)

## Next Steps
The combined dataset is ready for use in training a router to predict optimal decoding strategy per prompt.
