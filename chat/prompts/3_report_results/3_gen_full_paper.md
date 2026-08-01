# gen_full_paper — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `run_C4UvEedrrr_P` — When Do Tiny Learned Routers Improve Decoding Strategy Selection?
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_full_paper` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-08-01 00:16:37 UTC

````
<workspace>
Your workspace: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/4_gen_paper_repo/_4_assemble_paper/paper/workspace`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/4_gen_paper_repo/_4_assemble_paper/paper/workspace/`:
GOOD: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/4_gen_paper_repo/_4_assemble_paper/paper/workspace/file.py`, `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/4_gen_paper_repo/_4_assemble_paper/paper/workspace/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>

<task>
Create a publication-ready top-conference LaTeX paper with BibTeX from <paper_text> and <available_figures>, compile to PDF.
</task>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<paper_text>
title: When Do Tiny Learned Routers Improve Decoding Strategy Selection?
abstract: >-
  Large language models (LLMs) can use different decoding strategies—greedy decoding (deterministic) or sampling (stochastic)—each
  with distinct performance characteristics across prompts. Prior work on adaptive decoding uses reinforcement learning or
  complex policies requiring online interaction. We investigate whether a simple supervised classifier can learn to route
  prompts to their optimal decoding strategy based on prompt embeddings, and critically, under what conditions this routing
  improves accuracy. We conducted experiments on 500 prompts from four QA datasets (GSM8K, ARC-Challenge, BoolQ, MMLU) using
  GPT-4o-mini. A logistic regression classifier achieved 58.7% accuracy in predicting whether greedy or sampling decoding
  would produce correct answers. However, routing provided only 2.2% improvement over the best single strategy (62.4% vs 64.6%
  accuracy), and only when the optimal decoding strategy was reasonably balanced across prompts (sampling optimal for 30-70%
  of prompts). When one strategy dominated (>70% optimal rate), routing provided no benefit over simply using that strategy.
  Our findings demonstrate that (1) prompt embeddings contain information about optimal decoding strategy, but (2) routing
  only improves accuracy when strategies are balanced, with maximum benefit when the optimal strategy distribution approaches
  50-50. We provide a theoretical framework showing routing benefit depends on strategy distribution entropy and router accuracy
  exceeding the majority-class baseline. These results clarify the conditions under which learned routing can—and cannot—improve
  decoding.
paper_text: "# When Do Tiny Learned Routers Improve Decoding Strategy Selection?\n\n## Abstract\n\nLarge language models (LLMs)\
  \ can use different decoding strategies—greedy decoding (deterministic) or sampling (stochastic)—each with distinct performance\
  \ characteristics across prompts. Prior work on adaptive decoding uses reinforcement learning or complex policies requiring\
  \ online interaction. We investigate whether a simple supervised classifier can learn to route prompts to their optimal\
  \ decoding strategy based on prompt embeddings, and critically, under what conditions this routing improves accuracy. \n\
  \nWe conducted experiments on 500 prompts from four QA datasets (GSM8K, ARC-Challenge, BoolQ, MMLU) using GPT-4o-mini. A\
  \ logistic regression classifier achieved 58.7% accuracy in predicting whether greedy or sampling decoding would produce\
  \ correct answers. However, routing provided only 2.2% improvement over the best single strategy (62.4% vs 64.6% accuracy),\
  \ and only when the optimal decoding strategy was reasonably balanced across prompts (sampling optimal for 30-70% of prompts).\
  \ When one strategy dominated (>70% optimal rate), routing provided no benefit over simply using that strategy.\n\nOur findings\
  \ demonstrate that (1) prompt embeddings contain information about optimal decoding strategy, but (2) routing only improves\
  \ accuracy when strategies are balanced, with maximum benefit when the optimal strategy distribution approaches 50-50. We\
  \ provide a theoretical framework showing routing benefit depends on strategy distribution entropy and router accuracy exceeding\
  \ the majority-class baseline. These results clarify the conditions under which learned routing can—and cannot—improve decoding.\n\
  \n## Introduction\n\nLarge language models (LLMs) generate text using decoding strategies that determine how tokens are\
  \ selected at each step. Greedy decoding selects the highest-probability token, producing deterministic outputs suitable\
  \ for fact retrieval and straightforward questions. Sampling decoding randomly selects from the probability distribution\
  \ (temperature > 0), introducing stochasticity that can help explore alternative reasoning paths for challenging problems\
  \ [1, 2]. The choice between these strategies significantly impacts accuracy, yet current approaches to adaptive decoding\
  \ use fixed strategies or complex adaptation methods requiring reinforcement learning [3, 4, 5].\n\nA natural question arises:\
  \ *Can we predict which decoding strategy will work better for a given prompt, and use this prediction to route each prompt\
  \ to its optimal strategy?* If prompt embeddings contain information about which decoding strategy is likely to succeed,\
  \ a simple classifier could learn this mapping and enable adaptive decoding without the complexity of reinforcement learning.\n\
  \nPrior work on model routing shows that simple classifiers can effectively route prompts to models of different capabilities\
  \ based on task characteristics [6, 7]. We extend this routing paradigm to the single-model setting, where the decision\
  \ is not which model to use but which decoding strategy to employ. This approach offers potential advantages: simplicity\
  \ (a logistic regression classifier with ~10k parameters replaces complex RL policies), no online interaction (oracle labels\
  \ are precomputed offline), and interpretability (the classifier reveals what features distinguish prompts that benefit\
  \ from different strategies).\n\nHowever, a critical question remains: *When does routing between decoding strategies actually\
  \ improve accuracy over using a single strategy?* Intuition suggests routing only helps when different prompts genuinely\
  \ benefit from different strategies—that is, when the optimal decoding strategy is reasonably balanced across prompts rather\
  \ than dominated by one strategy.\n\nWe test this hypothesis through experiments on four QA datasets using GPT-4o-mini \\\
  footnote{Code: \\url{https://github.com/AMGrobelnik/ai-invention-073c82-when-do-tiny-learned-routers-improve-dec/tree/main/round-2/experiment-1}}.\
  \ Our contributions are:\n\n1. **Empirical evaluation of routing benefit**: We show that routing improves accuracy by 2.2%\
  \ over the best single strategy (64.6% vs 62.4%), but *only* when the optimal decoding strategy is balanced (sampling optimal\
  \ for 30-70% of prompts). When sampling dominates (>70% optimal), routing provides no benefit.\n\n2. **Theoretical framework**:\
  \ We develop an information-theoretic framework showing routing benefit depends on (a) strategy distribution entropy, (b)\
  \ router accuracy exceeding the majority-class baseline, and (c) strategy complementarity \\footnote{Code: \\url{https://github.com/AMGrobelnik/ai-invention-073c82-when-do-tiny-learned-routers-improve-dec/tree/main/round-2/research-1}}.\n\
  \n3. **Verified methodology**: We provide a complete methodology for constructing oracle labels by running both decoding\
  \ strategies and verifying correctness programmatically, totaling 500 examples across GSM8K [8], ARC-Challenge [9], BoolQ\
  \ [10], and MMLU [11].\n\n4. **Negative result with conditions**: We honestly report that routing does *not* help when one\
  \ strategy dominates (80-92% sampling optimal in our datasets), providing clarity on when routing is worthwhile.\n\nThe\
  \ remainder of this paper is organized as follows. Section 2 reviews related work on adaptive decoding and routing. Section\
  \ 3 describes our methodology for oracle label construction and classifier training. Section 4 presents experimental results,\
  \ including the conditional nature of routing benefit. Section 5 analyzes when routing helps and why. Section 6 discusses\
  \ limitations and future directions. Section 7 concludes.\n\n[FIGURE:fig1]\n\n## Related Work\n\n### Adaptive Decoding Methods\n\
  \nRecent work has explored several approaches to adaptive decoding. Zhang et al. [3] formulate decoding as a contextual\
  \ bandit problem and use reinforcement learning to train lightweight decoding adapters, achieving 10.2% Pass@1 improvement\
  \ on MATH and CodeContests. Dhuliawala et al. [4] introduce Adaptive Decoding with Latent Preference Optimization, adding\
  \ a learnable layer to dynamically select sampling temperature without requiring reward models. Chen et al. [12] propose\
  \ Mixture of Decoding for vision-language models, using Jensen-Shannon divergence to measure consistency between outputs\
  \ and select complementary decoding strategies. Chakraborty et al. [5] present Collab, which leverages multiple LLMs with\
  \ token-level switching guided by a Q-function.\n\nThese methods share a common limitation: they require complex optimization\
  \ (RL, preference learning, or attention analysis) and often need online interaction with the model. Our approach differs\
  \ by using simple supervised learning on precomputed oracle labels, eliminating the need for RL or online adaptation. However,\
  \ our results show that even simple routing only helps under specific conditions.\n\n### Model Routing in Multi-LLM Systems\n\
  \nThe concept of routing prompts to appropriate models based on task characteristics has gained traction in multi-LLM systems.\
  \ RouteLLM [6] demonstrates routing between strong and weak LLMs reduces cost by 2x without quality loss when routers achieve\
  \ >80% accuracy. RouterBench [7] provides a comprehensive benchmark showing routing benefits require >15% accuracy improvement\
  \ over baselines. Prior work shows simple classifiers can effectively route prompts to models of different capabilities\
  \ based on estimated task difficulty or required expertise [13].\n\nWe extend this routing paradigm to the single-model\
  \ setting, where the decision is not which model to use but which decoding strategy to employ. Our work is the first to\
  \ identify the critical condition: routing only helps when strategies are balanced across prompts.\n\n### Linear Probing\
  \ and Prompt Embeddings\n\nLinear probing literature demonstrates that prompt embeddings contain rich information about\
  \ task type, difficulty, and required reasoning capabilities [14, 15]. Prior work shows linear classifiers trained on embeddings\
  \ can predict task category, estimate difficulty, and identify required knowledge domains. Our work builds on this foundation\
  \ by showing that embeddings also contain information about optimal decoding strategy—a previously unexamined dimension\
  \ of prompt characteristics.\n\n## Methods\n\n### Problem Formulation\n\nGiven a prompt $x$, we consider two decoding strategies:\
  \ greedy decoding (temperature $T=0$) and sampling decoding (temperature $T=0.7$ with top-p=0.9). Let $y_{\\text{greedy}}(x)$\
  \ and $y_{\\text{sample}}(x)$ denote the outputs produced by each strategy, and let $c(x)$ be the ground truth answer. We\
  \ define the optimal decoding strategy $s^*(x) \\in \\{\\text{greedy}, \\text{sampling}\\}$ as:\n\n$$s^*(x) = \\begin{cases}\n\
  \\text{greedy} & \\text{if } y_{\\text{greedy}}(x) = c(x) \\text{ and } y_{\\text{sample}}(x) \\neq c(x) \\\\\n\\text{sampling}\
  \ & \\text{if } y_{\\text{sample}}(x) = c(x) \\text{ and } y_{\\text{greedy}}(x) \\neq c(x) \\\\\n\\text{greedy} & \\text{if\
  \ both correct (prefer simpler strategy)} \\\\\n\\text{exclude} & \\text{if both incorrect}\n\\end{cases}$$\n\nOur goal\
  \ is to learn a classifier $f: \\mathbb{R}^d \\rightarrow \\{\\text{greedy}, \\text{sampling}\\}$ that predicts $s^*(x)$\
  \ from the prompt embedding $\\phi(x) \\in \\mathbb{R}^d$, and to show that routing prompts according to $f(x)$ yields higher\
  \ accuracy than using either strategy alone—*but only when the optimal strategy distribution is balanced*.\n\n### Oracle\
  \ Label Construction\n\nWe construct oracle labels by running both decoding strategies on each prompt and verifying correctness.\
  \ For sampling decoding, we generate $k=1$ sample (reduced from $k=3$ in pilot experiments for computational efficiency;\
  \ see Section 5.3 for discussion of this choice). Correctness verification uses task-specific methods:\n\n- **Math problems\
  \ (GSM8K)**: Extract numerical answers using regex patterns (e.g., `#### 8`) and compare with tolerance 0.01.\n- **Multiple-choice\
  \ (MMLU, ARC)**: Exact match with the correct option letter.\n- **Boolean questions (BoolQ)**: Exact match with \"yes\"\
  \ or \"no\".\n\nIf both strategies produce correct answers, we assign the greedy label (preferring simpler, deterministic\
  \ decoding). If both produce incorrect answers, we exclude the prompt from training (the optimal strategy is ambiguous)\
  \ .\n\n### Classifier Architecture\n\nWe use a logistic regression classifier trained on prompt embeddings extracted by\
  \ a sentence transformer (all-MiniLM-L6-v2) [16]. The classifier has 384 input features (embedding dimension) and 1 output\
  \ (log-odds of sampling being better). We chose logistic regression for its interpretability and minimal computational requirements,\
  \ though the approach generalizes to small MLPs.\n\n### Routing Strategy\n\nAt inference time, for each prompt $x$:\n1.\
  \ Extract embedding $\\phi(x)$ using the sentence transformer.\n2. Predict $f(x) = \\text{sampling}$ if $P(\\text{sampling\
  \ better} \\mid \\phi(x)) > 0.5$, else $\\text{greedy}$.\n3. Generate the answer using the predicted decoding strategy.\n\
  \n### Theoretical Framework for Routing Benefit\n\nBased on information theory and empirical evidence, we derive conditions\
  \ under which routing provides benefit .\n\nLet $p$ = probability that greedy is optimal for a random prompt. The strategy\
  \ distribution entropy is $H(p) = -p\\log(p) - (1-p)\\log(1-p)$. Routing has maximum potential benefit when $H(p)$ is maximized\
  \ (i.e., $p \\approx 0.5$). When $p > 0.7$ or $p < 0.3$, routing benefit diminishes as one strategy dominates.\n\nFormally,\
  \ routing improves over always-greedy when:\n$$P(\\text{greedy correct} \\mid \\text{greedy optimal}) \\cdot p + P(\\text{sampling\
  \ correct} \\mid \\text{sampling optimal}) \\cdot (1-p) > \\max(P(\\text{greedy correct}), P(\\text{sampling correct}))$$\n\
  \nThis requires the router accuracy to exceed the majority-class baseline (e.g., 70% if 70% of prompts are sampling-optimal).\n\
  \n### Datasets\n\nWe use four datasets covering diverse task types \\footnote{Code: \\url{https://github.com/AMGrobelnik/ai-invention-073c82-when-do-tiny-learned-routers-improve-dec/tree/main/round-1/dataset-1}},\
  \ :\n\n- **GSM8K** [8]: 125 grade school math word problems with step-by-step solutions (80% sampling optimal in our experiments).\n\
  - **ARC-Challenge** [9]: 125 science reasoning multiple-choice questions (92% sampling optimal).\n- **BoolQ** [10]: 125\
  \ boolean (yes/no) questions requiring reading comprehension (88% sampling optimal).\n- **MMLU** [11]: 125 multiple-choice\
  \ questions across 57 subjects (84% sampling optimal).\n\nAll datasets are standardized to a common schema with fields:\
  \ `input` (prompt), `output` (correct answer), and `metadata`. Answers are automatically verifiable for all datasets.\n\n\
  [FIGURE:fig2]\n\n## Experiments\n\n### Experimental Setup\n\nWe conducted experiments using GPT-4o-mini via the OpenRouter\
  \ API . For each prompt, we generated:\n- 1 greedy decoding output (temperature=0.0, max_tokens=512)\n- 1 sampling decoding\
  \ output (temperature=0.7, top_p=0.9, max_tokens=512)\n\nThe experiment used 125 examples from each of the 4 datasets (500\
  \ total). We trained a logistic regression classifier on 70% of the data and evaluated on the held-out 30%.\n\n### Main\
  \ Results\n\n#### Baseline Accuracies\n\nTable 1 shows the accuracy of different strategies across the combined dataset:\n\
  \n| Strategy | Accuracy |\n|----------|----------|\n| Always greedy | 0.564 |\n| Always sampling | 0.624 |\n| Random routing\
  \ (50/50) | 0.594 |\n| Oracle routing (upper bound) | 0.624 |\n\nSampling decoding outperforms greedy decoding by 6.0% (62.4%\
  \ vs 56.4%), consistent with recent findings that sampling helps on reasoning tasks [1, 2].\n\n#### Router Performance\n\
  \nThe logistic regression classifier achieved **58.7% accuracy** in predicting which decoding strategy is optimal for held-out\
  \ prompts. This is only slightly above the majority-class baseline of 58.0% (sampling optimal rate across all datasets),\
  \ indicating limited predictive power.\n\nThe routing strategy achieved **64.6% accuracy**, providing a **2.2% improvement**\
  \ over always using sampling (62.4% vs 64.6%). However, this improvement is modest and comes with an important caveat: routing\
  \ only helps because our dataset combines tasks with different optimal strategy rates.\n\n#### Conditional Routing Benefit\n\
  \nFigure 3 shows routing benefit as a function of sampling optimal rate. When sampling is optimal for 80-92% of prompts\
  \ (individual datasets), routing provides **0% improvement** over always using sampling. When we create mixed datasets with\
  \ 30-70% sampling optimal, routing provides 2.2-11.0% improvement .\n\nThese results confirm our hypothesis: *routing only\
  \ improves accuracy when the optimal decoding strategy is balanced across prompts (30-70% range), not when one strategy\
  \ dominates.*\n\n[FIGURE:fig3]\n\n### Analysis\n\n#### Strategy Distribution Across Datasets\n\nTable 2 shows the optimal\
  \ strategy distribution across datasets:\n\n| Dataset | Sampling Optimal Rate | Greedy Optimal Rate | Routing Benefit |\n\
  |---------|----------------------|---------------------|-----------------|\n| GSM8K | 80% | 20% | 0.0% |\n| ARC-Challenge\
  \ | 92% | 8% | 0.0% |\n| BoolQ | 88% | 12% | 0.0% |\n| MMLU | 84% | 16% | 0.0% |\n| Mixed (all) | 58% | 42% | 2.2% |\n\n\
  Sampling is the dominant strategy across all datasets, with 80-92% optimal rate. This explains why routing provides no benefit\
  \ on individual datasets: the optimal decision for most prompts is already to use sampling.\n\n#### Why Does Sampling Dominate?\n\
  \nRecent work by Song et al. [1] shows greedy decoding generally outperforms sampling on most tasks, but our results show\
  \ the opposite. This discrepancy may be due to:\n\n1. **Model-specific behavior**: GPT-4o-mini may have different relative\
  \ performance of greedy vs. sampling compared to models tested in prior work.\n2. **Task composition**: Our datasets focus\
  \ on reasoning tasks (math, science, reading comprehension) where sampling is known to help [2].\n3. **Temperature choice**:\
  \ We used temperature=0.7 for sampling; lower temperatures might make sampling more similar to greedy.\n\n#### Error Analysis\n\
  \nThe classifier achieved 58.7% accuracy, only 0.7% above the majority-class baseline. Errors occur primarily on prompts\
  \ where:\n1. Both strategies produce correct answers (classifier must choose one arbitrarily).\n2. Both strategies produce\
  \ incorrect answers (optimal strategy is ambiguous).\n3. The prompt embedding does not clearly encode which strategy will\
  \ succeed.\n\n#### Computational Efficiency\n\nThe entire routing pipeline requires:\n- Embedding extraction: ~10ms per\
  \ prompt (all-MiniLM-L6-v2 on CPU)\n- Classifier prediction: <1ms per prompt (logistic regression)\n- Total overhead: ~11ms\
  \ per prompt, compared to ~500-1000ms for LLM generation\n\nThis represents a <2% computational overhead, making the approach\
  \ practical for real-time applications—*if* routing provides benefit.\n\n## Discussion\n\n### When Does Routing Help?\n\n\
  Our results provide clear evidence for the conditional nature of routing benefit. Routing only improves accuracy when:\n\
  \n1. **Strategies are balanced**: The optimal decoding strategy must be reasonably balanced across prompts (30-70% range).\
  \ When one strategy dominates (>70%), simply using that strategy approaches optimal routing performance.\n\n2. **Router\
  \ accuracy exceeds majority baseline**: The classifier must predict better than always choosing the majority class. With\
  \ 80% sampling optimal, the classifier needs >80% accuracy to help; our classifier achieved only 58.7%.\n\n3. **Strategies\
  \ are complementary**: There must exist prompts where greedy wins and prompts where sampling wins. If both strategies succeed\
  \ or fail together, routing cannot help.\n\nThese findings refine the 70% balance threshold from our original hypothesis\
  \ to 60-40 or 55-45 based on empirical evidence from RouteLLM and RouterBench [6, 7].\n\n### Comparison to Prior Work\n\n\
  Our approach differs from prior adaptive decoding methods in several key ways:\n\n1. **Supervised vs. RL**: We use supervised\
  \ learning with precomputed labels, while methods like [3] use reinforcement learning with online rewards.\n2. **Binary\
  \ vs. continuous**: We predict a binary choice (greedy vs. sampling), while methods like [4] adjust continuous temperature\
  \ parameters.\n3. **Prompt-level vs. token-level**: Our routing decision is made once per prompt, while methods like [5]\
  \ switch strategies at each token.\n\nHowever, our results show that even this simpler approach only helps under specific\
  \ conditions, suggesting the core challenge is not method complexity but strategy complementarity.\n\n### Limitations\n\n\
  Several limitations constrain the generalizability of our findings:\n\n1. **Single model**: We tested only GPT-4o-mini.\
  \ Different models may have different relative performance of greedy vs. sampling, affecting the routing potential.\n2.\
  \ **Binary decision**: Restricting routing to binary greedy-vs-sampling may miss nuances. Some prompts might benefit from\
  \ intermediate temperatures or more samples.\n3. **Limited sampling**: Using only $k=1$ sample for sampling decoding may\
  \ not reliably determine if sampling \"works.\" Prior work suggests $k \\geq 3$ samples [2].\n4. **Dataset skew**: All our\
  \ datasets show sampling dominance (80-92% optimal rate). Different task compositions might yield more balanced distributions.\n\
  5. **Small scale**: The experiment used 500 prompts. Larger-scale evaluation is needed to confirm findings.\n\n### Practical\
  \ Guidelines\n\nBased on our findings, we provide practical guidelines for when to use decoding strategy routing:\n\n- **Use\
  \ routing if**: Your dataset/task mix has 30-70% greedy-optimal prompts (balanced strategies).\n- **Skip routing if**: One\
  \ strategy dominates (>70% optimal). Simply use that strategy.\n- **Check balance first**: Run both strategies on a pilot\
  \ set of 100 prompts to measure the optimal strategy distribution before investing in routing.\n- **Consider alternatives**:\
  \ If strategies are imbalanced, consider (a) using the dominant strategy, (b) adjusting temperature continuously rather\
  \ than binary routing, or (c) mixing task types to create balance.\n\n## Conclusion\n\nWe investigated whether a simple\
  \ supervised classifier can learn to route prompts to their optimal decoding strategy (greedy or sampling) based on prompt\
  \ embeddings. Our experiments on 500 prompts from four QA datasets show that while logistic regression achieves 58.7% accuracy\
  \ in predicting which strategy is better, routing only improves accuracy by 2.2% over always using sampling—and *only* when\
  \ the optimal decoding strategy is balanced across prompts (30-70% sampling optimal).\n\nThese results make three key contributions:\
  \ (1) they demonstrate the feasibility of learning routing decisions from prompt embeddings with minimal computational overhead,\
  \ (2) they reveal that routing effectiveness depends critically on the distribution of optimal strategies across prompts,\
  \ and (3) they provide a theoretical framework and practical guidelines for when routing can—and cannot—improve decoding.\n\
  \nOur findings clarify a key misconception in the literature: predicting optimal strategy is not sufficient for routing\
  \ to help; the optimal strategy must vary sufficiently across prompts. Future work should evaluate routing on tasks with\
  \ naturally balanced strategy distributions, explore extensions to continuous temperature prediction, and test whether these\
  \ findings generalize to other models and decoding strategies.\n\n## References\n\n[1] Song, Y., Meng, Y., Tan, M., and\
  \ Peng, N. \"The Good, The Bad, and The Greedy: Evaluation of LLMs Should Not Ignore Non-Determinism.\" arXiv preprint arXiv:2407.10457,\
  \ 2024.\n\n[2] Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A., and Zhou, D. \"Self-Consistency\
  \ Improves Language Models as Mathematical Reasoners.\" EMNLP 2022.\n\n[3] Zhang, S., Ye, Z., Tenka, S., Yang, A. Z. H.,\
  \ Kong, S., and Ghai, U. \"Learning Adaptive LLM Decoding.\" arXiv preprint arXiv:2603.09065, 2026.\n\n[4] Dhuliawala, S.,\
  \ Kulikov, I., Yu, P., Celikyilmaz, A., Weston, J., Sukhbaatar, S., and Lanchantin, J. \"Adaptive Decoding via Latent Preference\
  \ Optimization.\" arXiv preprint arXiv:2411.09661, 2024.\n\n[5] Chakraborty, S., Bhatt, S., Sehwag, U. M., Ghosal, S. S.,\
  \ Qiu, J., Wang, M., Manocha, D., Huang, F., Koppel, A., and Ganesh, S. \"Collab: Controlled Decoding using Mixture of Agents\
  \ for LLM Alignment.\" ICLR 2025.\n\n[6] Ong, I., Almahairi, A., Wu, V., Chiang, W.-L., Wu, T., Gonzalez, J. E., Kadous,\
  \ W., and Stoica, I. \"RouteLLM: Learning to Route LLMs with Preference Data.\" arXiv preprint arXiv:2406.18665, 2024.\n\
  \n[7] Hu, Q., Lu, G., Zhang, P., Li, S., and Zhang, Y. \"RouterBench: A Benchmark for Multi-LLM Routing System.\" arXiv\
  \ preprint arXiv:2403.12031, 2024.\n\n[8] Cobbe, K., Kosaraju, V., Bavarian, M., Chen, M., Jun, H., Kaiser, L., Plappert,\
  \ M., Tworek, J., Hilton, J., Nakano, R., Hesse, C., and Schulman, J. \"Training Verifiers to Solve Math Word Problems.\"\
  \ arXiv preprint arXiv:2110.14168, 2021.\n\n[9] Clark, P., Cowhey, I., Etzioni, O., Khot, T., Sabharwal, A., Schoenick,\
  \ C., and Tafjord, O. \"Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge.\" arXiv preprint\
  \ arXiv:1803.05457, 2018.\n\n[10] Clark, C., Lee, K., Chang, M.-W., Kwiatkowski, T., Collins, M., and Toutanova, K. \"BoolQ:\
  \ Exploring the Surprising Difficulty of Natural Yes/No Questions.\" NAACL 2019, pp. 2924-2936.\n\n[11] Hendrycks, D., Burns,\
  \ C., Basart, S., Zou, A., Mazeika, M., Song, D., and Steinhardt, J. \"Measuring Massive Multitask Language Understanding.\"\
  \ ICLR 2021.\n\n[12] Chen, X., Zhang, Y., Liu, Q., Wu, J., Zhang, F., and Tan, T. \"Mixture of Decoding: An Attention-Inspired\
  \ Adaptive Decoding Strategy to Mitigate Hallucinations in Large Vision-Language Models.\" ACL Findings 2025.\n\n[13] Lu,\
  \ J., Li, C., Yan, H., Zhang, X., and Li, L. \"Routing to the Right Model: A Learning-Based Approach.\" arXiv preprint arXiv:2402.05845,\
  \ 2024.\n\n[14] Belinkov, Y. and Glass, J. \"Analysis Methods in Neural Language Processing: A Survey.\" TACL 2019.\n\n\
  [15] Tenney, I., Das, D., and Pavlick, E. \"BERT Rediscovers the Classical NLP Pipeline.\" NAACL 2019.\n\n[16] Reimers,\
  \ N. and Gurevych, I. \"Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks.\" EMNLP-IJCNLP 2019, pp. 3982-3992."
summary: >-
  This paper investigates when tiny learned routers can improve decoding strategy selection between greedy and sampling. Through
  experiments on 500 prompts from four QA datasets using GPT-4o-mini, we show that routing only improves accuracy (2.2% over
  best single strategy) when the optimal decoding strategy is balanced across prompts (30-70% sampling optimal). When one
  strategy dominates (>70%), routing provides no benefit. We provide a theoretical framework showing routing benefit depends
  on strategy distribution entropy and router accuracy exceeding the majority-class baseline. Our findings clarify the conditions
  under which learned routing can—and cannot—improve decoding, providing practical guidelines for when to use decoding strategy
  routing.
</paper_text>

<available_figures>
--- Item 1 ---
id: fig1
title: Routing Pipeline Architecture
caption: >-
  End-to-end pipeline for decoding strategy routing. The system extracts embeddings from input prompts, passes them through
  a logistic regression classifier to predict the optimal decoding strategy (greedy or sampling), and generates the answer
  using the predicted strategy. Oracle labels are precomputed offline by running both strategies and verifying correctness.
image_gen_detailed_description: >-
  Horizontal flow diagram, left to right, showing 5 stages: (1) 'Input Prompt' box (light gray) with example text 'What is
  2+2?', (2) 'Embedding Extraction' box (blue) with 'Sentence Transformer (all-MiniLM-L6-v2)' below, arrow labeled '384-dim
  vector', (3) 'Router Classifier' box (green) with 'Logistic Regression' inside, arrow labeled 'P(sampling better)', (4)
  'Strategy Selection' diamond (yellow) with '>0.5?' inside, two arrows: 'Yes → Sampling' and 'No → Greedy', (5) 'LLM Generation'
  box (orange) with 'GPT-4o-mini' below, producing 'Output'. Below the main flow, a dashed box 'Offline Oracle Label Construction'
  (light purple) with: 'Run greedy + sampling → Verify correctness → Store labels'. Sans-serif font, clean white background,
  no 3D effects, arrows are simple black lines with arrowheads.
aspect_ratio: '21:9'
summary: >-
  Architecture diagram showing the routing pipeline from prompt input to strategy selection and generation
figure_path: figures/fig1_v0.jpg

--- Item 2 ---
id: fig2
title: Optimal Strategy Distribution Across Datasets
caption: >-
  Distribution of optimal decoding strategies across the four datasets. Sampling decoding is optimal for 80-92% of prompts
  across all datasets, explaining why routing provides no benefit when evaluated on individual datasets. Error bars show 95%
  confidence intervals from 5-fold cross-validation.
image_gen_detailed_description: >-
  Grouped bar chart. X-axis: Dataset names ('GSM8K', 'ARC-Challenge', 'BoolQ', 'MMLU'). Y-axis: Percentage of prompts (0-100%).
  Two bars per dataset: 'Sampling Optimal' (blue) and 'Greedy Optimal' (red). Values: GSM8K: Sampling=80%, Greedy=20%; ARC:
  Sampling=92%, Greedy=8%; BoolQ: Sampling=88%, Greedy=12%; MMLU: Sampling=84%, Greedy=16%. All error bars are small (+/-
  2-3%). Horizontal dashed line at 70% labeled 'Dominance Threshold'. Sans-serif font, white background, bars have rounded
  corners, legend in top-right corner.
aspect_ratio: '21:9'
summary: >-
  Bar chart showing sampling is optimal for 80-92% of prompts across all datasets, exceeding the 70% dominance threshold
figure_path: figures/fig2_v0.jpg

--- Item 3 ---
id: fig3
title: Routing Benefit vs Strategy Balance
caption: >-
  Routing benefit (improvement over best single strategy) as a function of sampling optimal rate. Routing only provides benefit
  (positive values) when the optimal strategy is balanced between 30-70% sampling optimal. When one strategy dominates (>70%),
  routing provides zero benefit over simply using that strategy. Points show individual datasets; the line shows the theoretical
  prediction based on strategy distribution entropy.
image_gen_detailed_description: >-
  Scatter plot with line of best fit. X-axis: 'Sampling Optimal Rate (%)' (0-100%, labeled at 0, 20, 40, 60, 70, 80, 100).
  Y-axis: 'Routing Benefit (%)' (-5 to 15%, labeled at -5, 0, 5, 10, 15). Horizontal dashed line at y=0 labeled 'No benefit'.
  Vertical dashed line at x=70 labeled 'Dominance Threshold'. Data points: (80, 0.0) labeled 'GSM8K', (92, 0.0) labeled 'ARC',
  (88, 0.0) labeled 'BoolQ', (84, 0.0) labeled 'MMLU', (58, 2.2) labeled 'Mixed'. Curved line starting at (0, 0), rising to
  peak at (50, 12), then descending to (100, 0), labeled 'Theoretical max'. Shaded region 30-70% on x-axis labeled 'Benefit
  Zone'. Sans-serif font, white background, points are circles with dataset names next to them.
aspect_ratio: '21:9'
summary: >-
  Scatter plot showing routing only helps when sampling optimal rate is 30-70%, with zero benefit when one strategy dominates
  (>70%)
figure_path: figures/fig3_v0.jpg
</available_figures>

<figure_requirements>
CRITICAL: Include ALL figures from <available_figures>. No exceptions.

- Every figure MUST use \includegraphics{figures/filename.jpg}
- Do NOT skip, convert to tables, or describe without inserting
- Each needs: \begin{figure*|figure}[placement], \includegraphics, \caption, \label, \end{...} — pick env + placement by the figure's `aspect_ratio` field (see PLACEMENT below). Constrain every \includegraphics with `width=\linewidth,height=0.4\textheight,keepaspectratio` (single-column) or `width=\textwidth,height=0.45\textheight,keepaspectratio` (figure*). Use exactly these option keys — `max height=` is NOT valid LaTeX
- Use the `caption` field from each figure for \caption{...} — do NOT invent new captions
- Place figures where their [FIGURE:fig_id] markers appear in paper_text
- VERIFICATION: paper.tex MUST have exact same number of \includegraphics as <available_figures>
- Do NOT generate new figure images (no matplotlib, no PIL, no image generation). Use ONLY the pre-generated figures from <available_figures>. They were already created by a previous pipeline step.

PLACEMENT BY ASPECT RATIO (use the `aspect_ratio` field on each figure):
- `21:9` (architecture diagrams / hero figures): \begin{figure*}[!t] (full two-column width, top of page). The hero architecture diagram should appear EARLY in the paper — typically at the top of page 2. Marker placement in paper_text already determines this; preserve it.
- `16:9` (comparisons, multi-panel results): \begin{figure*}[!t] for full-width or \begin{figure}[!htbp] for single-column.
- `4:3` / `1:1` / `3:2` / `3:4` / `9:16`: \begin{figure}[!htbp] (single-column).
</figure_requirements>

<artifact_links>
The paper_text contains \footnote{Code: \url{...}} references linking to artifact source code
on GitHub. Include \usepackage{hyperref} and \usepackage{url}.
Preserve these exactly as-is — do not remove, rewrite, or convert them to plain text.
The URLs will not resolve yet (the repo is deployed after compilation) — do NOT try to verify or fix them.
</artifact_links>

<headings>
NEVER use inline math (``$...$``) inside ``\section{...}`` / ``\subsection{...}`` / ``\subsubsection{...}`` arguments — hyperref's bookmark builder errors out (``Token not allowed in a PDF string``) and the PDF outline breaks. If a section heading needs a math-looking term, use the text equivalent (``d star`` not ``$d^*$``, ``alpha-equivalent`` not ``$\alpha$-equivalent``) or wrap it in ``\texorpdfstring{$math$}{plain}``. Inline math inside body paragraphs is fine.
</headings>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.

<todos>
TODO 1. Read and STRICTLY follow these skills: aii-paper-to-latex, aii-semscholar-bib.
TODO 2. Review <paper_text> and <available_figures>. Copy all figure images into ./figures/ in your workspace. Count figures — MUST include every one. Plan placements per section. Build `./references.bib` via aii_semscholar_bib__fetch — collect DOIs/ArXiv IDs from <paper_text> and batch-fetch all BibTeX in one call. Do NOT fabricate entries.
TODO 3. Create `./paper.tex` per aii-paper-to-latex skill's setup, write ALL sections, insert ALL figures from <available_figures>, include `./references.bib` via \bibliography. Compile to PDF per skill's process. Fix errors.
TODO 4. CRITICAL VERIFICATION: Run `grep -c 'includegraphics' paper.tex`, confirm count equals figures in <available_figures>. If not, add missing figures. Verify `./paper.pdf` was created.
TODO 5. VISUAL REVIEW: Write Python script to convert EVERY page of paper.pdf to PNG at 150 DPI (use pdf2image or pymupdf). Then read ALL page screenshots — each page image costs ~1,600 tokens so a 15-page paper is only ~24K tokens. You MUST read every page. The ONLY exception is if all page images would not fit in your remaining context — in that case, read as many as fit and state which pages you are skipping and why. Check every page for layout issues, overlapping figures, cut-off text, bad spacing, formatting problems. Fix issues and recompile.
TODO 6. FINAL READ: Check page count (`pdfinfo paper.pdf` or pymupdf). Read entire paper.pdf — check for missing sections, unclear explanations, inconsistencies, typos. Fix and recompile. The ONLY exception is if all pages would not fit in your remaining context — in that case, read as many pages as fit and state which pages you are skipping and why.
</todos>

---

Output the result as JSON to: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "FullPaperExpectedFiles": {
      "description": "All expected output files from full paper generation.",
      "properties": {
        "paper_tex_path": {
          "description": "Path to LaTeX source file. Example: 'paper.tex'",
          "title": "Paper Tex Path",
          "type": "string"
        },
        "paper_pdf_path": {
          "description": "Path to compiled PDF. Example: 'paper.pdf'",
          "title": "Paper Pdf Path",
          "type": "string"
        },
        "references_bib_path": {
          "description": "Path to BibTeX bibliography file. Example: 'references.bib'",
          "title": "References Bib Path",
          "type": "string"
        },
        "figure_paths": {
          "description": "Paths to all figure image files. Example: ['figures/fig1_v0.jpg', 'figures/fig2_v0.jpg']",
          "items": {
            "type": "string"
          },
          "title": "Figure Paths",
          "type": "array"
        }
      },
      "required": [
        "paper_tex_path",
        "paper_pdf_path",
        "references_bib_path",
        "figure_paths"
      ],
      "title": "FullPaperExpectedFiles",
      "type": "object"
    }
  },
  "description": "Full paper \u2014 structured output from paper generation.",
  "properties": {
    "title": {
      "description": "Paper title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance. Aim for about 4-8 words (~40 characters).",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "description": "Brief summary of the generated paper: sections written, figures included, compilation status",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/FullPaperExpectedFiles",
      "description": "All output files you created. Must include paper.tex, paper.pdf, references.bib, and paths to all figure files."
    }
  },
  "required": [
    "title",
    "summary",
    "out_expected_files"
  ],
  "title": "FullPaper",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-08-01 00:16:37 UTC

```
Can a tiny learned router pick between two decoding strategies per prompt to beat always using either one alone?
```

### [3] SKILL-INPUT — aii-paper-to-latex · 2026-08-01 00:16:57 UTC

The agent loaded the **aii-paper-to-latex** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-to-latex
description: LaTeX paper assembly and compilation. Covers document setup, figure inclusion from pre-generated JPEGs, compilation process, and output files. Use when assembling a paper from pre-written text and pre-generated figures into a compiled PDF.
---

## LaTeX Paper Assembly

Assembles a research paper from paper text, pre-generated figure JPEGs, and bibliography into a compiled PDF.

### Document Setup

```latex
\documentclass[11pt,letterpaper]{article}
\usepackage{graphicx, geometry, amsmath, hyperref, natbib, booktabs, xcolor, listings}
\geometry{margin=1in}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}
```

### Figure Inclusion

CRITICAL: Include ALL figures. Every figure MUST appear in the paper.

```latex
\begin{figure}[!htbp]
  \centering
  \includegraphics[width=0.92\textwidth,keepaspectratio]{figures/filename.jpg}
  \caption{Descriptive caption.}
  \label{fig:label}
\end{figure}
```

Rules:
- ALWAYS use `[!htbp]` float placement (NOT `[t]` or `[h]` alone)
- ALWAYS constrain with `width` and `keepaspectratio` to prevent page takeover
- Every figure needs `\caption`, `\label`, and a `\ref` in the text
- Do NOT convert figures to tables or describe them without inserting the image
- Do NOT skip any figures

### Compilation Process

Run each command separately (do NOT chain with `&&` — pdflatex often exits non-zero on warnings, which would skip bibtex and leave citations as `??`):

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

All four commands are required. Skipping bibtex causes `??` in all citations.
Fix any errors between runs. Verify `./paper.pdf` was created.

### Output Files

- `./paper.tex` — LaTeX source
- `./references.bib` — bibliography file
- `./paper.pdf` — compiled PDF
- `./figures/*.jpg` — all figure images (pre-generated, copied into workspace)
````

### [4] SKILL-INPUT — aii-semscholar-bib · 2026-08-01 00:16:57 UTC

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
