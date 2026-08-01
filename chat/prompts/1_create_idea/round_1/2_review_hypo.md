# review_hypo — create_idea

> Phase: `hypo_loop` · round 1 · `review_hypo`
> Run: `run_C4UvEedrrr_P` — When Do Tiny Learned Routers Improve Decoding Strategy Selection?
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `review_hypo` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-07-31 20:28:04 UTC

````
<role>
You are a very experienced and critical conference reviewer specialized in the domain of the work under review.
You have reviewed for top-tier venues in the relevant field. Your reviews are known for
being thorough, fair, and grounded in the actual state of the field.
</role>

<hypothesis>
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
</hypothesis>

<review_context>
No experiments have been run yet — evaluate the hypothesis purely on its merits.
</review_context>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for judging whether the hypothesis is genuinely novel versus already-done or a known dead end in this field.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>





<task>
Provide a thorough peer review of this research hypothesis.

STEP 1 — GROUND YOUR REVIEW IN EVIDENCE:
Before writing critiques, search for relevant context to make your review authoritative:
- Search for accepted papers at top venues in this area — what level of
  contribution gets accepted? How does this hypothesis compare?
- Search for the closest existing work — is this genuinely novel or incremental?
- Check if the proposed methodology has known failure modes in the literature

STEP 2 — WRITE YOUR REVIEW:
For each critique:
1. Categorize: methodology, evidence, novelty, clarity, scope, or rigor
2. Rate severity: major (would waste compute if not fixed) or minor (polish)
3. Describe the issue clearly
4. Suggest a concrete action to address it

Focus on the most impactful issues. Flag fatal flaws that would waste compute if not fixed first.

STABILITY IS OK: If the hypothesis is on track and just needs more iterations to prove itself,
keep your feedback similar to the previous round. Don't manufacture new critiques — only escalate
when the revision introduced new issues or failed to address prior ones.

STEP 3 — H↔H EDGE:
This is the first iteration — there is no previous hypothesis. Leave
``relation_type`` null and ``relation_rationale`` empty.

Provide your review via structured output.
</task><user_data>
User-provided reference materials are available at `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

---

Output the result as JSON to: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/iter_1/review_hypo/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "Critique": {
      "description": "A single actionable critique from the reviewer.",
      "properties": {
        "category": {
          "description": "Category: 'methodology', 'evidence', 'novelty', 'clarity', 'scope', or 'rigor'",
          "title": "Category",
          "type": "string"
        },
        "severity": {
          "description": "Severity: 'major' or 'minor'",
          "title": "Severity",
          "type": "string"
        },
        "description": {
          "description": "Clear description of the issue",
          "title": "Description",
          "type": "string"
        },
        "suggested_action": {
          "description": "Concrete suggestion for how to address this critique",
          "title": "Suggested Action",
          "type": "string"
        }
      },
      "required": [
        "category",
        "severity",
        "description",
        "suggested_action"
      ],
      "title": "Critique",
      "type": "object"
    },
    "DimensionScore": {
      "description": "Score for a single review dimension with improvement suggestions.",
      "properties": {
        "dimension": {
          "description": "Dimension name: 'soundness', 'presentation', or 'contribution'",
          "title": "Dimension",
          "type": "string"
        },
        "score": {
          "description": "Score from 1 (poor) to 4 (excellent)",
          "title": "Score",
          "type": "integer"
        },
        "justification": {
          "description": "Brief justification for this score",
          "title": "Justification",
          "type": "string"
        },
        "improvements": {
          "description": "Specific improvements to raise the score (what + how + why)",
          "items": {
            "type": "string"
          },
          "title": "Improvements",
          "type": "array"
        }
      },
      "required": [
        "dimension",
        "score",
        "justification"
      ],
      "title": "DimensionScore",
      "type": "object"
    }
  },
  "description": "ReviewerFeedback + Moulines H\u2194H typology for hypo_loop iterations.\n\nAdds ``relation_type`` + ``relation_rationale`` so the trace projection\ncan build a typed edge from the previous iteration's hypothesis to\nthis iteration's. On iteration 1 (no previous), both fields are\nempty/None.",
  "properties": {
    "overall_assessment": {
      "description": "Overall assessment of the paper's quality and readiness",
      "title": "Overall Assessment",
      "type": "string"
    },
    "strengths": {
      "description": "Key strengths of the paper",
      "items": {
        "type": "string"
      },
      "title": "Strengths",
      "type": "array"
    },
    "dimension_scores": {
      "description": "Scores (1-4) for: soundness, presentation, contribution",
      "items": {
        "$ref": "#/$defs/DimensionScore"
      },
      "title": "Dimension Scores",
      "type": "array"
    },
    "critiques": {
      "description": "Actionable critiques \u2014 specific issues with concrete suggestions",
      "items": {
        "$ref": "#/$defs/Critique"
      },
      "title": "Critiques",
      "type": "array"
    },
    "score": {
      "description": "Overall quality score from 1 (very strong reject) to 10 (award quality)",
      "title": "Score",
      "type": "integer"
    },
    "confidence": {
      "default": 3,
      "description": "Confidence in assessment from 1 (educated guess) to 5 (absolutely certain)",
      "title": "Confidence",
      "type": "integer"
    },
    "relation_type": {
      "anyOf": [
        {
          "enum": [
            "evolution",
            "embedding",
            "replacement"
          ],
          "type": "string"
        },
        {
          "type": "null"
        }
      ],
      "default": null,
      "description": "Moulines's structuralist typology classifying how this iteration's hypothesis relates to the previous iteration's: 'evolution' \u2014 refining specialised claims while keeping the same conceptual frame; 'embedding' \u2014 the previous hypothesis is now a special case of a broader frame; 'replacement' \u2014 rejecting the previous frame entirely (Kuhnian shift). Leave null on the first iteration (no previous hypothesis).",
      "title": "Relation Type"
    },
    "relation_rationale": {
      "default": "",
      "description": "Brief rationale (one short line, \u2264120 chars) for the relation_type. Empty on the first iteration.",
      "maxLength": 120,
      "title": "Relation Rationale",
      "type": "string"
    }
  },
  "required": [
    "overall_assessment",
    "strengths",
    "critiques",
    "score"
  ],
  "title": "HypoReviewerFeedback",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/iter_1/review_hypo/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-07-31 20:28:04 UTC

```
Can a tiny learned router pick between two decoding strategies per prompt to beat always using either one alone?
```

### [3] SKILL-INPUT — aii-web-tools · 2026-07-31 20:28:14 UTC

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
