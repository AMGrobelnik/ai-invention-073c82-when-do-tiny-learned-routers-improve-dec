# gen_plan_research_1 — test_idea

> Phase: `invention_loop` · round 2 · `gen_plan`
> Run: `run_C4UvEedrrr_P` — When Do Tiny Learned Routers Improve Decoding Strategy Selection?
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_plan_research_1` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-07-31 22:39:03 UTC

````
<hypothesis>
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

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for the methods, proper baselines, and evaluation this field demands.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<artifact_direction>
Make this direction concrete and actionable. Keep the same type and respect dependencies.

id: research_iter2_dir2
type: research
objective: >-
  Fix citation errors and investigate what prompt features drive routing decisions to address reviewer feedback
approach: >-
  1. Verify and correct citations [6], [7], [8]: ARC-Challenge (Clark et al. 2018, arXiv:1803.05457), BoolQ (Clark et al.
  2019, arXiv:1905.10044), MMLU (Hendrycks et al. 2021, arXiv:2009.03300). Check original papers via web search and fetch.
  2. Complete reference [9] for Sentence-BERT with full EMNLP 2019 citation including page numbers. 3. Investigate what prompt
  features correlate with optimal decoding strategy: research feature importance methods, probe for task type indicators,
  complexity metrics (length, perplexity), and semantic clusters. 4. Search for theoretical work on routing conditions: information
  theory, strategy distribution entropy, optimal decision boundaries. 5. Find related work on when multi-model routing helps
  to draw analogies. 6. Investigate prior work on greedy vs sampling conditions in LLMs (when does sampling help vs hurt?).
  Output: corrected references in BibTeX format, feature analysis methodology, theoretical framework for routing conditions.
depends_on:
- id: art_qYKiu0EeZ_7T
  label: prior research
  relation_type:
  relation_rationale:
</artifact_direction>

<dependencies>
Completed artifacts this artifact can use during execution.

--- Dependency 1 ---
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
out_dependency_files:
  file_list:
  - research_out.json
</dependencies>

<instructions>
YOUR ROLE: Write a detailed PLAN for the artifact. A separate executor agent runs the actual artifact later.

You are a PLANNER, not an executor. Your output is a plan that tells the executor what to do and how.
Do NOT execute the artifact itself — a separate agent handles that. Your job is to plan it so well that the executor can follow your plan step by step.

You CAN and SHOULD: search the web, read papers, and explore library docs to make your plan concrete.
You CANNOT run shell commands or scripts — code execution is disabled. Research via web tools only.

Do NOT do the executor's job: don't download datasets, don't implement code, don't run experiments, don't write proofs, don't compute evaluations.

<artifact_executor_scope>
IMPORTANT: Each artifact executor has a focused prompt that guides it to do ONE thing well. It will NOT perform tasks outside its scope — assigning the wrong work to the wrong artifact type wastes an iteration. Match the task to the right executor.

RESEARCH executor scope:
  Output: research_out.json with {answer, sources, follow_up_questions} + research_report.md
  DOES: Web research — search, read, synthesize information from papers/docs/APIs into a structured report
  DOES NOT: Run code, download files, execute scripts, compute anything — no shell/Python access
  Use for literature surveys, API documentation, technical specifications — pure information gathering
</artifact_executor_scope>

<artifact_planning_rules>
RESEARCH: Plan early — findings guide dataset selection, experiment design, and methodology.
</artifact_planning_rules>


GOOD PLANS: specific, actionable, consider failure scenarios, build on the suggested approach.
BAD PLANS: vague hand-waving, ignoring the suggested approach, missing critical executor details.
</instructions><user_data>
User-provided reference materials are available at `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_2/gen_plan/gen_plan_research_1/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "description": "Plan for a RESEARCH artifact.",
  "properties": {
    "title": {
      "description": "Plan title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters).",
      "title": "Title",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Brief summary",
      "title": "Summary",
      "type": "string"
    },
    "runpod_compute_profile": {
      "anyOf": [
        {
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": "cpu_light",
      "description": "Compute tier for execution \u2014 pick from the available profiles list (e.g., 'gpu', 'cpu_heavy', 'cpu_light'). Only used in RunPod mode.",
      "title": "Runpod Compute Profile"
    },
    "question": {
      "default": "",
      "description": "The specific research question to investigate",
      "title": "Question",
      "type": "string"
    },
    "research_plan": {
      "description": "Step-by-step plan for web research to gather this research",
      "title": "Research Plan",
      "type": "string"
    },
    "explanation": {
      "description": "Why this research matters and what question it answers",
      "title": "Explanation",
      "type": "string"
    }
  },
  "required": [
    "title",
    "research_plan",
    "explanation"
  ],
  "title": "ResearchPlan",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_2/gen_plan/gen_plan_research_1/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-07-31 22:39:03 UTC

```
Can a tiny learned router pick between two decoding strategies per prompt to beat always using either one alone?
```

### [3] SKILL-INPUT — aii-web-tools · 2026-07-31 22:40:05 UTC

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
