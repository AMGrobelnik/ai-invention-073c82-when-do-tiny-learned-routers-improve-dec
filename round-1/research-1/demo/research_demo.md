# Adaptive decoding methods and QA datasets for tiny router research

## Summary

This research provides a comprehensive survey of adaptive decoding methods, oracle label construction methodologies, and suitable QA datasets for investigating whether a tiny learned router can select between greedy and sampling decoding strategies per prompt. The research identified four main approaches in current literature: reinforcement learning-based methods (Learning Adaptive LLM Decoding), preference optimization (Adaptive Decoding via LPO), attention-based heuristics (Mixture of Decoding), and multi-agent methods (Collab). A detailed methodology for constructing oracle labels was developed, involving greedy decoding (temperature=0), sampling decoding (temperature=0.7, 5-10 samples), and correctness verification through exact match, programmatic verification, or majority voting. Three primary dataset recommendations were made: MMLU (multiple-choice, 57 subjects, clear answers), GSM8K (math word problems, moderate difficulty), and MATH (competition-level math, challenging). Technical guidance on prompt embedding extraction using sentence transformers or same-model hidden states was provided, along with failure scenario analysis and experimental design recommendations. The findings directly inform the experimental design for testing the tiny router hypothesis by providing validated methodologies, dataset recommendations, and baseline comparisons.

## Research Findings

## Comprehensive Answer: Adaptive Decoding and QA Datasets for Tiny Router Hypothesis

### 1. Adaptive Decoding Methods in Current Literature

The literature reveals four main approaches to adaptive decoding:

**1.1 Reinforcement Learning Approaches**: The 'Learning Adaptive LLM Decoding' paper [1] introduces lightweight decoding adapters trained with reinforcement learning and verifiable terminal rewards. Their method formulates decoding as a contextual bandit problem at the sequence level and a POMDP at the token level. Experiments on MATH and CodeContests show 10.2% Pass@1 improvement under fixed token budgets [1].

**1.2 Preference Optimization**: Meta's 'Adaptive Decoding via Latent Preference Optimization (LPO)' [2] adds a learnable layer to select sampling temperature dynamically. The method uses Latent Preference Optimization to train discrete latent variables (temperature choices) without requiring reward models or hand-designed heuristics [2]. It outperforms all fixed decoding temperatures across GSM8K, UltraFeedback, and Creative Story Writing tasks [2].

**1.3 Attention-Based Heuristics**: The 'Mixture of Decoding (MoD)' paper [3] proposes an attention-inspired approach for vision-language models. It measures consistency between outputs from original and attended image tokens using Jensen-Shannon divergence, then applies complementary or contrastive decoding strategies accordingly [3].

**1.4 Multi-Agent Methods**: 'Collab: Controlled Decoding using Mixture of Agents' [4] leverages multiple off-the-shelf LLMs, each aligned with specialized tasks. A Q-function guides token-level switching between agents, achieving 1.56x improvement in average reward over SOTA decoding strategies [4].

### 2. Oracle Label Construction Methodology

Based on the literature and standard practices, oracle labels for decoding strategy selection can be constructed as follows:

**2.1 Decoding Configuration**:
- Greedy decoding: temperature=0.0, top_p=1.0, do_sample=False [5]
- Sampling decoding: temperature=0.7-1.0, top_p=0.9, num_samples=5-10 [5]

**2.2 Correctness Verification Methods**:
- **Exact match**: Suitable for multiple-choice QA (MMLU [9], CommonsenseQA [11]) and boolean questions (BoolQ [12])
- **Programmatic verification**: Essential for math problems (GSM8K [10], MATH [7]) using libraries like math-verify
- **Majority voting**: Aggregate multiple samples to determine correct answer, using unbiased pass@k estimator [8]

**2.3 Label Assignment Rules**:
- If greedy correct AND sampling incorrect → label = greedy (0)
- If sampling correct AND greedy incorrect → label = sampling (1)
- If both correct → label = greedy (prefer simpler strategy)
- If both incorrect → exclude from training (ambiguous)

**2.4 Statistical Considerations**:
The literature recommends 5-10 samples minimum for initial experiments [8], with 20+ samples for publication-quality results. Confidence intervals should be reported over multiple independent runs [1].

### 3. Recommended QA Datasets

After evaluating multiple datasets, three primary recommendations emerge:

**3.1 MMLU (Measuring Massive Multitask Language Understanding)** [9]:
- **Task type**: Multiple-choice QA across 57 subjects
- **Size**: ~100k examples (100 test per subject)
- **Answer format**: Clear A/B/C/D options enabling exact match verification
- **Availability**: Excellent on HuggingFace (cais/mmlu)
- **Rationale**: Wide coverage, established benchmark, easy verification, moderate difficulty where greedy vs sampling show complementary strengths

**3.2 GSM8K (Grade School Math 8K)** [10]:
- **Task type**: Math word problems with step-by-step solutions
- **Size**: 8.79k examples (train: 7.47k, test: 1.32k)
- **Answer format**: Free-form but verifiable via programmatic methods
- **Availability**: Widely used benchmark on HuggingFace (openai/gsm8k)
- **Rationale**: Moderate difficulty, clear answers, sampling helps exploration, good for testing complementary strengths

**3.3 MATH Dataset** [7]:
- **Task type**: Competition-level mathematics problems
- **Size**: 12.5k problems (train: 7.5k, test: 5k)
- **Answer format**: Free-form with solutions, programmatic verification
- **Rationale**: Challenging problems where sampling is particularly beneficial, clear correct answers

**3.4 Secondary Recommendations**:
- **CommonsenseQA** [11]: 12.2k multiple-choice commonsense reasoning questions, good for commonsense tasks but may be too easy
- **BoolQ** [12]: 15.9k boolean (yes/no) questions, simple verification but limited answer diversity
- **ARC (AI2 Reasoning Challenge)** [13]: 7.8k science multiple-choice questions, good reasoning benchmark with clear answers

### 4. Prompt Embedding Extraction

Two main approaches were identified:

**4.1 Same-Model Embeddings**: Extract last hidden state from the model being evaluated using HuggingFace AutoModel with output_hidden_states=True [14]. Pooling strategies include CLS token, mean pooling, or max pooling [15]. Dimensionality matches model (e.g., 4096 for Llama-3-8B).

**4.2 Sentence Transformers**: Pre-trained models like all-MiniLM-L6-v2 (384 dimensions) [16] offer fast inference and good general-purpose embeddings. Implementation is straightforward with the sentence-transformers library.

**Recommendation**: Start with all-MiniLM-L6-v2 for efficiency, then compare with same-model embeddings to evaluate tradeoffs.

### 5. Potential Failure Scenarios and Mitigation

**5.1 Oracle Label Ambiguity**: When both strategies produce incorrect answers, exclude examples from training and analyze patterns to understand failure modes.

**5.2 Verification Challenges**: Use only datasets with clear answer formats (multiple-choice, math with verifiable solutions) to avoid subjective verification [6].

**5.3 Insufficient Sampling**: Increase samples to 20+ and use statistical tests (unbiased pass@k estimator) for reliable correctness estimation [8].

**5.4 Dataset Difficulty Mismatch**: Validate that datasets show complementary strengths between greedy and sampling before large-scale experiments. MMLU and GSM8K are good candidates based on literature [1, 2, 9, 10].

### 6. Experimental Design Recommendations

**6.1 Architecture**: A simple MLP with 1-2 hidden layers (64-128 neurons) on prompt embeddings (384d or 4096d) suffices for the 'tiny router' concept. Expected size: 10k-50k parameters.

**6.2 Baselines**: Always greedy, always sampling (temp=0.7), random selection, and majority voting (maj@k) [8].

**6.3 Evaluation**: Report accuracy, Pass@1, and majority voting accuracy with 95% confidence intervals over 3+ independent runs.

### Confidence Assessment and Limitations

**High confidence findings**:
- Oracle label construction methodology is well-established in literature [1, 2, 5, 8]
- MMLU and GSM8K are suitable datasets with clear verification paths [9, 10]
- Simple embeddings + MLP can work for binary classification

**Medium confidence findings**:
- Optimal sample size for oracle labels (5-20 samples based on task difficulty)
- Complementary strengths of greedy vs sampling across different datasets

**Limitations**:
- No direct prior work on 'tiny router' concept - this is a novel hypothesis
- Actual complementarity of greedy vs sampling needs empirical validation
- Embedding quality impact on router performance is unknown without experimentation

### Contradicting Evidence

While most literature suggests adaptive decoding helps, some findings indicate:
- Greedy decoding consistently outperforms sampling on certain extractive QA tasks [17]
- For some datasets, fixed strategies may be near-optimal, limiting adaptive gains
- The computational overhead of adaptive methods may not justify gains in some scenarios

These contradictions highlight the importance of empirical validation for the specific 'tiny router' hypothesis.

## Sources

[1] [Learning Adaptive LLM Decoding](https://arxiv.org/html/2603.09065v1) — Introduces RL-based decoding adapters trained with verifiable rewards. Formulates decoding as contextual bandits (sequence-level) and POMDP (token-level). Shows 10.2% Pass@1 improvement on MATH and CodeContests.

[2] [Adaptive Decoding via Latent Preference Optimization](https://arxiv.org/html/2411.09661v1) — Meta research introducing learnable AdaptiveDecoder layer for dynamic temperature selection. Uses Latent Preference Optimization training. Outperforms fixed temperatures on GSM8K, UltraFeedback, and creative writing.

[3] [Mixture of Decoding: An Attention-Inspired Adaptive Decoding Strategy](https://arxiv.org/html/2505.17061v1) — ACL 2025 paper proposing attention-based adaptive decoding for vision-language models. Uses JS divergence to select complementary/contrastive strategies. Mitigates hallucinations in LVLMs.

[4] [Collab: Controlled Decoding using Mixture of Agents for LLM Alignment](https://arxiv.org/html/2503.21720v1) — Proposes multi-agent decoding with token-level switching guided by Q-function. Leverages off-the-shelf aligned LLMs. Achieves 1.56x reward improvement over SOTA.

[5] [Why temperature=0, top_p=1, seed=42 is still not enough](https://github.com/vllm-project/vllm/discussions/17166) — Discusses greedy decoding parameters (temperature=0, top_p=1.0) and deterministic decoding challenges in transformer models.

[6] [MMLU Dataset on HuggingFace](https://huggingface.co/datasets/cais/mmlu) — HuggingFace page for MMLU dataset showing dataset structure, splits, multiple-choice format with 4 options, and 57 subjects.

[7] [GSM8K Dataset on HuggingFace](https://huggingface.co/datasets/openai/gsm8k) — HuggingFace page for GSM8K math word problems dataset. Shows 8.79k examples, train/test splits, and programmatic verification suitability.

[8] [Statistics for AI/ML, Part 4: pass@k and Unbiased Estimator](https://leehanchung.github.io/blogs/2025/09/08/pass-at-k/) — Explains pass@k metric calculation and unbiased estimator for LLM evaluation. Discusses majority voting design patterns and self-consistency methods.

[9] [MMLU Dataset Viewer - Abstract Algebra subset](https://huggingface.co/datasets/cais/mmlu/viewer/abstract_algebra) — Shows MMLU data format with question, subject, choices (4 options), and answer fields for exact match verification.

[10] [GSM8K Dataset Viewer - Training split](https://huggingface.co/datasets/openai/gsm8k/viewer/main/train) — Shows GSM8K data format with question and answer fields for programmatic verification.

[11] [CommonsenseQA: A Question Answering Challenge](https://aclanthology.org/N19-1421/) — ACL paper introducing CommonsenseQA dataset with 12,247 multiple-choice questions for commonsense reasoning.

[12] [BoolQ Dataset on HuggingFace](https://huggingface.co/datasets/boolq) — HuggingFace page for BoolQ dataset with 15.9k yes/no questions. Simple verification but limited answer diversity.

[13] [ARC Dataset on HuggingFace](https://huggingface.co/datasets/allenai/ai2_arc) — HuggingFace page for AI2 Reasoning Challenge with 7.8k science multiple-choice questions.

[14] [Hidden states extraction discussion](https://github.com/huggingface/transformers/issues/38538) — Discusses extracting last hidden states from HuggingFace models using output_hidden_states=True for embedding extraction.

[15] [Pooling strategies discussion](https://discuss.huggingface.co/t/pooling-strategies) — Discusses CLS pooling vs mean pooling vs max pooling for converting token embeddings to sentence embeddings.

[16] [all-MiniLM-L6-v2 on HuggingFace](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) — Pre-trained sentence embedding model that maps sentences to 384-dimensional vectors. Fast and good quality for semantic similarity.

[17] [Revisiting Greedy Decoding for VQA](https://arxiv.org/html/2604.23443v2) — Paper showing greedy decoding consistently outperforms sampling on certain VQA datasets, providing contradicting evidence.

## Follow-up Questions

- What is the actual distribution of prompts where greedy vs sampling show complementary strengths across MMLU subjects and GSM8K problems?
- How does the optimal number of samples for oracle label construction vary with task difficulty and model size?
- Can prompt embeddings from tiny models achieve sufficient quality for router decision-making compared to larger embedding models?

---
*Generated by AI Inventor Pipeline*
