# upd_hypo — test_idea

> Phase: `invention_loop` · round 2 · `upd_hypo`
> Run: `run_C4UvEedrrr_P` — When Do Tiny Learned Routers Improve Decoding Strategy Selection?
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `upd_hypo` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-07-31 23:39:38 UTC

````
<current_hypothesis>
The hypothesis as it stands. Revise it based on the evidence below.

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

--- Item 4 ---
id: art_4Z4wnbjzo88i
type: experiment
in_dependencies:
- id: art_IJ_IrvobzhQ3
  label: dataset
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
in_dependencies:
- id: art_qYKiu0EeZ_7T
  label: prior research
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
These 2 artifacts were created THIS iteration.

id: art_4Z4wnbjzo88i
type: experiment
in_dependencies:
- id: art_IJ_IrvobzhQ3
  label: dataset
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

id: art_zAyHjTm5opeN
type: research
in_dependencies:
- id: art_qYKiu0EeZ_7T
  label: prior research
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
</new_artifacts_this_iteration>

<current_paper>
The paper draft from this iteration — represents the current state of the research story.

# When Do Tiny Learned Routers Improve Decoding Strategy Selection?

## Abstract

Large language models (LLMs) can use different decoding strategies—greedy decoding (deterministic) or sampling (stochastic)—each with distinct performance characteristics across prompts. Prior work on adaptive decoding uses reinforcement learning or complex policies requiring online interaction. We investigate whether a simple supervised classifier can learn to route prompts to their optimal decoding strategy based on prompt embeddings, and critically, under what conditions this routing improves accuracy. 

We conducted experiments on 500 prompts from four QA datasets (GSM8K, ARC-Challenge, BoolQ, MMLU) using GPT-4o-mini. A logistic regression classifier achieved 58.7% accuracy in predicting whether greedy or sampling decoding would produce correct answers. However, routing provided only 2.2% improvement over the best single strategy (62.4% vs 64.6% accuracy), and only when the optimal decoding strategy was reasonably balanced across prompts (sampling optimal for 30-70% of prompts). When one strategy dominated (>70% optimal rate), routing provided no benefit over simply using that strategy.

Our findings demonstrate that (1) prompt embeddings contain information about optimal decoding strategy, but (2) routing only improves accuracy when strategies are balanced, with maximum benefit when the optimal strategy distribution approaches 50-50. We provide a theoretical framework showing routing benefit depends on strategy distribution entropy and router accuracy exceeding the majority-class baseline. These results clarify the conditions under which learned routing can—and cannot—improve decoding.

## Introduction

Large language models (LLMs) generate text using decoding strategies that determine how tokens are selected at each step. Greedy decoding selects the highest-probability token, producing deterministic outputs suitable for fact retrieval and straightforward questions. Sampling decoding randomly selects from the probability distribution (temperature > 0), introducing stochasticity that can help explore alternative reasoning paths for challenging problems [1, 2]. The choice between these strategies significantly impacts accuracy, yet current approaches to adaptive decoding use fixed strategies or complex adaptation methods requiring reinforcement learning [3, 4, 5].

A natural question arises: *Can we predict which decoding strategy will work better for a given prompt, and use this prediction to route each prompt to its optimal strategy?* If prompt embeddings contain information about which decoding strategy is likely to succeed, a simple classifier could learn this mapping and enable adaptive decoding without the complexity of reinforcement learning.

Prior work on model routing shows that simple classifiers can effectively route prompts to models of different capabilities based on task characteristics [6, 7]. We extend this routing paradigm to the single-model setting, where the decision is not which model to use but which decoding strategy to employ. This approach offers potential advantages: simplicity (a logistic regression classifier with ~10k parameters replaces complex RL policies), no online interaction (oracle labels are precomputed offline), and interpretability (the classifier reveals what features distinguish prompts that benefit from different strategies).

However, a critical question remains: *When does routing between decoding strategies actually improve accuracy over using a single strategy?* Intuition suggests routing only helps when different prompts genuinely benefit from different strategies—that is, when the optimal decoding strategy is reasonably balanced across prompts rather than dominated by one strategy.

We test this hypothesis through experiments on four QA datasets using GPT-4o-mini [ARTIFACT:art_4Z4wnbjzo88i]. Our contributions are:

1. **Empirical evaluation of routing benefit**: We show that routing improves accuracy by 2.2% over the best single strategy (64.6% vs 62.4%), but *only* when the optimal decoding strategy is balanced (sampling optimal for 30-70% of prompts). When sampling dominates (>70% optimal), routing provides no benefit.

2. **Theoretical framework**: We develop an information-theoretic framework showing routing benefit depends on (a) strategy distribution entropy, (b) router accuracy exceeding the majority-class baseline, and (c) strategy complementarity [ARTIFACT:art_zAyHjTm5opeN].

3. **Verified methodology**: We provide a complete methodology for constructing oracle labels by running both decoding strategies and verifying correctness programmatically, totaling 500 examples across GSM8K [8], ARC-Challenge [9], BoolQ [10], and MMLU [11].

4. **Negative result with conditions**: We honestly report that routing does *not* help when one strategy dominates (80-92% sampling optimal in our datasets), providing clarity on when routing is worthwhile.

The remainder of this paper is organized as follows. Section 2 reviews related work on adaptive decoding and routing. Section 3 describes our methodology for oracle label construction and classifier training. Section 4 presents experimental results, including the conditional nature of routing benefit. Section 5 analyzes when routing helps and why. Section 6 discusses limitations and future directions. Section 7 concludes.

[FIGURE:fig1]

## Related Work

### Adaptive Decoding Methods

Recent work has explored several approaches to adaptive decoding. Zhang et al. [3] formulate decoding as a contextual bandit problem and use reinforcement learning to train lightweight decoding adapters, achieving 10.2% Pass@1 improvement on MATH and CodeContests. Dhuliawala et al. [4] introduce Adaptive Decoding with Latent Preference Optimization, adding a learnable layer to dynamically select sampling temperature without requiring reward models. Chen et al. [12] propose Mixture of Decoding for vision-language models, using Jensen-Shannon divergence to measure consistency between outputs and select complementary decoding strategies. Chakraborty et al. [5] present Collab, which leverages multiple LLMs with token-level switching guided by a Q-function.

These methods share a common limitation: they require complex optimization (RL, preference learning, or attention analysis) and often need online interaction with the model. Our approach differs by using simple supervised learning on precomputed oracle labels, eliminating the need for RL or online adaptation. However, our results show that even simple routing only helps under specific conditions.

### Model Routing in Multi-LLM Systems

The concept of routing prompts to appropriate models based on task characteristics has gained traction in multi-LLM systems. RouteLLM [6] demonstrates routing between strong and weak LLMs reduces cost by 2x without quality loss when routers achieve >80% accuracy. RouterBench [7] provides a comprehensive benchmark showing routing benefits require >15% accuracy improvement over baselines. Prior work shows simple classifiers can effectively route prompts to models of different capabilities based on estimated task difficulty or required expertise [13].

We extend this routing paradigm to the single-model setting, where the decision is not which model to use but which decoding strategy to employ. Our work is the first to identify the critical condition: routing only helps when strategies are balanced across prompts.

### Linear Probing and Prompt Embeddings

Linear probing literature demonstrates that prompt embeddings contain rich information about task type, difficulty, and required reasoning capabilities [14, 15]. Prior work shows linear classifiers trained on embeddings can predict task category, estimate difficulty, and identify required knowledge domains. Our work builds on this foundation by showing that embeddings also contain information about optimal decoding strategy—a previously unexamined dimension of prompt characteristics.

## Methods

### Problem Formulation

Given a prompt $x$, we consider two decoding strategies: greedy decoding (temperature $T=0$) and sampling decoding (temperature $T=0.7$ with top-p=0.9). Let $y_{\text{greedy}}(x)$ and $y_{\text{sample}}(x)$ denote the outputs produced by each strategy, and let $c(x)$ be the ground truth answer. We define the optimal decoding strategy $s^*(x) \in \{\text{greedy}, \text{sampling}\}$ as:

$$s^*(x) = \begin{cases}
\text{greedy} & \text{if } y_{\text{greedy}}(x) = c(x) \text{ and } y_{\text{sample}}(x) \neq c(x) \\
\text{sampling} & \text{if } y_{\text{sample}}(x) = c(x) \text{ and } y_{\text{greedy}}(x) \neq c(x) \\
\text{greedy} & \text{if both correct (prefer simpler strategy)} \\
\text{exclude} & \text{if both incorrect}
\end{cases}$$

Our goal is to learn a classifier $f: \mathbb{R}^d \rightarrow \{\text{greedy}, \text{sampling}\}$ that predicts $s^*(x)$ from the prompt embedding $\phi(x) \in \mathbb{R}^d$, and to show that routing prompts according to $f(x)$ yields higher accuracy than using either strategy alone—*but only when the optimal strategy distribution is balanced*.

### Oracle Label Construction

We construct oracle labels by running both decoding strategies on each prompt and verifying correctness. For sampling decoding, we generate $k=1$ sample (reduced from $k=3$ in pilot experiments for computational efficiency; see Section 5.3 for discussion of this choice). Correctness verification uses task-specific methods:

- **Math problems (GSM8K)**: Extract numerical answers using regex patterns (e.g., `#### 8`) and compare with tolerance 0.01.
- **Multiple-choice (MMLU, ARC)**: Exact match with the correct option letter.
- **Boolean questions (BoolQ)**: Exact match with "yes" or "no".

If both strategies produce correct answers, we assign the greedy label (preferring simpler, deterministic decoding). If both produce incorrect answers, we exclude the prompt from training (the optimal strategy is ambiguous) [ARTIFACT:art_4Z4wnbjzo88i].

### Classifier Architecture

We use a logistic regression classifier trained on prompt embeddings extracted by a sentence transformer (all-MiniLM-L6-v2) [16]. The classifier has 384 input features (embedding dimension) and 1 output (log-odds of sampling being better). We chose logistic regression for its interpretability and minimal computational requirements, though the approach generalizes to small MLPs.

### Routing Strategy

At inference time, for each prompt $x$:
1. Extract embedding $\phi(x)$ using the sentence transformer.
2. Predict $f(x) = \text{sampling}$ if $P(\text{sampling better} \mid \phi(x)) > 0.5$, else $\text{greedy}$.
3. Generate the answer using the predicted decoding strategy.

### Theoretical Framework for Routing Benefit

Based on information theory and empirical evidence, we derive conditions under which routing provides benefit [ARTIFACT:art_zAyHjTm5opeN].

Let $p$ = probability that greedy is optimal for a random prompt. The strategy distribution entropy is $H(p) = -p\log(p) - (1-p)\log(1-p)$. Routing has maximum potential benefit when $H(p)$ is maximized (i.e., $p \approx 0.5$). When $p > 0.7$ or $p < 0.3$, routing benefit diminishes as one strategy dominates.

Formally, routing improves over always-greedy when:
$$P(\text{greedy correct} \mid \text{greedy optimal}) \cdot p + P(\text{sampling correct} \mid \text{sampling optimal}) \cdot (1-p) > \max(P(\text{greedy correct}), P(\text{sampling correct}))$$

This requires the router accuracy to exceed the majority-class baseline (e.g., 70% if 70% of prompts are sampling-optimal).

### Datasets

We use four datasets covering diverse task types [ARTIFACT:art_IJ_IrvobzhQ3], [ARTIFACT:art_4Z4wnbjzo88i]:

- **GSM8K** [8]: 125 grade school math word problems with step-by-step solutions (80% sampling optimal in our experiments).
- **ARC-Challenge** [9]: 125 science reasoning multiple-choice questions (92% sampling optimal).
- **BoolQ** [10]: 125 boolean (yes/no) questions requiring reading comprehension (88% sampling optimal).
- **MMLU** [11]: 125 multiple-choice questions across 57 subjects (84% sampling optimal).

All datasets are standardized to a common schema with fields: `input` (prompt), `output` (correct answer), and `metadata`. Answers are automatically verifiable for all datasets.

[FIGURE:fig2]

## Experiments

### Experimental Setup

We conducted experiments using GPT-4o-mini via the OpenRouter API [ARTIFACT:art_4Z4wnbjzo88i]. For each prompt, we generated:
- 1 greedy decoding output (temperature=0.0, max_tokens=512)
- 1 sampling decoding output (temperature=0.7, top_p=0.9, max_tokens=512)

The experiment used 125 examples from each of the 4 datasets (500 total). We trained a logistic regression classifier on 70% of the data and evaluated on the held-out 30%.

### Main Results

#### Baseline Accuracies

Table 1 shows the accuracy of different strategies across the combined dataset:

| Strategy | Accuracy |
|----------|----------|
| Always greedy | 0.564 |
| Always sampling | 0.624 |
| Random routing (50/50) | 0.594 |
| Oracle routing (upper bound) | 0.624 |

Sampling decoding outperforms greedy decoding by 6.0% (62.4% vs 56.4%), consistent with recent findings that sampling helps on reasoning tasks [1, 2].

#### Router Performance

The logistic regression classifier achieved **58.7% accuracy** in predicting which decoding strategy is optimal for held-out prompts. This is only slightly above the majority-class baseline of 58.0% (sampling optimal rate across all datasets), indicating limited predictive power.

The routing strategy achieved **64.6% accuracy**, providing a **2.2% improvement** over always using sampling (62.4% vs 64.6%). However, this improvement is modest and comes with an important caveat: routing only helps because our dataset combines tasks with different optimal strategy rates.

#### Conditional Routing Benefit

Figure 3 shows routing benefit as a function of sampling optimal rate. When sampling is optimal for 80-92% of prompts (individual datasets), routing provides **0% improvement** over always using sampling. When we create mixed datasets with 30-70% sampling optimal, routing provides 2.2-11.0% improvement [ARTIFACT:art_4Z4wnbjzo88i].

These results confirm our hypothesis: *routing only improves accuracy when the optimal decoding strategy is balanced across prompts (30-70% range), not when one strategy dominates.*

[FIGURE:fig3]

### Analysis

#### Strategy Distribution Across Datasets

Table 2 shows the optimal strategy distribution across datasets:

| Dataset | Sampling Optimal Rate | Greedy Optimal Rate | Routing Benefit |
|---------|----------------------|---------------------|-----------------|
| GSM8K | 80% | 20% | 0.0% |
| ARC-Challenge | 92% | 8% | 0.0% |
| BoolQ | 88% | 12% | 0.0% |
| MMLU | 84% | 16% | 0.0% |
| Mixed (all) | 58% | 42% | 2.2% |

Sampling is the dominant strategy across all datasets, with 80-92% optimal rate. This explains why routing provides no benefit on individual datasets: the optimal decision for most prompts is already to use sampling.

#### Why Does Sampling Dominate?

Recent work by Song et al. [1] shows greedy decoding generally outperforms sampling on most tasks, but our results show the opposite. This discrepancy may be due to:

1. **Model-specific behavior**: GPT-4o-mini may have different relative performance of greedy vs. sampling compared to models tested in prior work.
2. **Task composition**: Our datasets focus on reasoning tasks (math, science, reading comprehension) where sampling is known to help [2].
3. **Temperature choice**: We used temperature=0.7 for sampling; lower temperatures might make sampling more similar to greedy.

#### Error Analysis

The classifier achieved 58.7% accuracy, only 0.7% above the majority-class baseline. Errors occur primarily on prompts where:
1. Both strategies produce correct answers (classifier must choose one arbitrarily).
2. Both strategies produce incorrect answers (optimal strategy is ambiguous).
3. The prompt embedding does not clearly encode which strategy will succeed.

#### Computational Efficiency

The entire routing pipeline requires:
- Embedding extraction: ~10ms per prompt (all-MiniLM-L6-v2 on CPU)
- Classifier prediction: <1ms per prompt (logistic regression)
- Total overhead: ~11ms per prompt, compared to ~500-1000ms for LLM generation

This represents a <2% computational overhead, making the approach practical for real-time applications—*if* routing provides benefit.

## Discussion

### When Does Routing Help?

Our results provide clear evidence for the conditional nature of routing benefit. Routing only improves accuracy when:

1. **Strategies are balanced**: The optimal decoding strategy must be reasonably balanced across prompts (30-70% range). When one strategy dominates (>70%), simply using that strategy approaches optimal routing performance.

2. **Router accuracy exceeds majority baseline**: The classifier must predict better than always choosing the majority class. With 80% sampling optimal, the classifier needs >80% accuracy to help; our classifier achieved only 58.7%.

3. **Strategies are complementary**: There must exist prompts where greedy wins and prompts where sampling wins. If both strategies succeed or fail together, routing cannot help.

These findings refine the 70% balance threshold from our original hypothesis to 60-40 or 55-45 based on empirical evidence from RouteLLM and RouterBench [6, 7].

### Comparison to Prior Work

Our approach differs from prior adaptive decoding methods in several key ways:

1. **Supervised vs. RL**: We use supervised learning with precomputed labels, while methods like [3] use reinforcement learning with online rewards.
2. **Binary vs. continuous**: We predict a binary choice (greedy vs. sampling), while methods like [4] adjust continuous temperature parameters.
3. **Prompt-level vs. token-level**: Our routing decision is made once per prompt, while methods like [5] switch strategies at each token.

However, our results show that even this simpler approach only helps under specific conditions, suggesting the core challenge is not method complexity but strategy complementarity.

### Limitations

Several limitations constrain the generalizability of our findings:

1. **Single model**: We tested only GPT-4o-mini. Different models may have different relative performance of greedy vs. sampling, affecting the routing potential.
2. **Binary decision**: Restricting routing to binary greedy-vs-sampling may miss nuances. Some prompts might benefit from intermediate temperatures or more samples.
3. **Limited sampling**: Using only $k=1$ sample for sampling decoding may not reliably determine if sampling "works." Prior work suggests $k \geq 3$ samples [2].
4. **Dataset skew**: All our datasets show sampling dominance (80-92% optimal rate). Different task compositions might yield more balanced distributions.
5. **Small scale**: The experiment used 500 prompts. Larger-scale evaluation is needed to confirm findings.

### Practical Guidelines

Based on our findings, we provide practical guidelines for when to use decoding strategy routing:

- **Use routing if**: Your dataset/task mix has 30-70% greedy-optimal prompts (balanced strategies).
- **Skip routing if**: One strategy dominates (>70% optimal). Simply use that strategy.
- **Check balance first**: Run both strategies on a pilot set of 100 prompts to measure the optimal strategy distribution before investing in routing.
- **Consider alternatives**: If strategies are imbalanced, consider (a) using the dominant strategy, (b) adjusting temperature continuously rather than binary routing, or (c) mixing task types to create balance.

## Conclusion

We investigated whether a simple supervised classifier can learn to route prompts to their optimal decoding strategy (greedy or sampling) based on prompt embeddings. Our experiments on 500 prompts from four QA datasets show that while logistic regression achieves 58.7% accuracy in predicting which strategy is better, routing only improves accuracy by 2.2% over always using sampling—and *only* when the optimal decoding strategy is balanced across prompts (30-70% sampling optimal).

These results make three key contributions: (1) they demonstrate the feasibility of learning routing decisions from prompt embeddings with minimal computational overhead, (2) they reveal that routing effectiveness depends critically on the distribution of optimal strategies across prompts, and (3) they provide a theoretical framework and practical guidelines for when routing can—and cannot—improve decoding.

Our findings clarify a key misconception in the literature: predicting optimal strategy is not sufficient for routing to help; the optimal strategy must vary sufficiently across prompts. Future work should evaluate routing on tasks with naturally balanced strategy distributions, explore extensions to continuous temperature prediction, and test whether these findings generalize to other models and decoding strategies.

## References

[1] Song, Y., Meng, Y., Tan, M., and Peng, N. "The Good, The Bad, and The Greedy: Evaluation of LLMs Should Not Ignore Non-Determinism." arXiv preprint arXiv:2407.10457, 2024.

[2] Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A., and Zhou, D. "Self-Consistency Improves Language Models as Mathematical Reasoners." EMNLP 2022.

[3] Zhang, S., Ye, Z., Tenka, S., Yang, A. Z. H., Kong, S., and Ghai, U. "Learning Adaptive LLM Decoding." arXiv preprint arXiv:2603.09065, 2026.

[4] Dhuliawala, S., Kulikov, I., Yu, P., Celikyilmaz, A., Weston, J., Sukhbaatar, S., and Lanchantin, J. "Adaptive Decoding via Latent Preference Optimization." arXiv preprint arXiv:2411.09661, 2024.

[5] Chakraborty, S., Bhatt, S., Sehwag, U. M., Ghosal, S. S., Qiu, J., Wang, M., Manocha, D., Huang, F., Koppel, A., and Ganesh, S. "Collab: Controlled Decoding using Mixture of Agents for LLM Alignment." ICLR 2025.

[6] Ong, I., Almahairi, A., Wu, V., Chiang, W.-L., Wu, T., Gonzalez, J. E., Kadous, W., and Stoica, I. "RouteLLM: Learning to Route LLMs with Preference Data." arXiv preprint arXiv:2406.18665, 2024.

[7] Hu, Q., Lu, G., Zhang, P., Li, S., and Zhang, Y. "RouterBench: A Benchmark for Multi-LLM Routing System." arXiv preprint arXiv:2403.12031, 2024.

[8] Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert, M., Tworek, J., Hilton, J., Nakano, R., Hesse, C., and Schulman, J. "Training Verifiers to Solve Math Word Problems." arXiv preprint arXiv:2110.14168, 2021.

[9] Clark, P., Cowhey, I., Etzioni, O., Khot, T., Sabharwal, A., Schoenick, C., and Tafjord, O. "Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge." arXiv preprint arXiv:1803.05457, 2018.

[10] Clark, C., Lee, K., Chang, M.-W., Kwiatkowski, T., Collins, M., and Toutanova, K. "BoolQ: Exploring the Surprising Difficulty of Natural Yes/No Questions." NAACL 2019, pp. 2924-2936.

[11] Hendrycks, D., Burns, C., Basart, S., Zou, A., Mazeika, M., Song, D., and Steinhardt, J. "Measuring Massive Multitask Language Understanding." ICLR 2021.

[12] Chen, X., Zhang, Y., Liu, Q., Wu, J., Zhang, F., and Tan, T. "Mixture of Decoding: An Attention-Inspired Adaptive Decoding Strategy to Mitigate Hallucinations in Large Vision-Language Models." ACL Findings 2025.

[13] Lu, J., Li, C., Yan, H., Zhang, X., and Li, L. "Routing to the Right Model: A Learning-Based Approach." arXiv preprint arXiv:2402.05845, 2024.

[14] Belinkov, Y. and Glass, J. "Analysis Methods in Neural Language Processing: A Survey." TACL 2019.

[15] Tenney, I., Das, D., and Pavlick, E. "BERT Rediscovers the Classical NLP Pipeline." NAACL 2019.

[16] Reimers, N. and Gurevych, I. "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks." EMNLP-IJCNLP 2019, pp. 3982-3992.
</current_paper>

<reviewer_feedback>
Feedback from the paper reviewer this iteration.

- [MAJOR] (evidence) CRITICAL DISCREPANCY: The paper claims individual dataset sampling optimal rates of 80-92% (GSM8K: 80%, ARC: 92%, BoolQ: 88%, MMLU: 84%), but the actual experimental data in full_method_out.json shows rates of 58-66% (GSM8K: 63.2%, ARC: 58.4%, BoolQ: 66.4%, MMLU: 61.6%). This is a major discrepancy that undermines the paper's central thesis about when routing helps. The paper's claim that routing doesn't help on individual datasets because 'sampling dominates (80-92% optimal rate)' is not supported by the actual data, which shows much more balanced rates (58-66%).
  Action: Re-run the analysis or explain the discrepancy. If the experimental data is correct, update the paper to report actual rates (58-66% not 80-92%). This will change the paper's narrative: with 58-66% rates, routing SHOULD help on individual datasets according to the paper's own hypothesis (30-70% is the helpful range). The paper must reconcile this. Either (1) the experiment code has a bug in computing optimal rates, (2) the paper incorrectly reports the results, or (3) the hypothesis needs refinement.
- [MAJOR] (evidence) The experimental output (full_method_out.json) has 'hypothesis_supported': false, but the paper claims the hypothesis IS supported ('routing only helps when 30-70% balanced'). This is a direct contradiction between the paper and its own experimental results. The paper states 'These results confirm our hypothesis' but the experiment code output says hypothesis_supported: false.
  Action: Fix the experiment code to correctly compute whether the hypothesis is supported, or update the paper to accurately reflect that the hypothesis is not supported by the data. The hypothesis testing logic in the code (test_conditional_hypothesis function) should be verified.
- [MAJOR] (methodology) The paper uses only k=1 sample for sampling decoding ('sampling_num_samples: 1' in experiment config), which is insufficient to reliably determine if sampling 'works.' Prior work (Wang et al. 2022, Self-Consistency) suggests using k≥3 samples. With only 1 sample, the sampling output may be unlucky, leading to incorrect oracle labels. This creates noise in the training data and may explain why the classifier accuracy is low (58.7%).
  Action: Re-run experiments with k≥3 samples for sampling decoding. Use majority voting or statistical methods to determine if sampling is 'better' given multiple samples. This will produce more reliable oracle labels and likely improve classifier performance. The research artifact from iter_1 used 5-10 samples - the reduction to 1 sample for 'computational efficiency' sacrifices scientific rigor.
- [MINOR] (novelty) The idea of using classifiers for routing is not novel - the paper itself cites RouteLLM and RouterBench which use classifiers to route between models. The extension to decoding strategies (rather than model selection) is incremental. The paper acknowledges this but doesn't adequately differentiate its contribution from prior routing work.
  Action: Strengthen the novelty by: (1) providing a theoretical analysis of why routing between decoding strategies is different from routing between models (e.g., strategies have correlated performance, while models have complementary capabilities), (2) analyzing what prompt features drive routing decisions (the research artifact mentions SHAP values and feature importance but this is not in the paper), (3) comparing embedding-based routing to heuristic routing baselines.
- [MINOR] (evidence) The routing benefit is modest: 2.2% improvement over always using sampling (64.6% vs 62.4%). With classifier accuracy of only 58.7% (0.7% above majority baseline), the routing is barely better than random. The paper acknowledges this but doesn't explore why the classifier performs so poorly or how to improve it.
  Action: Analyze why the classifier accuracy is low. Possible reasons: (1) sentence embeddings don't capture the right information - try using embeddings from the target model (GPT-4o-mini), (2) logistic regression is too simple - try MLPs or random forests, (3) the oracle labels are noisy (see k=1 sampling issue above). Ablate these factors to understand what limits routing performance.
- [MINOR] (methodology) The paper uses all-MiniLM-L6-v2 sentence embeddings rather than embeddings from the target model (GPT-4o-mini). The sentence transformer embeddings may not capture the same information that GPT-4o-mini 'sees' in prompts. The routing would likely be more accurate with embeddings from the actual model being routed.
  Action: Use embeddings from the target model (GPT-4o-mini) for routing, if API constraints allow. If not, at least discuss this limitation and test whether using the target model's embeddings improves routing accuracy. Compare sentence-transformer vs target-model embeddings in an ablation study.
- [MINOR] (scope) The paper only considers binary routing between greedy and sampling. Real-world adaptive decoding might benefit from more nuanced strategies: different temperatures, top-p values, or number of samples. The binary restriction limits the impact. The paper mentions this as 'future work' but it should be included to make the contribution substantial.
  Action: Extend the approach to predict continuous temperature values or discrete temperature buckets (e.g., T=0, 0.3, 0.7, 1.0). Even a simple extension to 3-way classification (greedy, moderate sampling, high sampling) would strengthen the paper. The method generalizes easily to multi-class classification.
- [MINOR] (rigor) The paper evaluates on a single model (GPT-4o-mini). Different models have very different behaviors for greedy vs sampling. The strategy distribution skew may be specific to this model. The paper should test generalizability across models.
  Action: Evaluate on at least 2-3 different models spanning different capability levels and architectures (e.g., GPT-4o, Claude Haiku, Llama-3-8B). This is important because the greedy-vs-sampling tradeoff is model-dependent. If routing only works for GPT-4o-mini, the contribution is limited.
- [MINOR] (clarity) The paper's title asks 'When Do Tiny Learned Routers Improve Decoding Strategy Selection?' but the answer is somewhat circular: 'routing improves when strategies are balanced.' This is intuitive - if one strategy is always better, routing can't help. The paper would be stronger if it provided a priori features to predict balance (e.g., task type, difficulty) rather than discovering balance empirically.
  Action: Provide practical guidelines for predicting strategy balance a priori. For example: 'Math reasoning tasks tend to have more balanced greedy/sampling optimal rates than factual QA tasks.' This would make the paper more useful for practitioners who want to decide whether to invest in routing before running experiments.
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

Output the result as JSON to: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_2/upd_hypo/upd_hypo/.sdk_openhands_agent_struct_out.json`

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

IMPORTANT: this task is NOT complete until `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_2/upd_hypo/upd_hypo/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-07-31 23:39:38 UTC

```
Can a tiny learned router pick between two decoding strategies per prompt to beat always using either one alone?
```

### [3] SYSTEM-USER prompt · 2026-07-31 23:40:34 UTC

```
<validation-feedback>
Attempt 1 failed validation.

The file `.sdk_openhands_agent_struct_out.json` does not contain valid JSON: Expecting value: line 3 column 17 (char 91). Rewrite the entire file with well-formed JSON.

Produce `.sdk_openhands_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```

### [4] SYSTEM-USER prompt · 2026-07-31 23:42:10 UTC

```
<validation-feedback>
Attempt 2 failed validation.

Schema validation found 1 problem — fix ALL of them at once:
  - at `relation_rationale`: 'Refined based on reviewer feedback: acknowledged methodological flaws, narrowed balance range, emphasized need for reliable labels' is too long (at most 120 characters, got 130)
Every required field must be present and every field type must match the schema.

Produce `.sdk_openhands_agent_struct_out.json` again so it contains corrected JSON that matches the schema. Do not invent new fields.
</validation-feedback>
```
