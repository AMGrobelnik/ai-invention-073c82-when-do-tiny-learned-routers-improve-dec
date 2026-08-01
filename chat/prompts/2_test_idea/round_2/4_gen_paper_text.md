# gen_paper_text — test_idea

> Phase: `invention_loop` · round 2 · `gen_paper_text`
> Run: `run_C4UvEedrrr_P` — When Do Tiny Learned Routers Improve Decoding Strategy Selection?
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_paper_text` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-07-31 23:28:32 UTC

````
<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for related-work positioning and how this field frames a genuinely novel contribution.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>
<previous_paper>
STARTING POINT: This is your paper draft from the previous iteration.

# Introduction

Large language models (LLMs) can generate text using different decoding strategies, each with distinct characteristics. Greedy decoding selects the highest-probability token at each step, producing deterministic outputs that are often correct for straightforward tasks. Sampling decoding randomly selects from the probability distribution, introducing stochasticity that can help explore alternative reasoning paths for challenging problems. The choice between these strategies significantly impacts accuracy, yet current approaches use fixed strategies or complex adaptation methods that require reinforcement learning.

The core research question is: *Can we predict which decoding strategy will work better for a given prompt, and use this prediction to route each prompt to its optimal strategy?* If prompt embeddings contain information about which decoding strategy is likely to succeed, a simple classifier could learn this mapping and enable adaptive decoding without the complexity of reinforcement learning.

Current approaches to adaptive decoding have limitations. Reinforcement learning methods like Learning Adaptive LLM Decoding [1] train decoding adapters with verifiable rewards, but require online interaction and complex policy learning. Latent Preference Optimization [2] adds learnable layers to adjust sampling temperature, but still requires optimization of continuous parameters. Multi-agent methods like Collab [3] use multiple models with token-level switching, introducing substantial computational overhead. Attention-based heuristics like Mixture of Decoding [4] require access to internal model attention patterns.

We propose a radically simpler approach: precompute which decoding strategy works best for each prompt using ground truth labels, then train a tiny supervised classifier to predict this choice from the prompt embedding. This approach offers three advantages over prior work:

1. **Simplicity**: A logistic regression classifier with ~10k parameters replaces complex RL policies or attention mechanisms.
2. **No online interaction**: Oracle labels are precomputed offline, eliminating the need for live feedback during training.
3. **Interpretability**: The classifier provides a clear decision boundary based on prompt embeddings, revealing what features distinguish prompts that benefit from different strategies.

Our main contributions are:

- We demonstrate that prompt embeddings contain sufficient information to predict optimal decoding strategies with 96% accuracy, confirming the information-theoretic feasibility of the routing approach [ARTIFACT:art_yzGDa6VcOFHG].
- We provide a complete methodology for constructing oracle labels by running both greedy and sampling decoding strategies and verifying correctness programmatically [ARTIFACT:art_qYKiu0EeZ_7T].
- We release standardized datasets for routing experiments across four task types: math reasoning (GSM8K), science reasoning (ARC-Challenge), boolean questions (BoolQ), and multiple-choice questions (MMLU), totaling 18,771 examples [ARTIFACT:art_IJ_IrvobzhQ3].
- We analyze the conditions under which routing improves over single strategies, showing that effectiveness depends on the distribution of optimal strategies across prompts.

The remainder of this paper is organized as follows. Section 2 reviews related work on adaptive decoding and routing. Section 3 describes our methodology for oracle label construction and classifier training. Section 4 presents experimental results. Section 5 discusses limitations and future directions. Section 6 concludes.

[FIGURE:fig1]

# Related Work

## Adaptive Decoding Methods

Recent work has explored several approaches to adaptive decoding. Zhang et al. [1] formulate decoding as a contextual bandit problem and use reinforcement learning to train lightweight decoding adapters, achieving 10.2% Pass@1 improvement on MATH and CodeContests. Dhuliawala et al. [2] introduce Adaptive Decoding with Latent Preference Optimization, adding a learnable layer to dynamically select sampling temperature without requiring reward models. Chen et al. [4] propose Mixture of Decoding for vision-language models, using Jensen-Shannon divergence to measure consistency between outputs and select complementary decoding strategies. Chakraborty et al. [3] present Collab, which leverages multiple LLMs with token-level switching guided by a Q-function.

These methods share a common limitation: they require complex optimization (RL, preference learning, or attention analysis) and often need online interaction with the model. Our approach differs by using simple supervised learning on precomputed oracle labels, eliminating the need for RL or online adaptation.

## Model Routing in Multi-LLM Systems

The concept of routing prompts to appropriate models based on task characteristics has gained traction in multi-LLM systems. Prior work shows that simple classifiers can effectively route prompts to models of different capabilities based on estimated task difficulty or required expertise. We extend this routing paradigm to the single-model setting, where the decision is not which model to use but which decoding strategy to employ.

## Linear Probing and Prompt Embeddings

Linear probing literature demonstrates that prompt embeddings contain rich information about task type, difficulty, and required reasoning capabilities. Prior work shows that linear classifiers trained on embeddings can predict task category, estimate difficulty, and identify required knowledge domains. Our work builds on this foundation by showing that embeddings also contain information about optimal decoding strategy—a previously unexamined dimension of prompt characteristics.

# Methods

## Problem Formulation

Given a prompt $x$, we consider two decoding strategies: greedy decoding (temperature $T=0$) and sampling decoding (temperature $T=0.7$ with top-p=0.9). Let $y_{\text{greedy}}(x)$ and $y_{\text{sample}}(x)$ denote the outputs produced by each strategy, and let $c(x)$ be the ground truth answer. We define the optimal decoding strategy $s^*(x) \in \{\text{greedy}, \text{sampling}\}$ as:

$$s^*(x) = \begin{cases}
\text{greedy} & \text{if } y_{\text{greedy}}(x) = c(x) \text{ and } y_{\text{sample}}(x) \neq c(x) \\
\text{sampling} & \text{if } y_{\text{sample}}(x) = c(x) \text{ and } y_{\text{greedy}}(x) \neq c(x) \\
\text{greedy} & \text{if both correct (prefer simpler strategy)} \\
\text{exclude} & \text{if both incorrect}
\end{cases}$$

Our goal is to learn a classifier $f: \mathbb{R}^d \rightarrow \{\text{greedy}, \text{sampling}\}$ that predicts $s^*(x)$ from the prompt embedding $\phi(x) \in \mathbb{R}^d$, and to show that routing prompts according to $f(x)$ yields higher accuracy than using either strategy alone.

## Oracle Label Construction

We construct oracle labels by running both decoding strategies on each prompt and verifying correctness. For sampling decoding, we generate $k=3$ independent samples to account for stochasticity. Correctness verification uses task-specific methods:

- **Math problems (GSM8K)**: Extract numerical answers using regex patterns (e.g., `#### 8`) and compare with tolerance 0.01.
- **Multiple-choice (MMLU, ARC)**: Exact match with the correct option letter.
- **Boolean questions (BoolQ)**: Exact match with "yes" or "no".

If both strategies produce correct answers, we assign the greedy label (preferring simpler, deterministic decoding). If both produce incorrect answers, we exclude the prompt from training (the optimal strategy is ambiguous).

## Classifier Architecture

We use a simple logistic regression classifier trained on prompt embeddings extracted by a sentence transformer (all-MiniLM-L6-v2) [ARTIFACT:art_yzGDa6VcOFHG]. The classifier has 384 input features (embedding dimension) and 1 output (log-odds of sampling being better). We chose logistic regression for its interpretability and minimal computational requirements, though the approach generalizes to small MLPs.

## Routing Strategy

At inference time, for each prompt $x$:
1. Extract embedding $\phi(x)$ using the sentence transformer.
2. Predict $f(x) = \text{sampling}$ if $P(\text{sampling better} \mid \phi(x)) > 0.5$, else $\text{greedy}$.
3. Generate the answer using the predicted decoding strategy.

## Datasets

We use four datasets covering diverse task types [ARTIFACT:art_IJ_IrvobzhQ3]:

- **GSM8K** [5]: 7,473 grade school math word problems with step-by-step solutions.
- **ARC-Challenge** [6]: 1,119 science reasoning multiple-choice questions.
- **BoolQ** [7]: 9,427 boolean (yes/no) questions requiring reading comprehension.
- **MMLU** [8]: 752 multiple-choice questions across 57 subjects.

All datasets are standardized to a common schema with fields: `input` (prompt), `output` (correct answer), and `metadata`. Answers are automatically verifiable for all datasets.

[FIGURE:fig2]

# Experiments

## Experimental Setup

We conducted experiments using GPT-4o-mini via the OpenRouter API [ARTIFACT:art_yzGDa6VcOFHG]. For each prompt, we generated:
- 1 greedy decoding output (temperature=0.0, max_tokens=256)
- 3 sampling decoding outputs (temperature=0.7, top_p=0.9, max_tokens=256)

The experiment used 100 training prompts and 50 test prompts from a synthetic math word problem dataset (generated when GSM8K loading failed). We trained a logistic regression classifier on the training set and evaluated on the test set.

## Main Results

### Classifier Accuracy

The logistic regression classifier achieved **96% accuracy** in predicting which decoding strategy is optimal for held-out prompts. This result confirms that prompt embeddings contain sufficient information to distinguish prompts that benefit from greedy versus sampling decoding with high reliability.

### Routing Performance

Table 1 shows the accuracy of different strategies on the test set:

| Strategy | Accuracy |
|----------|----------|
| Greedy only | 0.50 |
| Sampling only | 0.54 |
| Router (predicted) | 0.54 |

The routing strategy did not outperform always using sampling decoding. Analysis of oracle labels revealed that sampling was the optimal strategy for 92 out of 100 training prompts (92%) and 45 out of 50 test prompts (90%). When one strategy is optimal for the vast majority of prompts, routing provides little benefit over simply using that strategy.

### Oracle Label Distribution

Figure 3 shows the distribution of optimal decoding strategies across prompts. The heavy skew toward sampling (91% of prompts) explains why routing failed to improve over always-sampling: the optimal decision for most prompts is already to use sampling.

[FIGURE:fig3]

## Analysis

### When Does Routing Help?

Our results suggest that routing provides the most benefit when the optimal decoding strategy is relatively balanced across prompts. In datasets where one strategy dominates (e.g., sampling better for 91% of math problems), simply using the dominant strategy approaches the optimal routing performance. Routing would provide larger gains in datasets with more balanced distributions, where different prompts genuinely benefit from different strategies.

### Error Analysis

The classifier achieved 96% accuracy, but the 4% error rate still impacts routing performance. Errors occur primarily on prompts where:
1. Both strategies produce correct answers (classifier must choose one arbitrarily).
2. Both strategies produce incorrect answers (optimal strategy is ambiguous).
3. Sampling outputs have high variance, making the "sampling better" label noisy.

### Computational Efficiency

The entire routing pipeline requires:
- Embedding extraction: ~10ms per prompt (all-MiniLM-L6-v2 on CPU)
- Classifier prediction: <1ms per prompt (logistic regression)
- Total overhead: ~11ms per prompt, compared to ~500-1000ms for LLM generation

This represents a <2% computational overhead, making the approach practical for real-time applications.

# Discussion

## Interpretation of Results

The high classifier accuracy (96%) demonstrates that prompt embeddings contain rich information about which decoding strategy will succeed. This is a significant finding: it confirms the information-theoretic feasibility of the routing approach and suggests that prompt characteristics (task type, complexity, ambiguity) manifest in embeddings in ways that correlate with optimal decoding strategy.

However, the failure of routing to improve over always-sampling highlights an important caveat: *predicting optimal strategy is not sufficient for routing to help; the optimal strategy must vary sufficiently across prompts*. In datasets where one strategy dominates, routing adds complexity without benefit.

## Comparison to Prior Work

Our approach differs from prior adaptive decoding methods in several key ways:

1. **Supervised vs. RL**: We use supervised learning with precomputed labels, while methods like [1] use reinforcement learning with online rewards.
2. **Binary vs. continuous**: We predict a binary choice (greedy vs. sampling), while methods like [2] adjust continuous temperature parameters.
3. **Prompt-level vs. token-level**: Our routing decision is made once per prompt, while methods like [3] switch strategies at each token.

These simplifications reduce computational overhead and eliminate the need for complex training procedures, at the cost of reduced flexibility (binary choice vs. continuous adjustment).

## Limitations

Several limitations constrain the generalizability of our findings:

1. **Dataset skew**: The heavy skew toward sampling in our dataset (91%) may not generalize to other tasks or models. Different models or datasets might show more balanced optimal strategy distributions.
2. **Synthetic data**: The experiment used synthetic math problems due to dataset loading issues. Results on standard benchmarks (GSM8K, MMLU) may differ.
3. **Single model**: We tested only GPT-4o-mini. Different models may have different relative performance of greedy vs. sampling, affecting the routing potential.
4. **Binary decision**: Restricting routing to binary greedy-vs-sampling may miss nuances. Some prompts might benefit from intermediate temperatures or more samples.
5. **Small scale**: The experiment used 150 prompts. Larger-scale evaluation is needed to confirm findings.

## Future Directions

Based on our findings, we identify several promising research directions:

- **Multi-dataset evaluation**: Test routing on datasets with more balanced optimal strategy distributions (e.g., mixing MMLU subjects or task types).
- **Temperature prediction**: Extend the binary classifier to predict optimal temperature values, combining the simplicity of supervised learning with the flexibility of continuous adjustment.
- **Ensemble routing**: Combine embedding-based routing with confidence-based heuristics (e.g., route based on both embedding and model confidence).
- **Theoretical analysis**: Investigate what prompt features (length, perplexity, task type) drive the classifier's predictions and why.

# Conclusion

We investigated whether a simple supervised classifier can learn to route prompts to their optimal decoding strategy (greedy or sampling) based on prompt embeddings. Our experiments show that logistic regression achieves 96% accuracy in predicting which strategy is better, confirming that prompt embeddings contain sufficient information for this decision. However, the routing strategy did not improve over always using sampling because sampling was optimal for 91% of prompts in our dataset.

These results make two key contributions: (1) they demonstrate the feasibility of learning routing decisions from prompt embeddings with minimal computational overhead, and (2) they reveal that routing effectiveness depends critically on the distribution of optimal strategies across prompts. Future work should evaluate routing on datasets with more balanced strategy distributions and explore extensions to continuous temperature prediction.

Our approach offers a path toward adaptive decoding that is orders of magnitude simpler than RL-based methods, requires no online interaction, and provides interpretable decisions. While routing may not help for all datasets, the ability to predict optimal decoding strategy with high accuracy opens new possibilities for efficient, adaptive LLM inference.

# References

[1] Zhang, S., Ye, Z., Tenka, S., Yang, A. Z. H., Kong, S., & Ghai, U. (2026). Learning Adaptive LLM Decoding. *arXiv preprint arXiv:2603.09065*.

[2] Dhuliawala, S., Kulikov, I., Yu, P., Celikyilmaz, A., Weston, J., Sukhbaatar, S., & Lanchantin, J. (2024). Adaptive Decoding via Latent Preference Optimization. *arXiv preprint arXiv:2411.09661*.

[3] Chakraborty, S., Bhatt, S., Sehwag, U. M., Ghosal, S. S., Qiu, J., Wang, M., Manocha, D., Huang, F., Koppel, A., & Ganesh, S. (2025). Collab: Controlled Decoding using Mixture of Agents for LLM Alignment. *International Conference on Learning Representations*.

[4] Chen, X., Zhang, Y., Liu, Q., Wu, J., Zhang, F., & Tan, T. (2025). Mixture of Decoding: An Attention-Inspired Adaptive Decoding Strategy to Mitigate Hallucinations in Large Vision-Language Models. *Findings of ACL*.

[5] Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano, R., Hesse, C., & Schulman, J. (2021). Training Verifiers to Solve Math Word Problems. *arXiv preprint arXiv:2110.14168*.

[6] Clark, C., Lee, K., Chang, M. W., Kwiatkowski, T., Collins, M., & Toutanova, K. (2019). BoolQ: Exploring the Surprising Difficulty of Natural Yes/No Questions. *North American Chapter of the Association for Computational Linguistics*.

[7] Hendrycks, D., Burns, C., Basart, S., Zou, A., Mazeika, M., Song, D., & Steinhardt, J. (2020). Measuring Massive Multitask Language Understanding. *International Conference on Learning Representations*.

[8] Clark, C., Lee, K., Chang, M. W., Kwiatkowski, T., Collins, M., & Toutanova, K. (2019). BoolQ: Exploring the Surprising Difficulty of Natural Yes/No Questions. *North American Chapter of the Association for Computational Linguistics*.

[9] Reimers, N., & Gurevych, I. (2019). Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks. *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing*.

</previous_paper>

<reviewer_feedback>
STEP 1 — REVIEW: A reviewer evaluated the previous paper draft above and produced this feedback.

- [MAJOR] (rigor) Major citation errors in References [6], [7], and [8]. Reference [6] attributes ARC-Challenge to Clark et al. 2019, but ARC is Clark et al. 2018 (arXiv:1803.05457). Reference [7] attributes BoolQ to Hendrycks et al. 2020, but BoolQ is Clark et al. 2019 (arXiv:1905.10044). Reference [8] attributes MMLU to Clark et al. 2019, but MMLU is Hendrycks et al. 2020 (arXiv:2009.03300). These are not minor errors—the authors and years are completely scrambled, suggesting insufficient verification of references.
  Action: Verify every reference against the original source. Correct [6] to: Clark et al., 'Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge,' arXiv:1803.05457, 2018. Correct [7] to: Clark et al., 'BoolQ: Exploring the Surprising Difficulty of Natural Yes/No Questions,' NAACL 2019, arXiv:1905.10044. Correct [8] to: Hendrycks et al., 'Measuring Massive Multitask Language Understanding,' ICLR 2021, arXiv:2009.03300. Additionally, reference [9] (Sentence-BERT) should cite Reimers & Gurevych 2019 at EMNLP, not just 'Proceedings of EMNLP' without page numbers.
- [MAJOR] (evidence) The experiment used only 150 synthetic prompts (100 train, 50 test) generated because 'GSM8K loading failed.' However, the paper claims to have collected 18,771 examples from standard datasets (GSM8K, ARC-Challenge, BoolQ, MMLU) and implies these were used in experiments. The abstract says 'totaling 18,771 examples' as if they were evaluated. This is a major discrepancy between claims and actual experiments.
  Action: Run the actual experiments on the collected datasets. The dataset artifact (art_IJ_IrvobzhQ3) shows 18,771 examples were collected—use them. Fix whatever dataset loading issue prevented using GSM8K. If there are persistent loading issues, use HuggingFace datasets library which has all these datasets readily available. The evaluation must be on standard benchmarks, not synthetic data, for the claims to be credible.
- [MAJOR] (evidence) The core experimental result is negative: routing does not improve over always using sampling (0.54 vs 0.54 accuracy). The 96% classifier accuracy is meaningless because it doesn't translate to performance gains. The paper attempts to spin this as a positive contribution ('we demonstrate feasibility...') but the actual routing provides zero benefit. A top-tier venue would expect demonstrated improvement, not just 'predictability.'
  Action: Either (1) find datasets/tasks where routing actually improves performance (the paper acknowledges this requires more balanced strategy distributions), or (2) reframe the paper as a negative result paper that provides insights about when routing can help. For option 1, mix datasets with different characteristics or evaluate on tasks where greedy is known to be better (e.g., some code generation tasks). For option 2, provide deeper analysis of what features make sampling better and develop practical guidelines.
- [MAJOR] (methodology) The evaluation is on a single model (GPT-4o-mini) with only 150 synthetic prompts. This is insufficient to support general claims about decoding strategy routing. Different models have very different behaviors for greedy vs. sampling—GPT-4o-mini may show different patterns than GPT-4, Claude, or open-source models. The strategy distribution skew (91% sampling-better) may be specific to this model and task.
  Action: Evaluate on at least 2-3 different models spanning different capability levels and architectures (e.g., GPT-4o, Claude Haiku, Llama-3-8B). Evaluate on the four collected datasets (GSM8K, ARC, BoolQ, MMLU) which cover diverse task types. Use at least 1000 training prompts and 500 test prompts. This is the minimum scale for a credible top-tier publication.
- [MINOR] (novelty) The idea of using classifiers for routing is not novel—the paper itself cites prior work on model routing. The extension to decoding strategies (rather than model selection) is incremental. The most novel aspect would be demonstrating that this actually works, but the paper fails to show improvement. The negative result (high predictability but no benefit under skew) is somewhat interesting but not sufficient for a top-tier publication without deeper analysis.
  Action: Strengthen the novelty by: (1) providing a theoretical analysis of when routing can help (relating to strategy distribution entropy), (2) analyzing what prompt features drive the classifier's decisions (feature importance analysis), (3) comparing embedding-based routing to other simple heuristics (e.g., route based on question type, length, or model confidence). This would provide more insight beyond 'we tried a classifier.'
- [MINOR] (methodology) The oracle label construction has a potential issue: when both strategies produce correct answers, the paper assigns 'greedy' arbitrarily. When both are incorrect, the prompt is excluded. This creates label noise and may bias the classifier. Additionally, only 3 samples are used for sampling decoding, which may not be sufficient to reliably determine if sampling 'works' (sampling has variance).
  Action: For prompts where both strategies are correct, include them with a label reflecting that either works (or exclude them consistently). For prompts where both are incorrect, consider whether a different strategy (e.g., higher temperature, more samples) might work rather than excluding. Increase samples for sampling to k=5 or use statistical methods to estimate the probability that sampling is better given observed samples.
- [MINOR] (methodology) The paper uses all-MiniLM-L6-v2 sentence embeddings rather than embeddings from the target model (GPT-4o-mini). This is suboptimal because the sentence transformer embeddings may not capture the same information that GPT-4o-mini 'sees' in prompts. The routing would be more accurate with embeddings from the actual model being routed.
  Action: Use embeddings from the target model (GPT-4o-mini) for routing. Extract embeddings from the model's input layer or use the last hidden state of a prompt token. If API constraints prevent this, at least discuss this limitation and test whether using the target model's embeddings improves routing accuracy. Compare sentence-transformer vs. target-model embeddings in an ablation.
- [MINOR] (clarity) The paper is misleading in its presentation. The abstract says 'Can we predict which decoding strategy will work better for a given prompt?' and implies success. The introduction says 'Our main contributions are...' listing 96% accuracy as if it's the main result. But the actual routing doesn't help. The writing should be more honest about the negative result.
  Action: Rewrite the abstract to clearly state: (1) we can predict optimal strategy with 96% accuracy, BUT (2) routing does not improve performance when one strategy dominates (91% sampling-better), and (3) routing may only help when strategies are more balanced. Currently the abstract implies routing is successful. Similarly, the introduction should frame this as an exploration with mixed results, not a successful demonstration.
- [MINOR] (scope) The paper only considers binary routing between greedy and sampling. Real-world adaptive decoding might benefit from more nuanced strategies: different temperatures, top-p values, or even number of samples. The binary restriction limits the impact.
  Action: Extend the approach to predict continuous temperature values or discrete temperature buckets (e.g., T=0, 0.3, 0.7, 1.0). This would increase the practical impact. The paper mentions this as 'future work' but it should be included to make the contribution substantial. Even a simple extension to 3-way classification (greedy, moderate sampling, high sampling) would strengthen the paper significantly.
</reviewer_feedback>

<pipeline_steps>
STEP 2 — STRATEGY: The pipeline's strategy generator (gen_strat) read the reviewer feedback
and designed a new research strategy to address the critiques.

STEP 3 — PLANNING: The planner (gen_plan) turned the strategy into concrete artifact plans —
specific experiments, datasets, or research tasks to execute.

STEP 4 — EXECUTION: The executor (gen_art) ran those plans and produced the new artifacts
shown in <new_artifacts_this_iteration> below.
</pipeline_steps>

<hypothesis>
STEP 5 — HYPOTHESIS UPDATE: The hypothesis was revised based on evidence from previous iterations.

kind: hypothesis
title: When can tiny routers improve decoding strategy selection?
hypothesis: >-
  Prompt embeddings contain sufficient information to predict whether greedy or sampling decoding will produce correct answers
  for a given prompt, but a learned router based on these embeddings only improves accuracy over single-strategy baselines
  when the optimal decoding strategy is reasonably balanced across prompts (neither strategy dominates for >70% of prompts).
  The conditions under which routing provides benefit depend on: (1) the distribution of optimal strategies across the dataset,
  (2) the model being routed, and (3) the task type. Current evidence shows high classifier accuracy (96%) is achievable,
  but routing provided no benefit on synthetic math problems where sampling was optimal for 91% of prompts.
motivation: >-
  Current approaches to adaptive decoding use reinforcement learning or complex policies that require online interaction with
  the model. We propose a simpler, more interpretable approach: precompute which decoding strategy works best for each prompt
  using ground truth labels, then train a tiny supervised classifier to predict this choice from the prompt embedding. This
  approach is orders of magnitude simpler than RL-based methods, requires no online interaction, and provides a clear information-theoretic
  justification: prompt embeddings contain sufficient information about task type to determine optimal decoding strategy.
assumptions:
- >-
  Prompt embeddings contain sufficient information to distinguish prompts that benefit from greedy vs sampling decoding
- >-
  The optimal decoding strategy for a prompt is consistent across multiple runs (i.e., greedy is reliably better for some
  prompts, sampling for others)
- >-
  A simple classifier (linear or small MLP) can capture the mapping from prompt embeddings to optimal decoding strategy
- >-
  Ground truth labels for 'which strategy works better' can be obtained by running both strategies and checking correctness
investigation_approach: >-
  1. Create a dataset of prompts with oracle labels: for each prompt, run both greedy and sampling decoding (multiple samples
  for sampling), determine which strategy produces the correct answer more often. 2. Extract prompt embeddings using a frozen
  LLM. 3. Train a simple binary classifier (logistic regression or 2-layer MLP) to predict 'greedy is better' vs 'sampling
  is better' from the prompt embedding. 4. Evaluate on held-out prompts: use the classifier to route each prompt to its predicted
  strategy, compare against always-greedy and always-sampling baselines. 5. Analyze what prompt features the classifier uses
  (task type, complexity, etc.).
success_criteria: >-
  The router-classified approach should achieve higher accuracy than the best single strategy (greedy or sampling) on held-out
  prompts. Specifically, if greedy achieves X% accuracy and sampling achieves Y% accuracy on a test set, the router should
  achieve > max(X, Y)% accuracy. Additionally, the router should outperform random routing (50/50 split between strategies)
  and simple heuristics (e.g., route based on prompt length or perplexity).
related_works:
- >-
  Learning Adaptive LLM Decoding (arXiv:2603.09065): Uses RL with verifiable rewards to learn adaptive decoding policies.
  Our approach differs by using supervised learning with precomputed oracle labels instead of RL, and using a much simpler
  classifier instead of a learned adapter.
- >-
  Adaptive Decoding via Latent Preference Optimization (arXiv:2411.09661): Uses latent preference optimization to learn temperature
  adaptation. Our approach differs by framing the problem as binary classification (greedy vs sampling) with supervised labels,
  not continuous temperature adjustment via LPO.
- >-
  Collab: Controlled Decoding using Mixture of Agents (arXiv:2503.21720): Uses multiple LLM agents with token-level switching.
  Our approach differs by using a single model with two decoding strategies and a simple prompt-level router, not multiple
  models.
- >-
  Mixture of Decoding (ACL 2025): Uses attention-based dynamic adaptation for vision-language models. Our approach differs
  by using supervised learning on prompt embeddings rather than attention-based heuristics, and focusing on the simpler binary
  greedy-vs-sampling decision.
inspiration: >-
  The hypothesis draws inspiration from three sources: (1) Model routing in multi-LLM systems, where simple classifiers route
  prompts to appropriate models based on task difficulty; (2) Minimum Description Length principle from information theory,
  which suggests that different tasks have different optimal compression strategies (analogous to decoding strategies); (3)
  Linear probing literature, which shows that prompt embeddings contain rich information about task type that can be extracted
  with simple classifiers.
terms:
- term: Decoding strategy
  definition: >-
    The algorithm used to select the next token when generating text from a language model, such as greedy decoding (always
    pick highest probability token) or sampling (randomly pick from top tokens).
- term: Prompt embedding
  definition: >-
    A vector representation of the input prompt produced by the language model, typically from the last hidden state or pooled
    output, that captures semantic information about the prompt.
- term: Oracle label
  definition: >-
    The ground truth label indicating which decoding strategy (greedy or sampling) produces the correct answer for a given
    prompt, determined by actually running both strategies and checking correctness.
- term: Router
  definition: >-
    A small model or classifier that decides which strategy or model to use for a given input, in this case choosing between
    greedy and sampling decoding.
- term: Greedy decoding
  definition: >-
    A deterministic decoding strategy that always selects the token with the highest probability at each step.
- term: Sampling decoding
  definition: >-
    A stochastic decoding strategy that randomly samples from the probability distribution over tokens (possibly truncated
    to top-k or top-p tokens).
summary: >-
  A simple supervised classifier can learn to predict whether greedy or sampling decoding will work better for a given prompt
  based on its embedding, and routing prompts to their predicted optimal strategy beats using either strategy alone.
_relation_rationale: >-
  Revised to acknowledge negative result and specify conditions for routing benefit
_confidence_delta: decreased
_key_changes:
- >-
  Added critical condition: routing only helps when strategies are balanced (<70% dominance)
- >-
  Changed from positive claim ('yields higher accuracy') to conditional claim ('only improves when...')
- 'Incorporated negative result: routing provided no benefit with 91% strategy skew'
- Added dependency on model, task type, and strategy distribution
- Reframed as investigating 'when' rather than demonstrating 'that' routing works
- >-
  Preserved core finding: embeddings can predict optimal strategy with high accuracy
relation_type: evolution
</hypothesis>

<all_artifacts>
FULL EVIDENCE BASE: All 5 research artifacts across all iterations.

--- Item 1 ---
id: art_qYKiu0EeZ_7T
type: research
title: Adaptive decoding methods and QA datasets for tiny router research
summary: >-
  This research provides a comprehensive survey of adaptive decoding methods, oracle label construction methodologies, and
  suitable QA datasets for investigating whether a tiny learned router can select between greedy and sampling decoding strategies
  per prompt. The research identified four main approaches in current literature: reinforcement learning-based methods (Learning
  Adaptive LLM Decoding), preference optimization (Adaptive Decoding via LPO), attention-based heuristics (Mixture of Decoding),
  and multi-agent methods (Collab). A detailed methodology for constructing oracle labels was developed, involving greedy
  decoding (temperature=0), sampling decoding (temperature=0.7, 5-10 samples), and correctness verification through exact
  match, programmatic verification, or majority voting. Three primary dataset recommendations were made: MMLU (multiple-choice,
  57 subjects, clear answers), GSM8K (math word problems, moderate difficulty), and MATH (competition-level math, challenging).
  Technical guidance on prompt embedding extraction using sentence transformers or same-model hidden states was provided,
  along with failure scenario analysis and experimental design recommendations. The findings directly inform the experimental
  design for testing the tiny router hypothesis by providing validated methodologies, dataset recommendations, and baseline
  comparisons.
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1
out_expected_files:
- research_out.json

--- Item 2 ---
id: art_IJ_IrvobzhQ3
type: dataset
title: QA datasets for routing experiments
summary: >-
  Successfully collected 4 primary datasets (GSM8K, ARC-Challenge, BoolQ, MMLU) with 18,771 total examples. All datasets are
  standardized to the exp_sel_data_out.json schema with fields: input (prompt), output (correct answer), and metadata fields.
  Datasets were verified to have >100 downloads, published papers, and proper provenance. The datasets cover diverse task
  types: math reasoning (GSM8K: 7,473 examples), science reasoning (ARC-Challenge: 1,119 examples), boolean questions (BoolQ:
  9,427 examples), and multiple-choice questions across subjects (MMLU: 752 examples). All answers are automatically verifiable.
  Output files include full dataset (13MB), mini version (3 examples per dataset), and preview version (truncated strings).
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_dataset_1
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json

--- Item 3 ---
id: art_yzGDa6VcOFHG
type: experiment
title: Test Tiny Router for Decoding Strategy
summary: >-
  Implemented a complete experiment to test if prompt embeddings can predict whether greedy or sampling decoding works better
  for math word problems. The experiment uses GPT-4o-mini via OpenRouter API to generate responses with both decoding strategies,
  then trains a logistic regression classifier on sentence embeddings to predict the optimal strategy. Results show the classifier
  achieves 88% accuracy in predicting which strategy is better, though the routing strategy did not outperform always using
  greedy decoding in this dataset due to sampling being better for 91% of prompts. The experiment includes full API integration
  with caching, retry logic, cost tracking (total $0.0093), and comprehensive logging. Synthetic math dataset was used as
  fallback when GSM8K loading failed.
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 4 ---
id: art_4Z4wnbjzo88i
type: experiment
title: Test when tiny routers improve decoding
summary: >-
  Successfully implemented and executed experiment to test if routing between greedy and sampling decoding based on prompt
  embeddings improves accuracy only when optimal strategies are balanced (30-70% distribution). The experiment used 4 QA datasets
  (GSM8K, ARC, BoolQ, MMLU) with 500 examples total (from cache). Results show that routing benefit is positive (0.020-0.110)
  only when sampling optimal rate is 30-70%, confirming the hypothesis. When sampling rate is outside this range, routing
  benefit is 0.000. The learned router achieved 64.6% accuracy with 3.8% improvement over best baseline. The experiment demonstrates
  that tiny learned routers can pick between decoding strategies, but they only provide value when strategies are balanced.
  Output files follow exp_gen_sol_out.json schema with datasets array at top level. All JSON files validated against schema
  successfully.
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_2/gen_art/gen_art_experiment_1
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json

--- Item 5 ---
id: art_zAyHjTm5opeN
type: research
title: Citation fixes and routing analysis for tiny router
summary: >-
  This research provides three main contributions: (1) Verified and corrected citations for ARC-Challenge (arXiv:1803.05457,
  2018), BoolQ (NAACL 2019, pp. 2924-2936), MMLU (ICLR 2021, arXiv:2009.03300), and Sentence-BERT (EMNLP-IJCNLP 2019, pp.
  3982-3992). (2) Identified prompt features that drive routing decisions including task type indicators (via linear probing
  on embeddings), complexity metrics (token length, perplexity, vocabulary diversity), and semantic clusters (via UMAP/t-SNE
  visualization). Recommends using SHAP values, LIME, or feature ablation for interpretability analysis. (3) Developed a theoretical
  framework for routing benefit conditions based on information theory (strategy distribution entropy), optimal decision boundary
  theory (Bayes classifier, class imbalance effects), and empirical evidence from RouteLLM and RouterBench. The framework
  shows routing provides benefit when strategy distribution is balanced (closer to 55-45 than 70-30), router accuracy exceeds
  majority-class baseline, decision boundaries are simple, and strategies have complementary strengths. The 70% balance threshold
  from the original hypothesis is evaluated and refined to 60-40 or 55-45 based on literature evidence showing greedy decoding
  outperforms sampling on 70-80% of standard benchmarks.
workspace_path: >-
  /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_2/gen_art/gen_art_research_1
out_expected_files:
- research_out.json
</all_artifacts>

<new_artifacts_this_iteration>
NEW THIS ITERATION: These 2 artifacts were created to address the reviewer
feedback. Their findings should be the primary basis for your revisions.

id: art_4Z4wnbjzo88i
type: experiment
title: Test when tiny routers improve decoding
summary: >-
  Successfully implemented and executed experiment to test if routing between greedy and sampling decoding based on prompt
  embeddings improves accuracy only when optimal strategies are balanced (30-70% distribution). The experiment used 4 QA datasets
  (GSM8K, ARC, BoolQ, MMLU) with 500 examples total (from cache). Results show that routing benefit is positive (0.020-0.110)
  only when sampling optimal rate is 30-70%, confirming the hypothesis. When sampling rate is outside this range, routing
  benefit is 0.000. The learned router achieved 64.6% accuracy with 3.8% improvement over best baseline. The experiment demonstrates
  that tiny learned routers can pick between decoding strategies, but they only provide value when strategies are balanced.
  Output files follow exp_gen_sol_out.json schema with datasets array at top level. All JSON files validated against schema
  successfully.

id: art_zAyHjTm5opeN
type: research
title: Citation fixes and routing analysis for tiny router
summary: >-
  This research provides three main contributions: (1) Verified and corrected citations for ARC-Challenge (arXiv:1803.05457,
  2018), BoolQ (NAACL 2019, pp. 2924-2936), MMLU (ICLR 2021, arXiv:2009.03300), and Sentence-BERT (EMNLP-IJCNLP 2019, pp.
  3982-3992). (2) Identified prompt features that drive routing decisions including task type indicators (via linear probing
  on embeddings), complexity metrics (token length, perplexity, vocabulary diversity), and semantic clusters (via UMAP/t-SNE
  visualization). Recommends using SHAP values, LIME, or feature ablation for interpretability analysis. (3) Developed a theoretical
  framework for routing benefit conditions based on information theory (strategy distribution entropy), optimal decision boundary
  theory (Bayes classifier, class imbalance effects), and empirical evidence from RouteLLM and RouterBench. The framework
  shows routing provides benefit when strategy distribution is balanced (closer to 55-45 than 70-30), router accuracy exceeds
  majority-class baseline, decision boundaries are simple, and strategies have complementary strengths. The 70% balance threshold
  from the original hypothesis is evaluated and refined to 60-40 or 55-45 based on literature evidence showing greedy decoding
  outperforms sampling on 70-80% of standard benchmarks.
</new_artifacts_this_iteration>

<data_files>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_files>

<task>
Write a research paper draft with LaTeX-ready text, BibTeX citations, and figure placeholders.

YOUR TURN (gen_paper_text): Revise the paper.

You are a researcher improving your paper after receiving a conference review.
Take the feedback seriously and make substantive changes, not cosmetic ones.

1. ADDRESS REVIEWER FEEDBACK: For each critique in <reviewer_feedback>, either fix the
   issue in the paper or argue convincingly why it doesn't apply. Major critiques MUST
   be resolved -- they would cause rejection if left unaddressed.
2. USE THE NEW EVIDENCE: The artifacts in <new_artifacts_this_iteration> were created
   specifically to address the reviewer's concerns. Reference their findings to
   strengthen the sections that were flagged as weak.
3. REWRITE, DON'T PATCH: Don't just append new paragraphs. Restructure and rewrite
   the sections the reviewer identified as problematic.
4. MAINTAIN CONSISTENCY: Ensure the paper aligns with the updated hypothesis.
</task>

<figure_instructions>
FIGURE FORMAT: Use [FIGURE:fig_id] markers in paper_text to indicate where each figure goes.
Then provide the full figure specs in the separate `figures` structured output array.
Each figure in the array must have an `id` matching a marker in the text. Set the `aspect_ratio`
field per figure: 21:9 for architecture / pipeline / flow-chart diagrams (the hero figure should
be one of these — place its marker near the END of the Introduction so it floats to the top of
page 2), 16:9 for comparisons / multi-panel results, 4:3 for dense charts, 1:1 for heatmaps /
confusion matrices / scatter plots.

Example in paper_text:
  "...our method achieves state-of-the-art results as shown below.\n\n[FIGURE:fig3]\n\nThe results demonstrate..."

Example in figures array (results comparison):
  {"id": "fig3", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: latency (seconds, 0-5). Values: PostgreSQL=4.6s (red), Bao=2.8s (blue), RLQOpt=2.0s (green). Error bars +/-0.3-0.8. Sans-serif font, white background.", "aspect_ratio": "16:9", "summary": "Compares latency across optimizers"}

Example in figures array (architecture diagram, hero):
  {"id": "fig1", "title": "System Architecture", "caption": "End-to-end pipeline: encoder feeds latents into the planner, which queries the value head before emitting actions.", "image_gen_detailed_description": "Horizontal flow diagram, left to right. Five labeled boxes: 'Input' (gray), 'Encoder' (blue), 'Latent (z, 256-dim)' (light blue, narrow), 'Planner' (green), 'Action Head' (orange). Arrows labeled with shapes. Value head as separate green box below 'Planner', bidirectional arrow. Sans-serif font, clean white background, no 3D.", "aspect_ratio": "21:9", "summary": "Hero architecture diagram"}

CRITICAL: Before writing figure specs, look through artifact workspace output files (*_out.json)
and code to find ALL the exact values. The figure generator cannot read files — every exact number
and value MUST be in the image_gen_detailed_description.
</figure_instructions>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-writing, aii-semscholar-bib.
TODO 2. LITERATURE REVIEW: Use web search tools to research the landscape — search key terms from
<hypothesis> and <all_artifacts>. Then use aii_semscholar_bib__fetch to batch-fetch real
BibTeX entries. Build a comprehensive Related Work section. Do NOT fabricate entries.
TODO 3. READ ARTIFACTS: Before writing each section, READ the relevant artifact source code, output
files, and data in the workspace. Extract concrete implementation details, technical innovations,
algorithmic specifics, and quantitative results. Do NOT write surface-level descriptions.

ARTIFACT REFERENCES: When you reference results, methodology, or findings from a specific artifact,
place an [ARTIFACT:artifact_id] marker inline. These become footnotes linking to the artifact's code
in the GitHub repository (first mention gets a footnote with URL, subsequent mentions are omitted).
Use the exact artifact ID from <all_artifacts>. Place the marker right after the claim it supports.
Example:
  "Our evaluation showed a 15% improvement over baselines [ARTIFACT:art_4f9d2c81ab37]." 
TODO 4. WRITE PAPER: Write the full paper text with [FIGURE:fig_id] markers per <figure_instructions>,
and provide the figure specs in the figures array. Cite with numeric references [1], [2], etc.
At the end of the paper text, include a full bibliography section. Do NOT compile LaTeX or generate
actual image/figure files. Your ONLY output is the structured JSON.
</todos><user_data>
User-provided reference materials are available at `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FigureSpec": {
      "description": "Figure specification \u2014 structured output from paper writing agent.\n\nThe LLM fills these as a list in PaperText.figures.\nLater converted to Figure objects for viz gen.",
      "properties": {
        "id": {
          "description": "Figure ID matching the [FIGURE:id] marker in paper_text (e.g., 'fig1')",
          "title": "Id",
          "type": "string"
        },
        "title": {
          "description": "Figure title in plain, everyday language \u2014 short and jargon-free. Aim for about 4-8 words (~40 characters).",
          "title": "Title",
          "type": "string"
        },
        "caption": {
          "description": "LaTeX figure caption \u2014 appears below the figure in the paper. Should describe what the figure shows and highlight key takeaways.",
          "title": "Caption",
          "type": "string"
        },
        "image_gen_detailed_description": {
          "description": "Detailed image generation prompt \u2014 axes, labels, ALL numeric values, colors, aspect ratio, layout. The image generator cannot read files; this is its ONLY input.",
          "title": "Image Gen Detailed Description",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this figure communicates",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "id",
        "title",
        "caption",
        "image_gen_detailed_description",
        "summary"
      ],
      "title": "FigureSpec",
      "type": "object"
    }
  },
  "description": "Paper text \u2014 structured output from paper writing agent.\n\nStructured output fields (LLMPrompt + LLMStructOut):\n- title, abstract, paper_text, figures, summary\n\npaper_text contains [FIGURE:fig_id] markers for positioning.\nfigures contains the full specs as structured objects.\n\nMetadata fields (plain, set by pipeline code):\n- id",
  "properties": {
    "title": {
      "description": "Paper title \u2014 clear, plain-language, and short so a non-expert understands the main contribution at a glance. Aim for about 6-10 words; avoid jargon and acronyms.",
      "title": "Title",
      "type": "string"
    },
    "abstract": {
      "description": "Paper abstract",
      "title": "Abstract",
      "type": "string"
    },
    "paper_text": {
      "description": "Full paper body text with markdown section headers (# Introduction, # Methods, # Results, # Discussion, # Conclusion). Use [FIGURE:fig_id] markers (e.g. [FIGURE:fig1]) to indicate where each figure should appear.",
      "title": "Paper Text",
      "type": "string"
    },
    "figures": {
      "description": "List of figure specifications. Each must have an id matching a [FIGURE:id] marker in paper_text.",
      "items": {
        "$ref": "#/$defs/FigureSpec"
      },
      "title": "Figures",
      "type": "array"
    },
    "summary": {
      "description": "Brief summary of the paper's main contribution and findings",
      "title": "Summary",
      "type": "string"
    }
  },
  "required": [
    "title",
    "abstract",
    "paper_text",
    "summary"
  ],
  "title": "PaperText",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_2/gen_paper_text/gen_paper_text/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-07-31 23:28:32 UTC

```
Can a tiny learned router pick between two decoding strategies per prompt to beat always using either one alone?
```

### [3] SKILL-INPUT — aii-paper-writing · 2026-07-31 23:28:52 UTC

The agent loaded the **aii-paper-writing** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-writing
description: Academic paper writing guidance for AI research. Covers paper structure, figure placeholders, bibliography building with Semantic Scholar, and citation rules. Does NOT cover LaTeX compilation or figure file generation — see aii-paper-to-latex for that.
---

## Technical Papers

Guidance for the standard "technical paper" format: propose a method/system/framework, evaluate it experimentally, report results. This is the main track at most CS venues (NeurIPS, ICML, ICLR, ACL, AAAI, etc.). Does NOT cover: pure theory/formal proofs, survey papers, position papers, or dataset/benchmark papers — those have different structures.

### Paper Structure

Target 6-8 pages. Use formal academic language, third person. Support claims with evidence from artifacts.

#### Rough Page Budget (8-page paper)

| Section | Pages | Notes |
|---|---|---|
| Abstract | 0.3 | Problem, approach, key result |
| Introduction | 1.0-1.5 | The most important section |
| Related Work | 0.5-1.0 | Beginning or end (see below) |
| Methods | 1.5-2.0 | Architecture fig on page 1 |
| Experiments | 1.5-2.0 | Setup + results + ablations |
| Discussion | 0.5-1.0 | Limitations go here |
| Conclusion | 0.3-0.5 | Do not repeat the abstract |
| References | 0.5-1.0 | Not counted in page limit |

**Critical rule**: A clear new technical contribution must be articulated by page 3 (quarter of the paper). If the reader doesn't know what you did by then, you've lost them.

#### Section Details

**Abstract** (150-250 words): State the problem, your approach, and the main results. Be factual and comprehensive. Do not repeat the abstract word-for-word later in the paper.

**Introduction** — Follow this 5-paragraph structure:

1. **What is the problem?** Define the task concretely.
2. **Why is it interesting and important?** Real-world impact, scale.
3. **Why is it hard?** Why do naive approaches fail?
4. **Why hasn't it been solved before?** What's wrong with prior solutions? How does yours differ?
5. **What are the key components of your approach and results?** Include specific limitations.

End with a "Summary of Contributions" subsection — bullet list of contributions with section references. This doubles as an outline, saving space.

**Related Work** — Placement decision:
- **Beginning** (Section 2): If it can be short yet detailed, or if you need a strong defensive stance against prior work early.
- **End** (before Conclusions): If comparisons require your technical content, or if it can be summarized briefly in the Introduction. Can be titled "Discussion and Related Work."

**Methods/Approach**: Every section tells a story — the story of the results, NOT the story of how you arrived at them. Use top-down description: readers should see where the material is going and be able to skip ahead. Move gory details to appendices.

**Experiments**: Setup (datasets, metrics, baselines) → main results → ablations → analysis. Every claim needs quantitative evidence.

**Discussion**: Interpret results, compare to prior work, state limitations honestly. Limitations should be specific and actionable, not vague disclaimers.

**Conclusion**: Short summarizing paragraph. Do NOT repeat material from the Abstract or Introduction. Make original claims more concrete (e.g., reference quantitative results). Include future work as bullet list — if actively pursuing follow-up, say so to mark territory.

#### Writing Quality Rules

- Define all notation/terminology before use, only once. Group global definitions in Preliminaries.
- Do NOT use nonreferential "this", "that", "these", "it". Always specify the referent. BAD: "This is important because..." GOOD: "This accuracy gap is important because..."
- Do NOT use "etc." unless remaining items are completely obvious. BAD: "We measure volatility, scalability, etc." GOOD: "We measure volatility and scalability."
- Do NOT write "for various reasons" — state the actual reasons.
- "That" is defining, "which" is nondefining. "The algorithms that are easy to implement" vs "The algorithms, which are easy to implement."
- Use italics for definitions and quotes, not for emphasis. Context alone should provide emphasis.

### Figure Format

Figures use a hybrid marker + structured array approach. ALL figures are generated by a separate pipeline step using an AI image model — your `image_gen_detailed_description` is the ONLY input that model sees. It cannot read files or access data. Do NOT generate actual image files yourself (no matplotlib, no PIL, no image generation scripts).

**In paper_text**: Place `[FIGURE:fig_id]` markers where figures should appear.

**In figures array**: Provide full specs as structured objects with these fields:
- `id` — matches the `[FIGURE:id]` marker in paper_text
- `title` — short descriptive title
- `caption` — LaTeX caption that appears below the figure in the paper
- `image_gen_detailed_description` — detailed prompt for the image generator (axes, ALL values, colors, layout)
- `summary` — brief summary of what the figure communicates

Example in paper_text:
```
...our method achieves state-of-the-art results as shown below.

[FIGURE:fig_1]

The results in Figure 1 demonstrate...
```

Example figure spec in figures array:
```json
{"id": "fig_1", "title": "Performance Comparison", "caption": "Comparison of geometric mean query latency across optimizers on JOB benchmark. RLQOpt achieves 2.3x speedup over PostgreSQL.", "image_gen_detailed_description": "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: ModelA=0.847, ModelB=0.762, Baseline=0.531. Error bars with std: 0.02, 0.03, 0.05. Sans-serif font, white background.", "summary": "Compares accuracy of proposed methods vs baseline."}
```

Every marker in text MUST have a matching figure in the array, and vice versa.

#### Data Precision Requirement

`image_gen_detailed_description` MUST include exact numbers from artifact output files. Read the actual output files before writing figure specs.

- BAD: "Compare accuracy metrics across configurations"
- GOOD: "Grouped bar chart. X-axis: model names. Y-axis: accuracy (0.0-1.0). Values: K=3: 0.765, K=5: 0.729, Baseline: 0.121."

#### Figure vs Table Decision

Do NOT create figures for tabular data (rows/columns of text or numbers). Use `\begin{table}` in LaTeX instead. Figures are for actual visualizations only (charts, plots, diagrams).

#### Figure Placement Strategy

Be intentional with figure ordering. The architectural/method overview figure explaining the proposed approach MUST appear early — in the Introduction or at the start of Methods — so readers can immediately orient themselves. Readers skim papers top-down; if the first figure they see is a results bar chart, they have no mental model for interpreting it.

Recommended ordering:
1. **Architecture/method diagram** — Introduction or early Methods (so readers understand the approach before diving into details)
2. **Conceptual/analogy figures** — Introduction or Methods (to build intuition)
3. **Results figures** (bar charts, line plots, scatter plots) — Results section
4. **Analysis/ablation figures** — Discussion or later Results

#### Guidelines

- Plan 3-6 figures total across the paper
- Place [FIGURE:fig_id] markers INLINE where referenced in text
- Include axes, labels, ALL numeric values in figure descriptions
- Both data-driven figures (bar charts, line plots) and conceptual diagrams (architecture, flowcharts)
- Be as detailed as possible in descriptions: specify aspect ratio, preferred colors, all data values, axis labels, ranges, legend entries, and any other visual details. The more specific the description, the better the generated figure

### Bibliography with Semantic Scholar

Build `./references.bib` using the aii-semscholar-bib skill (real BibTeX from Semantic Scholar):

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in one batch
3. Write the returned .bib text into `./references.bib`

Rules:
- Do NOT fabricate BibTeX entries — always fetch from Semantic Scholar
- If a paper isn't found (very recent preprint), write the entry manually as fallback
- Use `\bibliography{references}` and `\bibliographystyle{plainnat}`
- Do NOT use inline `thebibliography` environment

### Citation Format (for Research Artifacts)

When writing research with numbered citations:

1. Every factual claim MUST have a numbered citation: `[1]`, `[2]`, `[1, 3]`, etc.
2. Each source in the "sources" array MUST have an "index" field
3. The index MUST EXACTLY MATCH citation numbers in the text
4. NEVER cite a number without a matching source index
5. Example: "LLMs show 40% improvement with multi-agent collaboration [1]."
````

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-07-31 23:28:52 UTC

The agent loaded the **aii-semscholar-bib** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-semscholar-bib
description: Build bibliographies using Semantic Scholar. Batch-fetch BibTeX for papers by DOI, ArXiv ID, or title. Use when writing papers, generating reference lists, or building .bib files.
---

## Tool: `aii_semscholar_bib__fetch`

Batch-fetch BibTeX entries from Semantic Scholar. Pass all references in a single call — the tool handles batching internally.

### How it works

1. **DOI/ArXiv refs** → batched into POST /paper/batch calls (up to 500 per API call, auto-chunked)
2. **Title-only refs** → individual GET /paper/search/match (1s delay between)
3. **Post-process** → fix entry type, fix citation key (AuthorYYYY), inject DOI

The ability server runs a single worker (`max_threads: 1`). Multiple concurrent tool calls are queued — each runs independently (no cross-request aggregation). Batching happens within each request.

### Input format

```json
{
  "references": [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
    {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
    {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
  ]
}
```

Each reference object can have:
- `doi` — DOI string (ArXiv DOIs like `10.48550/arXiv.XXXX.XXXXX` auto-convert to ArXiv IDs)
- `arxiv` — ArXiv ID (e.g. `"2305.14325"`)
- `title` — Paper title (used for search/match when no DOI/ArXiv)
- `author` — First author last name (for cleaner citation key)
- `year` — Publication year (int, for citation key)

At least one of `doi`, `arxiv`, or `title` is required per reference.

### Output format

```json
{
  "success": true,
  "bib_text": "@inproceedings{Vaswani2017, ...}\n\n@article{Wei2022, ...}",
  "total": 3,
  "found": 3,
  "failed_count": 0,
  "entries": [{"citation_key": "Vaswani2017", "bibtex": "...", "title": "...", "doi": "...", "arxiv": ""}],
  "failed": []
}
```

### Workflow

1. Collect DOIs, ArXiv IDs, or titles for all papers you need to cite
2. Call `aii_semscholar_bib__fetch` with the full list in **one call**
3. Save `bib_text` from the response to your `references.bib` file
4. Check `failed` — for any missed papers, follow the **fallback procedure** below

### Fallback for failed references (MANDATORY)

NEVER fabricate BibTeX. For each failed reference:
1. **WebSearch** for `"Title" author year` (try `site:arxiv.org` too)
2. **WebFetch** the paper page → extract title, authors, year, venue, DOI/ArXiv ID
3. If DOI/ArXiv found → retry `aii_semscholar_bib__fetch` with it
4. Last resort: write BibTeX by hand using **only verified info from the actual paper page**

---

### CLI (for manual use / debugging)

```bash
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-semscholar-bib" && \
$SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_semscholar_bib__fetch.py --refs '[
  {"doi": "10.48550/arXiv.1706.03762", "author": "Vaswani", "year": 2017},
  {"arxiv": "2201.11903", "author": "Wei", "year": 2022},
  {"title": "Tree of Thoughts", "author": "Yao", "year": 2023}
]'
```

`--json, -j` — output raw JSON instead of .bib text

**If the script fails** with a connection error (ability server not running): create a local `.venv`, install server deps from `server_requirements.txt` into it, then import the `@aii_ability` function from the script and call it directly — bypassing the server:
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r "$SKILL_DIR/scripts/server_requirements.txt"
```
````

### [5] SKILL-INPUT — aii-web-tools · 2026-07-31 23:30:48 UTC

The agent loaded the **aii-web-tools** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-web-tools
description: "Web research toolkit: web search (Serper/Google), web page fetch as markdown (HTML and PDF), and regex grep over full page/PDF text. Use whenever a task needs to search the web, read a page, mine a paper/PDF, verify citations, or extract exact quotes, numbers, or methodology from a URL."
---

## Web tools

You have three web capabilities: **search**, **fetch**, and **grep** (exact
regex extraction over a full page or PDF).

**Pick where they come from, in this order:**

1. **If you have built-in `WebSearch` / `WebFetch` tools, PREFER those over the
   scripts below.** They may be **deferred tools** (listed by name but with
   schemas not yet loaded) — if so, call `ToolSearch("select:WebSearch,WebFetch")`
   ONCE to load them, then use them normally. Do not skip them just because they
   need that one extra load step; they are the preferred path. Pair them with the
   `aii_web_tools__fetch_grep` script below when you need exact text / numbers /
   methodology that a summary would miss, or when reading a PDF.
2. **Only if you have NO built-in `WebSearch` / `WebFetch`** (e.g. the OpenHands
   backend), use the scripts in this skill (below). They are our own
   implementations — Serper.dev for search, html2text + PyMuPDF for fetch, and
   regex grep over the full document text. They work without any built-in web
   tools.

Workflow either way: **search** (discover) → **fetch** (read for the gist) →
**grep** (pull exact details / read PDFs).

---

## Running the scripts

Run every script with the skill's pre-provisioned interpreter (it already has
`requests`, `html2text`, `pymupdf`, `python-dotenv`). Set `PY` once:

```bash
export SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-web-tools"
export PY="$SKILL_DIR/../.ability_client_venv/bin/python"
```

### 1. Search the web (Serper.dev / Google)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_search.py" --query "neuro-symbolic FOL translation LLM" --max-results 10
```

Returns ranked title / URL / snippet lines. Use it first to scan the
landscape; snippets are for discovery only — fetch a page before judging it.

### 2. Fetch a page as markdown (HTML or PDF)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" fetch --url "https://arxiv.org/abs/2303.11366" --max-chars 10000
```

`--max-chars` caps output (default 10000); `--char-offset N` pages further in.
Handles PDFs transparently via PyMuPDF.

### 3. Grep a page or PDF (exact regex extraction)

```bash
$PY "$SKILL_DIR/scripts/aii_fast_web_fetch.py" grep --url "https://arxiv.org/pdf/2303.11366" --pattern "verbal reinforcement" --max-matches 20 --context-chars 200
```

Returns only the matching sections with surrounding context — the right tool
for exact numbers, table values, methodology, or long PDFs where a summary
would lose the detail. `-i` for case-insensitive.

**Parallelize** independent searches/fetches in one turn; only sequence a
fetch after the search that produced its URL.

---

## Notes

- The scripts call our ability server. If a script prints
  `Ability service not available`, the server is down — say so rather than
  silently improvising a different search method.
- Do **not** hand-roll your own `requests`/scraping for search when these
  tools are available: Serper returns clean Google results and the fetch/grep
  scripts already handle HTML, PDFs, and encoding.
````
