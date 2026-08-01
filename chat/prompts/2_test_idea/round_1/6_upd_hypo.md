# upd_hypo — test_idea

> Phase: `invention_loop` · round 1 · `upd_hypo`
> Run: `run_C4UvEedrrr_P` — When Do Tiny Learned Routers Improve Decoding Strategy Selection?
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `upd_hypo` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-07-31 22:25:44 UTC

````
<current_hypothesis>
The hypothesis as it stands. Revise it based on the evidence below.

kind: hypothesis
title: Tiny Router Picks Greedy or Sampling
hypothesis: >-
  A simple supervised classifier trained on prompt embeddings can learn to predict whether greedy or sampling decoding will
  produce the correct answer for a given prompt, and using this classifier to route each prompt to its predicted optimal strategy
  yields higher accuracy than using either strategy alone.
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
</current_hypothesis>

<all_artifacts>
Complete set of research artifacts across all iterations.

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
</all_artifacts>

<new_artifacts_this_iteration>
These 3 artifacts were created THIS iteration.

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
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

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

</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

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



<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the field's landscape, prior work, crowded lanes, and the novelty bar — consult it while revising so the updated hypothesis stays genuinely novel and well-positioned.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<task>
IMPORTANT: Your ONLY output is the revised hypothesis text. Do NOT run code, produce artifacts,
fix bugs, or attempt to address the evidence yourself — the next iteration of the invention loop
will generate fresh artifacts based on your revised hypothesis. Reflect and rewrite; nothing else.

Do NOT generate a completely new hypothesis. Take the current hypothesis and REVISE it
to incorporate new evidence. Keep the core idea — refine, narrow, or strengthen it.

1. Does the evidence support the hypothesis? Narrow or broaden scope as needed.
2. Which claims now have strong evidence? Which are still unsupported?
3. Should the hypothesis become more specific based on what we've learned?
4. If reviewer feedback is provided, address the critiques directly.

STABILITY IS OK: If progress is good and evidence supports the current direction, keep the
hypothesis similar or identical. Only make substantive changes when evidence clearly calls for
them — e.g., contradictory results, fundamental reviewer critiques, or findings that refine scope.

You must also classify two kinds of edges in the research trace:

(A) The H↔H edge — how does this revised hypothesis relate to the previous one?
    Set `relation_type` (Moulines's structuralist typology) to one of:
    - "evolution": refining specialised claims, same conceptual frame
    - "embedding": previous hypothesis is now a special case of a broader frame
    - "replacement": rejecting the previous frame entirely (Kuhnian shift)
    Set `relation_rationale` to a brief justification (≤120 chars).

(B) The A↔A edges — for each artifact created THIS iteration, classify each of its
    `in_dependencies` (predecessor → dependent) using MultiCite's citation-function
    typology (Lauscher et al., NAACL 2022) — emit one entry in `artifact_relations`
    per (predecessor, dependent) pair. Predecessors are ALWAYS artifacts from EARLIER
    iterations — artifacts within one iteration run in parallel and cannot depend on
    each other, so never emit a relation between two same-iteration artifacts (it
    will be dropped):
    - "background": predecessor is treated as background context
    - "motivation": predecessor motivated this artifact's research
    - "uses": this artifact uses the predecessor's data, method, or output
    - "extends": this artifact extends the predecessor
    - "similarities": this artifact's results agree with the predecessor's
    - "differences": this artifact's results disagree with the predecessor's
    Each `relation_rationale` must be ≤120 characters.

Output the COMPLETE revised hypothesis (with the H↔H relation fields) AND the full
list of A↔A `artifact_relations` for this iteration's new artifacts.
</task><user_data>
User-provided reference materials are available at `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/upd_hypo/upd_hypo/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ArtifactRelation": {
      "description": "One typed A\u2194A edge between a dependent artifact and one of its in_dependencies.\n\nMultiCite citation-function typology (Lauscher et al., NAACL 2022),\nreduced to 6 plain-English types.",
      "properties": {
        "from_id": {
          "description": "ID of the predecessor artifact (the one being depended on)",
          "title": "From Id",
          "type": "string"
        },
        "to_id": {
          "description": "ID of the dependent artifact (the new artifact this iteration)",
          "title": "To Id",
          "type": "string"
        },
        "relation_type": {
          "description": "MultiCite citation-function type for the predecessor\u2192dependent edge: 'background' \u2014 predecessor is treated as background context; 'motivation' \u2014 predecessor motivated this artifact's research; 'uses' \u2014 this artifact uses the predecessor's data, method, or output; 'extends' \u2014 this artifact extends the predecessor; 'similarities' \u2014 this artifact's results agree with the predecessor's; 'differences' \u2014 this artifact's results disagree with the predecessor's.",
          "enum": [
            "background",
            "motivation",
            "uses",
            "extends",
            "similarities",
            "differences"
          ],
          "title": "Relation Type",
          "type": "string"
        },
        "relation_rationale": {
          "description": "Brief rationale for this relation type (one short line, max 120 characters).",
          "maxLength": 120,
          "title": "Relation Rationale",
          "type": "string"
        }
      },
      "required": [
        "from_id",
        "to_id",
        "relation_type",
        "relation_rationale"
      ],
      "title": "ArtifactRelation",
      "type": "object"
    }
  },
  "description": "Revised hypothesis after reviewing iteration results.\n\nOutput matches the hypothesis dict structure so it can replace the\noriginal hypothesis in subsequent iterations.",
  "properties": {
    "title": {
      "description": "Revised hypothesis title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); may be unchanged if still accurate.",
      "title": "Title",
      "type": "string"
    },
    "hypothesis": {
      "description": "Revised hypothesis statement \u2014 what we now believe based on evidence",
      "title": "Hypothesis",
      "type": "string"
    },
    "relation_rationale": {
      "description": "Brief rationale for the H\u2194H revision type (one short line, max 120 characters).",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    },
    "confidence_delta": {
      "description": "How confidence changed: 'increased', 'decreased', or 'unchanged'",
      "title": "Confidence Delta",
      "type": "string"
    },
    "key_changes": {
      "description": "Bullet list of specific changes made to the hypothesis",
      "items": {
        "type": "string"
      },
      "title": "Key Changes",
      "type": "array"
    },
    "relation_type": {
      "description": "Moulines's structuralist typology of this hypothesis revision: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (incommensurable, Kuhnian revolution).",
      "enum": [
        "evolution",
        "embedding",
        "replacement"
      ],
      "title": "Relation Type",
      "type": "string"
    },
    "artifact_relations": {
      "description": "Typed A\u2194A edges for this iteration's new artifacts. Emit one entry per (predecessor \u2192 dependent) edge for every in_dependency on each artifact produced this iteration.",
      "items": {
        "$ref": "#/$defs/ArtifactRelation"
      },
      "title": "Artifact Relations",
      "type": "array"
    }
  },
  "required": [
    "title",
    "hypothesis",
    "relation_rationale",
    "confidence_delta",
    "key_changes",
    "relation_type"
  ],
  "title": "RevisedHypothesis",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/upd_hypo/upd_hypo/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-07-31 22:25:44 UTC

```
Can a tiny learned router pick between two decoding strategies per prompt to beat always using either one alone?
```

### [3] SYSTEM-USER prompt · 2026-07-31 22:36:13 UTC

```
Your last response did not include a function call or a message. Please use a tool to proceed with the task.
```
