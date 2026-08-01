#!/usr/bin/env python3
"""
Fetch BibTeX entries for all references in the paper.
"""
import json
import sys
import os

# Add skill scripts directory to path
skill_dir = "/home/adrian/projects/ai-inventor/.claude/skills/aii-semscholar-bib"
sys.path.insert(0, os.path.join(skill_dir, "scripts"))

# Reference data extracted from paper text
references = [
    # [1] Song et al. 2024 - arXiv:2407.10457
    {"arxiv": "2407.10457", "author": "Song", "year": 2024, "title": "The Good, The Bad, and The Greedy: Evaluation of LLMs Should Not Ignore Non-Determinism"},
    
    # [2] Wang et al. 2022 - Self-Consistency (EMNLP 2022)
    {"title": "Self-Consistency Improves Language Models as Mathematical Reasoners", "author": "Wang", "year": 2022},
    
    # [3] Zhang et al. 2026 - arXiv:2603.09065
    {"arxiv": "2603.09065", "author": "Zhang", "year": 2026, "title": "Learning Adaptive LLM Decoding"},
    
    # [4] Dhuliawala et al. 2024 - arXiv:2411.09661
    {"arxiv": "2411.09661", "author": "Dhuliawala", "year": 2024, "title": "Adaptive Decoding via Latent Preference Optimization"},
    
    # [5] Chakraborty et al. 2025 - ICLR 2025
    {"title": "Collab: Controlled Decoding using Mixture of Agents for LLM Alignment", "author": "Chakraborty", "year": 2025},
    
    # [6] Ong et al. 2024 - arXiv:2406.18665 (RouteLLM)
    {"arxiv": "2406.18665", "author": "Ong", "year": 2024, "title": "RouteLLM: Learning to Route LLMs with Preference Data"},
    
    # [7] Hu et al. 2024 - arXiv:2403.12031 (RouterBench)
    {"arxiv": "2403.12031", "author": "Hu", "year": 2024, "title": "RouterBench: A Benchmark for Multi-LLM Routing System"},
    
    # [8] Cobbe et al. 2021 - arXiv:2110.14168 (GSM8K)
    {"arxiv": "2110.14168", "author": "Cobbe", "year": 2021, "title": "Training Verifiers to Solve Math Word Problems"},
    
    # [9] Clark et al. 2018 - arXiv:1803.05457 (ARC)
    {"arxiv": "1803.05457", "author": "Clark", "year": 2018, "title": "Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge"},
    
    # [10] Clark et al. 2019 - BoolQ (NAACL 2019)
    {"title": "BoolQ: Exploring the Surprising Difficulty of Natural Yes/No Questions", "author": "Clark", "year": 2019},
    
    # [11] Hendrycks et al. 2021 - MMLU (ICLR 2021)
    {"title": "Measuring Massive Multitask Language Understanding", "author": "Hendrycks", "year": 2021},
    
    # [12] Chen et al. 2025 - Mixture of Decoding (ACL Findings 2025)
    {"title": "Mixture of Decoding: An Attention-Inspired Adaptive Decoding Strategy to Mitigate Hallucinations in Large Vision-Language Models", "author": "Chen", "year": 2025},
    
    # [13] Lu et al. 2024 - arXiv:2402.05845
    {"arxiv": "2402.05845", "author": "Lu", "year": 2024, "title": "Routing to the Right Model: A Learning-Based Approach"},
    
    # [14] Belinkov and Glass 2019 - TACL
    {"title": "Analysis Methods in Neural Language Processing: A Survey", "author": "Belinkov", "year": 2019},
    
    # [15] Tenney et al. 2019 - BERT Rediscovers (NAACL 2019)
    {"title": "BERT Rediscovers the Classical NLP Pipeline", "author": "Tenney", "year": 2019},
    
    # [16] Reimers and Gurevych 2019 - Sentence-BERT (EMNLP-IJCNLP 2019)
    {"title": "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks", "author": "Reimers", "year": 2019},
]

# Try to import and call the ability function
try:
    from aii_semscholar_bib__fetch import aii_semscholar_bib__fetch
    
    print("Calling aii_semscholar_bib__fetch with references...")
    result = aii_semscholar_bib__fetch(references=references)
    
    print(f"\nSuccess: {result.get('success')}")
    print(f"Total: {result.get('total')}")
    print(f"Found: {result.get('found')}")
    print(f"Failed: {result.get('failed_count')}")
    
    if result.get('bib_text'):
        with open('references.bib', 'w') as f:
            f.write(result['bib_text'])
        print("\nSaved references.bib")
    else:
        print("\nNo bib_text returned")
        
except Exception as e:
    print(f"Error: {e}")
    print("\nTrying alternative approach...")
    
    # Fallback: try using the CLI script
    import subprocess
    
    refs_json = json.dumps(references)
    cmd = [
        os.path.join(skill_dir, "../.ability_client_venv/bin/python"),
        os.path.join(skill_dir, "scripts/aii_semscholar_bib__fetch.py"),
        "--refs", refs_json
    ]
    
    print(f"Running command: {' '.join(cmd[:3])} ...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Success!")
        print(result.stdout)
    else:
        print(f"Error: {result.stderr}")
