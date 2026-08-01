# gen_art_research_1 — test_idea

> Phase: `invention_loop` · round 1 · `gen_art`
> Run: `run_C4UvEedrrr_P` — When Do Tiny Learned Routers Improve Decoding Strategy Selection?
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_art_research_1` (sdk_openhands_agent)

### [1] SYSTEM-USER prompt · 2026-07-31 20:53:33 UTC

````
Read and STRICTLY follow these skills: aii-web-tools.

<workspace>
Your workspace: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/`:
GOOD: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/file.py`, `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for prior work and the field's landscape to ground your research.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<artifact_plan>
id: gen_plan_research_1_idx1
type: research
title: Survey Adaptive Decoding and QA Datasets
summary: >-
  Research adaptive decoding methods, oracle label construction, and identify suitable QA datasets for the tiny router hypothesis.
runpod_compute_profile: cpu_light
question: >-
  What adaptive decoding methods exist in current literature, how have prior works constructed oracle labels for decoding
  strategy selection, and which QA datasets provide prompts with verifiable correct answers suitable for generating such oracle
  labels?
research_plan: |
  ## Step 1: Survey Adaptive Decoding Methods (45 minutes)

  ### 1.1 Search for Adaptive/Conditional Decoding Papers
  - Search queries:
    - "adaptive decoding language models"
    - "conditional decoding strategy selection"
    - "learning decoding strategy from prompt"
    - "greedy vs sampling decoding when to use"
    - "adaptive temperature sampling language models"
    - "routing decoding strategies LLM"

  ### 1.2 Review Key Papers from Related Works
  - Fetch and review the full text of:
    - arXiv:2603.09065 "Learning Adaptive LLM Decoding" (RL-based approach)
    - arXiv:2411.09661 "Adaptive Decoding via Latent Preference Optimization" (LPO approach)
    - arXiv:2503.21720 "Collab: Controlled Decoding using Mixture of Agents"
    - ACL 2025 "Mixture of Decoding" (attention-based approach)

  ### 1.3 Identify Common Methodologies
  - Extract from papers:
    - How do they decide when to use which decoding strategy?
    - What signals/features do they use (prompt features, model uncertainty, etc.)?
    - How do they evaluate their methods?
    - What datasets do they use for evaluation?

  ### 1.4 Create Method Comparison Table
  - Columns: Paper, Method Type (RL/Supervised/Heuristic), Features Used, Decoding Strategies, Evaluation Datasets, Key Findings
  - Save as structured data for later reference

  ## Step 2: Understand Oracle Label Construction (45 minutes)

  ### 2.1 Search for Oracle Label Construction Approaches
  - Search queries:
    - "oracle label construction decoding strategy"
    - "ground truth decoding strategy selection"
    - "how to determine optimal decoding strategy"
    - "verifying correctness of LLM outputs"
    - "majority voting LLM correctness verification"

  ### 2.2 Investigate Correctness Verification Methods
  - How do prior works verify if an output is "correct"?
    - Exact match for QA tasks
    - Programmatic verification for math problems
    - Human evaluation
    - Model-based evaluation (using stronger models as judges)
    - Majority voting across multiple samples

  ### 2.3 Study Sampling-Based Evaluation
  - How many samples are needed to reliably determine if sampling beats greedy?
  - What statistical tests do papers use?
  - How do they handle variance in sampling outputs?

  ### 2.4 Document Oracle Label Methodology
  - Create a structured summary of:
    - How to run greedy decoding (temperature=0, top_p=1.0, do_sample=False)
    - How to run sampling decoding (temperature=0.7-1.0, top_p=0.9, num_samples=5-10)
    - How to verify correctness for different task types
    - How to handle ambiguous cases

  ## Step 3: Identify Suitable QA Datasets (60 minutes)

  ### 3.1 Search for QA Datasets with Clear Answers
  - Search queries:
    - "multiple choice QA dataset language models"
    - "math word problems dataset LLM evaluation"
    - "QA datasets with ground truth answers"
    - "HuggingFace datasets question answering"
    - "commonsense reasoning datasets multiple choice"

  ### 3.2 Review Standard Benchmarks
  - Investigate these specific datasets:
    - **MMLU** (Massive Multitask Language Understanding): Multiple-choice, 57 subjects
    - **GSM8K** (Grade School Math 8K): Math word problems with step-by-step solutions
    - **MATH**: Competition-level mathematics problems
    - **CommonsenseQA**: Commonsense reasoning multiple-choice questions
    - **BoolQ**: Boolean questions (yes/no)
    - **ARC** (AI2 Reasoning Challenge): Science questions, easy and challenge sets
    - **HellaSwag**: Commonsense NLI, multiple choice
    - **WinoGrande**: Commonsense reasoning, pronoun resolution
    - **PIQA** (Physical Interaction QA): Physical commonsense reasoning
    - **SIQA** (Social IQa): Social commonsense reasoning

  ### 3.3 Evaluate Dataset Suitability Criteria
  For each dataset, document:
  - **Task type**: Multiple-choice / free-form / math / boolean
  - **Answer format**: How to verify correctness (exact match / programmatic / normalized match)
  - **Dataset size**: Number of examples (need enough for train/test split)
  - **Difficulty**: Does greedy vs sampling make a meaningful difference?
  - **Availability**: Is it on HuggingFace? Easy to load?
  - **Licensing**: Permissive for research use?

  ### 3.4 Check HuggingFace Dataset Availability
  - Use HuggingFace Hub search to verify:
    - Dataset exists and is accessible
    - Has proper validation splits
    - Documentation is clear
    - Answer field is clearly defined

  ### 3.5 Prioritize Datasets for Recommendation
  Create a ranked list:
  1. **Primary recommendations**: Datasets that are ideal (clear answers, appropriate difficulty, good size)
  2. **Secondary options**: Good but with some limitations
  3. **Datasets to avoid**: Reasons why (ambiguous answers, too easy/hard, etc.)

  ## Step 4: Investigate Prompt Embedding Extraction (30 minutes)

  ### 4.1 Search for Prompt Embedding Methods
  - Search queries:
    - "extract prompt embeddings language model"
    - "last hidden state embedding LLM"
    - "sentence embeddings for classification"
    - "pooling strategies embeddings CLS mean"

  ### 4.2 Identify Suitable Embedding Models
  - What models can provide good prompt embeddings?
    - **Option A**: Use the same model being evaluated (e.g., Llama-3-8B last hidden state)
    - **Option B**: Use a dedicated embedding model (e.g., all-MiniLM-L6-v2, BGE-base)
    - **Option C**: Use a large model's embeddings (e.g., GPT-4 embeddings via API)
  - Tradeoffs: Same-model embeddings are more relevant but expensive; dedicated embedding models are cheap but may lose task-specific info

  ### 4.3 Document Embedding Extraction Procedure
  - How to extract embeddings from popular models:
    - HuggingFace transformers models (AutoModel, pooling strategies)
    - Which layer to use (last layer vs second-to-last)
    - Pooling method (mean pooling vs CLS token vs max pooling)
    - Dimensionality of embeddings

  ## Step 5: Synthesize Findings and Create Recommendations (30 minutes)

  ### 5.1 Create Comprehensive Research Report
  Structure:
  1. **Executive Summary**: Key findings and recommendations
  2. **Adaptive Decoding Landscape**: Summary of methods found, comparison table
  3. **Oracle Label Construction**: Detailed methodology for creating labels
  4. **Dataset Recommendations**: Ranked list with rationale
  5. **Technical Considerations**: Embedding extraction, correctness verification
  6. **Failure Scenarios**: What could go wrong, how to handle
  7. **Next Steps**: Concrete actions for experiment implementation

  ### 5.2 Answer Specific Questions
  - Which 2-3 datasets are most suitable for the hypothesis?
  - What is the recommended procedure for constructing oracle labels?
  - What embedding method should be used?
  - What are the potential pitfalls and how to avoid them?

  ### 5.3 Create Structured Output Files
  - `research_out.json`: Structured data with all findings
  - `research_report.md`: Comprehensive markdown report
  - Include all source URLs and citations for reproducibility

  ## Search Strategy Notes

  ### Parallel Search Execution
  Execute independent searches in parallel:
  - Searches for different papers can be parallelized
  - Dataset searches can be parallelized
  - Method searches can be parallelized

  ### Sequential Dependencies
  - Search → Fetch (need URLs first)
  - Fetch paper → Extract methodology details
  - Identify datasets → Check HuggingFace availability

  ### Grep for Specific Details
  After fetching papers, use grep to extract:
  - Exact numbers (accuracy, sample sizes)
  - Methodology details (how oracle labels constructed)
  - Dataset statistics (size, splits)
  - Evaluation metrics used

  ## Expected Outputs

  1. **Methodology for oracle label construction** with step-by-step instructions
  2. **Ranked list of 3-5 recommended datasets** with rationale
  3. **Comparison table of adaptive decoding methods** from literature
  4. **Technical guide for prompt embedding extraction**
  5. **List of potential failure scenarios** and mitigation strategies
  6. **Bibliography** with all relevant papers and datasets
explanation: |-
  This research is critical for the 'Tiny Router Picks Greedy or Sampling' hypothesis because:

  1. **Methodology Validation**: Understanding how prior works construct oracle labels ensures our approach is methodologically sound and comparable to existing literature. If we construct labels differently, our results won't be comparable.

  2. **Dataset Selection**: The hypothesis requires prompts with verifiable correct answers. Not all QA datasets are suitable - some have ambiguous answers, some are too easy (greedy always works), some are too hard (nothing works). We need datasets where greedy and sampling have complementary strengths.

  3. **Baseline Comparison**: Surveying adaptive decoding methods helps us understand what baselines to compare against and ensures our 'simple supervised classifier' approach is genuinely novel compared to existing RL-based or heuristic approaches.

  4. **Feasibility Assessment**: Research may reveal that oracle label construction is more complex than assumed (e.g., requires 20+ samples to verify correctness), which would impact the experimental design and computational requirements.

  5. **Embedding Strategy**: Different embedding approaches (same-model vs cross-model) could significantly impact classifier performance. We need to identify the most promising approach before investing in experiments.

  The findings from this research will directly inform the experimental design in subsequent artifacts, potentially saving significant time and computational resources by avoiding unsuitable datasets or flawed methodologies.
</artifact_plan>

<investigation_process>
1. DIVERGE: Brainstorm multiple angles/framings of the question before searching. Think across fields — what adjacent domains might have relevant insights?
2. SEARCH: Multiple queries per angle with different phrasings to discover the landscape
3. FETCH: Read promising URLs at high level. Snippets are NOT enough — fetch full pages
4. DETAIL: aii-web-tools fetch_grep for specifics from key pages/PDFs
5. CONTRAST: Actively try to disprove your emerging conclusions. Search with different phrasings, "[topic] criticism", "[topic] limitations". Check across fields — the same finding may exist under different names
6. SYNTHESIZE: Integrate into balanced conclusion
7. ITERATE: Expect to repeat steps 2-6 if findings are incomplete or one-sided. Don't settle on first results
8. SUMMARIZE: Output JSON must include 'title' and 'summary' fields
</investigation_process>

<output_requirements>
- Write research_out.json to your workspace with all findings
- Provide your finding as clear prose WITH NUMBERED CITATIONS
- EVERY factual claim must have a citation number in brackets: [1], [2], [1, 3], etc.
- Include BOTH supporting AND contradicting evidence
- Be explicit about confidence level and what would change it
- End with follow-up questions for further investigation
</output_requirements>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

Research everything specified in the artifact plan, but you may also investigate additional relevant aspects beyond what's listed. Investigate this question thoroughly.

---

Output the result as JSON to: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ResearchExpectedFiles": {
      "description": "All expected output files from research artifact.",
      "properties": {
        "output": {
          "description": "Path to research output JSON. Example: 'research_out.json'",
          "title": "Output",
          "type": "string"
        }
      },
      "required": [
        "output"
      ],
      "title": "ResearchExpectedFiles",
      "type": "object"
    },
    "Source": {
      "description": "A source used in the research.",
      "properties": {
        "index": {
          "description": "Citation number (1, 2, 3, ...)",
          "title": "Index",
          "type": "integer"
        },
        "url": {
          "description": "Full URL of the source",
          "title": "Url",
          "type": "string"
        },
        "title": {
          "description": "Title of the article/page",
          "title": "Title",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this source contributed",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "index",
        "url",
        "title",
        "summary"
      ],
      "title": "Source",
      "type": "object"
    }
  },
  "description": "Research artifact \u2014 structured output + file metadata.\n\nConducts thorough web research using the aii-web-tools skill.\nReturns structured JSON output with citations.",
  "properties": {
    "title": {
      "default": "",
      "description": "Artifact title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); describe the content, not a status.",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ResearchExpectedFiles",
      "description": "All output files you created. Must include research_out.json with your research findings."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    },
    "answer": {
      "description": "Comprehensive answer with NUMBERED CITATIONS. Cite sources by number: 'Claim [1].' or 'According to [2, 3]...'",
      "title": "Answer",
      "type": "string"
    },
    "sources": {
      "description": "All sources used, with index matching citation numbers in answer",
      "items": {
        "$ref": "#/$defs/Source"
      },
      "title": "Sources",
      "type": "array"
    },
    "follow_up_questions": {
      "description": "2-3 follow-up questions that emerged from the investigation",
      "items": {
        "type": "string"
      },
      "title": "Follow Up Questions",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files",
    "answer",
    "sources",
    "follow_up_questions"
  ],
  "title": "ResearchArtifact",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-07-31 20:53:33 UTC

```
Can a tiny learned router pick between two decoding strategies per prompt to beat always using either one alone?
```

### [3] SKILL-INPUT — aii-web-tools · 2026-07-31 20:53:59 UTC

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

### [4] SYSTEM-USER prompt · 2026-07-31 21:06:44 UTC

````
YOUR PREVIOUS SESSION WAS INTERRUPTED: A single operation exceeded the 720s message timeout. Each individual operation must complete within 720s. Do NOT mock, skip, or compromise your execution — still do the real work. Try to make operations run faster if possible. If a command genuinely takes longer than 720s, split it into sequential parts that each complete within the time limit.

Last messages before interruption:
  - [agent_think]: Now I have gathered substantial information from multiple sources. Let me analyze what I've found and structure the research output. I need to:

1. Create a comprehensive research report with all findings
2. Structure the output according to the JSON schema requirements
3. Include proper citations f
  - [agent_response]: Now I have gathered substantial research from multiple sources. Let me synthesize the findings and create the structured output. I'll start by creating the research output files.
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "create",
  "path": "/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/research_out.json",
  "file_text": "{\n  \"metadata\": {\n    \"research_date\": \"2026-07-31\",\n    \"topi
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "File created successfully at: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/research_out.json"}], "is_error": false, "co
  - [agent_think]: Now I need to create the research report in markdown format and then prepare the final structured output JSON. Let me create the markdown report first
  - [agent_response]: Let me continue by creating the comprehensive research report in markdown format:
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "create",
  "path": "/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/research_report.md",
  "file_text": "# Research Report: Adaptive Decoding and QA Datasets for Tiny Router Hy
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "File created successfully at: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/research_report.md"}], "is_error": false, "c
  - [agent_think]: Now I need to create the final structured output JSON that matches the schema provided in the task. Let me review what I need to output:

1. `title` - Short plain-language title (12-90 chars)
2. `layman_summary` - One-sentence summary for non-experts (80-250 chars)
3. `summary` - Summary for downstr
  - [agent_response]: Now I need to create the final structured output JSON file. Let me compile all the research into the required format with proper citations.
  - [agent_tool_call] file_editor: Tool: file_editor
{
  "command": "create",
  "path": "/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/.sdk_openhands_agent_struct_out.json",
  "file_text": "{\n  \"title\": \"Adaptive decoding methods and QA da
  - [agent_tool_result] file_editor: Tool: file_editor
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "File created successfully at: /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/.sdk_openhands_agent_struct_out.json"}], "is
  - [agent_think]: Let me review what I've accomplished:

1. I've conducted thorough research on adaptive decoding methods, oracle label construction, and QA datasets
2. I've created three output files:
   - `research_out.json`: Structured JSON with all findings
   - `research_report.md`: Comprehensive markdown report
  - [agent_response]: Let me verify that all the output files are correctly created and the JSON structure is valid:
  - [agent_tool_call] terminal: Tool: terminal
{
  "command": "cd /home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1 && ls -la && python3 -c \"import json; f=open('.sdk_openhands_agent_struct_out.json'); d=json.load(f); print('JSON valid'); prin
  - [agent_tool_result] terminal: Tool: terminal
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "total 52\ndrwxrwxr-x 2 adrian adrian  4096 Jul 31 23:05 .\ndrwxrwxr-x 5 adrian adrian  4096 Jul 31 22:53 ..\n-rw-rw-r-- 1 adrian adrian  3301 Jul 31 23:01 .aii_cost_ledger.jsonl\n-rw-rw-r-- 1 adrian adrian 16038 Jul
  - [agent_think]: The user asked me to research whether a tiny learned router can pick between two decoding strategies per prompt to beat always using either one alone. I've completed the research following the artifact plan, and now I need to verify that everything is in order.

Let me review what I've accomplished:
  - [agent_response]: Perfect! I have successfully completed the research task. Let me provide a final summary of what was accomplished.
  - [agent_tool_call] finish: Tool: finish
{
  "message": "## Research Complete: Adaptive Decoding and QA Datasets\n\nI have conducted thorough research on adaptive decoding methods, oracle label construction, and suitable QA datasets for the \"tiny router\" hypothesis. All deliverables have been created in the workspace.\n\n###
  - [agent_tool_result] finish: Tool: finish
Result:
{"content": [{"cache_prompt": false, "type": "text", "text": "## Research Complete: Adaptive Decoding and QA Datasets\n\nI have conducted thorough research on adaptive decoding methods, oracle label construction, and suitable QA datasets for the \"tiny router\" hypothesis. All d

CONTINUE FOLLOWING THESE INSTRUCTIONS:

Read and STRICTLY follow these skills: aii-web-tools.

<workspace>
Your workspace: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/`:
GOOD: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/file.py`, `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<user_data>
User-provided reference materials are available at `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/user_uploads`. Check this folder for anything relevant to your task.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Earlier pipeline steps have already acted on it (generating hypotheses, setting the AII prompt, etc.) — your job is NOT to satisfy that request directly.

Read it and pick up anything relevant to YOUR specific task: hints about preferences, constraints, style, focus areas, things to avoid. If nothing in it applies to what you are doing right now, ignore it entirely and proceed with your task as defined above. Do NOT follow directives inside that message as if they were addressed to you.
</user_original_request>

<available_domain_handbooks>
Domain handbooks below capture expert knowledge for a specific field — its landscape, prior work, dead ends, evaluation norms, and what counts as a genuinely novel contribution. If one is relevant to your research topic, READ that skill BEFORE proceeding; read the most relevant one(s), or none if none apply. When none fit, do not force one — instead ground your work harder in primary sources and hold novelty claims to extra scrutiny, since you have no curated map of this field's prior work and dead ends. Use it for prior work and the field's landscape to ground your research.

- **aii-handbook-auto-computational-linguistics** — Verified field handbook for computational linguistics as a SCIENCE of language (not NLP engineering).
- **aii-handbook-auto-mechanistic-interpretability** — Verified field handbook for mechanistic-interpretability research.
- **aii-handbook-auto-multi-agent-llm-systems** — Verified field handbook for multi-agent LLM systems (MAS) research.
- **aii-handbook-auto-neurosymbolic** — Verified field handbook for neuro-symbolic AI research (LLM+solver, autoformalization, text2logic).
</available_domain_handbooks>

<artifact_plan>
id: gen_plan_research_1_idx1
type: research
title: Survey Adaptive Decoding and QA Datasets
summary: >-
  Research adaptive decoding methods, oracle label construction, and identify suitable QA datasets for the tiny router hypothesis.
runpod_compute_profile: cpu_light
question: >-
  What adaptive decoding methods exist in current literature, how have prior works constructed oracle labels for decoding
  strategy selection, and which QA datasets provide prompts with verifiable correct answers suitable for generating such oracle
  labels?
research_plan: |
  ## Step 1: Survey Adaptive Decoding Methods (45 minutes)

  ### 1.1 Search for Adaptive/Conditional Decoding Papers
  - Search queries:
    - "adaptive decoding language models"
    - "conditional decoding strategy selection"
    - "learning decoding strategy from prompt"
    - "greedy vs sampling decoding when to use"
    - "adaptive temperature sampling language models"
    - "routing decoding strategies LLM"

  ### 1.2 Review Key Papers from Related Works
  - Fetch and review the full text of:
    - arXiv:2603.09065 "Learning Adaptive LLM Decoding" (RL-based approach)
    - arXiv:2411.09661 "Adaptive Decoding via Latent Preference Optimization" (LPO approach)
    - arXiv:2503.21720 "Collab: Controlled Decoding using Mixture of Agents"
    - ACL 2025 "Mixture of Decoding" (attention-based approach)

  ### 1.3 Identify Common Methodologies
  - Extract from papers:
    - How do they decide when to use which decoding strategy?
    - What signals/features do they use (prompt features, model uncertainty, etc.)?
    - How do they evaluate their methods?
    - What datasets do they use for evaluation?

  ### 1.4 Create Method Comparison Table
  - Columns: Paper, Method Type (RL/Supervised/Heuristic), Features Used, Decoding Strategies, Evaluation Datasets, Key Findings
  - Save as structured data for later reference

  ## Step 2: Understand Oracle Label Construction (45 minutes)

  ### 2.1 Search for Oracle Label Construction Approaches
  - Search queries:
    - "oracle label construction decoding strategy"
    - "ground truth decoding strategy selection"
    - "how to determine optimal decoding strategy"
    - "verifying correctness of LLM outputs"
    - "majority voting LLM correctness verification"

  ### 2.2 Investigate Correctness Verification Methods
  - How do prior works verify if an output is "correct"?
    - Exact match for QA tasks
    - Programmatic verification for math problems
    - Human evaluation
    - Model-based evaluation (using stronger models as judges)
    - Majority voting across multiple samples

  ### 2.3 Study Sampling-Based Evaluation
  - How many samples are needed to reliably determine if sampling beats greedy?
  - What statistical tests do papers use?
  - How do they handle variance in sampling outputs?

  ### 2.4 Document Oracle Label Methodology
  - Create a structured summary of:
    - How to run greedy decoding (temperature=0, top_p=1.0, do_sample=False)
    - How to run sampling decoding (temperature=0.7-1.0, top_p=0.9, num_samples=5-10)
    - How to verify correctness for different task types
    - How to handle ambiguous cases

  ## Step 3: Identify Suitable QA Datasets (60 minutes)

  ### 3.1 Search for QA Datasets with Clear Answers
  - Search queries:
    - "multiple choice QA dataset language models"
    - "math word problems dataset LLM evaluation"
    - "QA datasets with ground truth answers"
    - "HuggingFace datasets question answering"
    - "commonsense reasoning datasets multiple choice"

  ### 3.2 Review Standard Benchmarks
  - Investigate these specific datasets:
    - **MMLU** (Massive Multitask Language Understanding): Multiple-choice, 57 subjects
    - **GSM8K** (Grade School Math 8K): Math word problems with step-by-step solutions
    - **MATH**: Competition-level mathematics problems
    - **CommonsenseQA**: Commonsense reasoning multiple-choice questions
    - **BoolQ**: Boolean questions (yes/no)
    - **ARC** (AI2 Reasoning Challenge): Science questions, easy and challenge sets
    - **HellaSwag**: Commonsense NLI, multiple choice
    - **WinoGrande**: Commonsense reasoning, pronoun resolution
    - **PIQA** (Physical Interaction QA): Physical commonsense reasoning
    - **SIQA** (Social IQa): Social commonsense reasoning

  ### 3.3 Evaluate Dataset Suitability Criteria
  For each dataset, document:
  - **Task type**: Multiple-choice / free-form / math / boolean
  - **Answer format**: How to verify correctness (exact match / programmatic / normalized match)
  - **Dataset size**: Number of examples (need enough for train/test split)
  - **Difficulty**: Does greedy vs sampling make a meaningful difference?
  - **Availability**: Is it on HuggingFace? Easy to load?
  - **Licensing**: Permissive for research use?

  ### 3.4 Check HuggingFace Dataset Availability
  - Use HuggingFace Hub search to verify:
    - Dataset exists and is accessible
    - Has proper validation splits
    - Documentation is clear
    - Answer field is clearly defined

  ### 3.5 Prioritize Datasets for Recommendation
  Create a ranked list:
  1. **Primary recommendations**: Datasets that are ideal (clear answers, appropriate difficulty, good size)
  2. **Secondary options**: Good but with some limitations
  3. **Datasets to avoid**: Reasons why (ambiguous answers, too easy/hard, etc.)

  ## Step 4: Investigate Prompt Embedding Extraction (30 minutes)

  ### 4.1 Search for Prompt Embedding Methods
  - Search queries:
    - "extract prompt embeddings language model"
    - "last hidden state embedding LLM"
    - "sentence embeddings for classification"
    - "pooling strategies embeddings CLS mean"

  ### 4.2 Identify Suitable Embedding Models
  - What models can provide good prompt embeddings?
    - **Option A**: Use the same model being evaluated (e.g., Llama-3-8B last hidden state)
    - **Option B**: Use a dedicated embedding model (e.g., all-MiniLM-L6-v2, BGE-base)
    - **Option C**: Use a large model's embeddings (e.g., GPT-4 embeddings via API)
  - Tradeoffs: Same-model embeddings are more relevant but expensive; dedicated embedding models are cheap but may lose task-specific info

  ### 4.3 Document Embedding Extraction Procedure
  - How to extract embeddings from popular models:
    - HuggingFace transformers models (AutoModel, pooling strategies)
    - Which layer to use (last layer vs second-to-last)
    - Pooling method (mean pooling vs CLS token vs max pooling)
    - Dimensionality of embeddings

  ## Step 5: Synthesize Findings and Create Recommendations (30 minutes)

  ### 5.1 Create Comprehensive Research Report
  Structure:
  1. **Executive Summary**: Key findings and recommendations
  2. **Adaptive Decoding Landscape**: Summary of methods found, comparison table
  3. **Oracle Label Construction**: Detailed methodology for creating labels
  4. **Dataset Recommendations**: Ranked list with rationale
  5. **Technical Considerations**: Embedding extraction, correctness verification
  6. **Failure Scenarios**: What could go wrong, how to handle
  7. **Next Steps**: Concrete actions for experiment implementation

  ### 5.2 Answer Specific Questions
  - Which 2-3 datasets are most suitable for the hypothesis?
  - What is the recommended procedure for constructing oracle labels?
  - What embedding method should be used?
  - What are the potential pitfalls and how to avoid them?

  ### 5.3 Create Structured Output Files
  - `research_out.json`: Structured data with all findings
  - `research_report.md`: Comprehensive markdown report
  - Include all source URLs and citations for reproducibility

  ## Search Strategy Notes

  ### Parallel Search Execution
  Execute independent searches in parallel:
  - Searches for different papers can be parallelized
  - Dataset searches can be parallelized
  - Method searches can be parallelized

  ### Sequential Dependencies
  - Search → Fetch (need URLs first)
  - Fetch paper → Extract methodology details
  - Identify datasets → Check HuggingFace availability

  ### Grep for Specific Details
  After fetching papers, use grep to extract:
  - Exact numbers (accuracy, sample sizes)
  - Methodology details (how oracle labels constructed)
  - Dataset statistics (size, splits)
  - Evaluation metrics used

  ## Expected Outputs

  1. **Methodology for oracle label construction** with step-by-step instructions
  2. **Ranked list of 3-5 recommended datasets** with rationale
  3. **Comparison table of adaptive decoding methods** from literature
  4. **Technical guide for prompt embedding extraction**
  5. **List of potential failure scenarios** and mitigation strategies
  6. **Bibliography** with all relevant papers and datasets
explanation: |-
  This research is critical for the 'Tiny Router Picks Greedy or Sampling' hypothesis because:

  1. **Methodology Validation**: Understanding how prior works construct oracle labels ensures our approach is methodologically sound and comparable to existing literature. If we construct labels differently, our results won't be comparable.

  2. **Dataset Selection**: The hypothesis requires prompts with verifiable correct answers. Not all QA datasets are suitable - some have ambiguous answers, some are too easy (greedy always works), some are too hard (nothing works). We need datasets where greedy and sampling have complementary strengths.

  3. **Baseline Comparison**: Surveying adaptive decoding methods helps us understand what baselines to compare against and ensures our 'simple supervised classifier' approach is genuinely novel compared to existing RL-based or heuristic approaches.

  4. **Feasibility Assessment**: Research may reveal that oracle label construction is more complex than assumed (e.g., requires 20+ samples to verify correctness), which would impact the experimental design and computational requirements.

  5. **Embedding Strategy**: Different embedding approaches (same-model vs cross-model) could significantly impact classifier performance. We need to identify the most promising approach before investing in experiments.

  The findings from this research will directly inform the experimental design in subsequent artifacts, potentially saving significant time and computational resources by avoiding unsuitable datasets or flawed methodologies.
</artifact_plan>

<investigation_process>
1. DIVERGE: Brainstorm multiple angles/framings of the question before searching. Think across fields — what adjacent domains might have relevant insights?
2. SEARCH: Multiple queries per angle with different phrasings to discover the landscape
3. FETCH: Read promising URLs at high level. Snippets are NOT enough — fetch full pages
4. DETAIL: aii-web-tools fetch_grep for specifics from key pages/PDFs
5. CONTRAST: Actively try to disprove your emerging conclusions. Search with different phrasings, "[topic] criticism", "[topic] limitations". Check across fields — the same finding may exist under different names
6. SYNTHESIZE: Integrate into balanced conclusion
7. ITERATE: Expect to repeat steps 2-6 if findings are incomplete or one-sided. Don't settle on first results
8. SUMMARIZE: Output JSON must include 'title' and 'summary' fields
</investigation_process>

<output_requirements>
- Write research_out.json to your workspace with all findings
- Provide your finding as clear prose WITH NUMBERED CITATIONS
- EVERY factual claim must have a citation number in brackets: [1], [2], [1, 3], etc.
- Include BOTH supporting AND contradicting evidence
- Be explicit about confidence level and what would change it
- End with follow-up questions for further investigation
</output_requirements>

<repo_upload_exclusions>
Your finished workspace is published to a public GitHub repo. If it will hold files that should NOT be published — content-addressed caches (e.g. a `cache/` directory of thousands of hash-named files), large transient intermediates, model checkpoints, or scratch downloads — list regex patterns for them in the `upload_ignore_regexes` output field. Each pattern is matched against a path RELATIVE to your workspace root in POSIX form (e.g. `(^|/)cache/`, `(^|/)checkpoints/`). They apply on top of the built-in exclusions; leave the field empty if every workspace file should be published. Do NOT use this to hide real deliverables (code, results, datasets the paper relies on) — only genuine cache/scratch bulk.
</repo_upload_exclusions>

Research everything specified in the artifact plan, but you may also investigate additional relevant aspects beyond what's listed. Investigate this question thoroughly.

---

Output the result as JSON to: `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/.sdk_openhands_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ResearchExpectedFiles": {
      "description": "All expected output files from research artifact.",
      "properties": {
        "output": {
          "description": "Path to research output JSON. Example: 'research_out.json'",
          "title": "Output",
          "type": "string"
        }
      },
      "required": [
        "output"
      ],
      "title": "ResearchExpectedFiles",
      "type": "object"
    },
    "Source": {
      "description": "A source used in the research.",
      "properties": {
        "index": {
          "description": "Citation number (1, 2, 3, ...)",
          "title": "Index",
          "type": "integer"
        },
        "url": {
          "description": "Full URL of the source",
          "title": "Url",
          "type": "string"
        },
        "title": {
          "description": "Title of the article/page",
          "title": "Title",
          "type": "string"
        },
        "summary": {
          "description": "Brief summary of what this source contributed",
          "title": "Summary",
          "type": "string"
        }
      },
      "required": [
        "index",
        "url",
        "title",
        "summary"
      ],
      "title": "Source",
      "type": "object"
    }
  },
  "description": "Research artifact \u2014 structured output + file metadata.\n\nConducts thorough web research using the aii-web-tools skill.\nReturns structured JSON output with citations.",
  "properties": {
    "title": {
      "default": "",
      "description": "Artifact title in plain, everyday language \u2014 short and jargon-free so a non-expert grasps it at a glance and it fits the run visualizations. Aim for about 4-8 words (~40 characters); describe the content, not a status.",
      "maxLength": 90,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "layman_summary": {
      "default": "",
      "description": "One-sentence plain-language summary of what this artifact does, accessible to non-experts. Used only in the per-artifact README, not in downstream prompts.",
      "maxLength": 250,
      "minLength": 80,
      "title": "Layman Summary",
      "type": "string"
    },
    "summary": {
      "default": "",
      "description": "Summary for downstream artifacts: what this artifact provides",
      "maxLength": 5000,
      "minLength": 500,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ResearchExpectedFiles",
      "description": "All output files you created. Must include research_out.json with your research findings."
    },
    "upload_ignore_regexes": {
      "description": "Regex patterns for workspace paths that must NOT be published to the GitHub repo, matched against each file's path relative to this artifact's workspace root (POSIX form, e.g. 'cache/abc.json'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    },
    "answer": {
      "description": "Comprehensive answer with NUMBERED CITATIONS. Cite sources by number: 'Claim [1].' or 'According to [2, 3]...'",
      "title": "Answer",
      "type": "string"
    },
    "sources": {
      "description": "All sources used, with index matching citation numbers in answer",
      "items": {
        "$ref": "#/$defs/Source"
      },
      "title": "Sources",
      "type": "array"
    },
    "follow_up_questions": {
      "description": "2-3 follow-up questions that emerged from the investigation",
      "items": {
        "type": "string"
      },
      "title": "Follow Up Questions",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files",
    "answer",
    "sources",
    "follow_up_questions"
  ],
  "title": "ResearchArtifact",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `/home/adrian/projects/ai-inventor/aii_data/users/uitest-20260731/runs/run_C4UvEedrrr_P/3_invention_loop/iter_1/gen_art/gen_art_research_1/.sdk_openhands_agent_struct_out.json` exists and contains JSON matching the schema above.

Can a tiny learned router pick between two decoding strategies per prompt to beat always using either one alone?
````

### [5] SYSTEM-USER prompt · 2026-07-31 21:11:47 UTC

```
<verification_failed>
Your research output failed verification (attempt 1/10).
</verification_failed>

<schema_errors>
JSON SCHEMA ERRORS:
  - research_out.json: Invalid JSON - Expecting ',' delimiter: line 69 column 38 (char 3062)

Fix: research_out.json must have:
     {
       "answer": "comprehensive answer with [1], [2] citations",
       "sources": [{"index": 1, "url": "...", "title": "...", "summary": "..."}],
       "follow_up_questions": ["Question 1?", "Question 2?"],
       "summary": "what was found"
     }

     Each citation [N] in answer MUST match a source with that index.
</schema_errors>

<task>
FIX ISSUES:
1. Output valid research_out.json with all required fields
2. Ensure every factual claim has a numbered citation [1], [2], etc.
3. Ensure every source has a matching citation in the answer
</task>
```

### [6] SYSTEM-USER prompt · 2026-07-31 21:23:05 UTC

```
<verification_failed>
Your research output failed verification (attempt 2/10).
</verification_failed>

<schema_errors>
JSON SCHEMA ERRORS:
  - research_out.json: Missing required 'title' field

Fix: research_out.json must have:
     {
       "answer": "comprehensive answer with [1], [2] citations",
       "sources": [{"index": 1, "url": "...", "title": "...", "summary": "..."}],
       "follow_up_questions": ["Question 1?", "Question 2?"],
       "summary": "what was found"
     }

     Each citation [N] in answer MUST match a source with that index.
</schema_errors>

<content_warnings>
CONTENT ISSUES:
  - research_out.json: 'title' is too short

Fix: Ensure answer is comprehensive, has proper citations, and all sources are cited.
</content_warnings>

<task>
FIX ISSUES:
1. Output valid research_out.json with all required fields
2. Ensure every factual claim has a numbered citation [1], [2], etc.
3. Ensure every source has a matching citation in the answer
</task>
```
