# Routing Experiment

## Overview
This experiment tests whether a tiny learned router can pick between two decoding strategies (greedy vs sampling) per prompt to beat always using either one alone.

## Hypothesis
Routing between greedy and sampling decoding based on prompt embeddings improves accuracy only when optimal strategies are balanced (30-70% distribution), not when one strategy dominates.

## Method
1. **Data Loading**: Load 4 QA datasets (GSM8K, ARC, BoolQ, MMLU) with 18,771 total examples
2. **Oracle Label Generation**: For each prompt, run both strategies via OpenRouter API:
   - Greedy: temperature=0, max_tokens=512
   - Sampling: temperature=0.7, num_samples=3 (best-of-3)
   - Parse responses by task type and determine oracle label (1 if sampling correct, 0 otherwise)
3. **Embedding Extraction**: Use sentence-transformers (all-MiniLM-L6-v2) to encode prompts
4. **Classifier Training**: LogisticRegression on 70/30 train/test split with 5-fold CV
5. **Routing Evaluation**: Compare router accuracy vs baselines:
   - Always-greedy, always-sampling, random routing (50/50), oracle routing (upper bound)
6. **Conditional Hypothesis Test**: Verify routing benefit > 0 only when 30-70% sampling optimal
7. **Mixed Datasets**: Create subsets with controlled ratios to verify hypothesis

## Usage

### Mock Mode (Testing without API)
```bash
MOCK_MODE=true python method.py
```

### Real Mode (Requires OpenRouter API Key)
```bash
export OPENROUTER_API_KEY="your-key-here"
python method.py
```

### With Full Dataset
Edit `method.py` and change line 709 from `mini_data_out.json` to `full_data_out.json`

## Output Files
- `method_out.json`: Full experiment results in JSON format
- `exp_gen_sol_out.json`: Results in exp_gen_sol_out schema format
- `logs/run.log`: Detailed experiment logs
- `cache/`: Cached API responses and embeddings

## Results Summary (Mock Mode Test)
- Router accuracy: 0.750
- Routing benefit: 0.083 (improvement over best baseline)
- Hypothesis supported: False (due to mock data limitations)

## Dependencies
See `pyproject.toml` for full list. Key packages:
- numpy, pandas, scikit-learn
- sentence-transformers, torch
- matplotlib, seaborn
- loguru, tenacity

## Notes
- Maximum API budget: $10 USD
- Memory limit: 80% of available RAM
- Embeddings are cached to disk for efficiency
- API responses are cached to avoid duplicate calls
