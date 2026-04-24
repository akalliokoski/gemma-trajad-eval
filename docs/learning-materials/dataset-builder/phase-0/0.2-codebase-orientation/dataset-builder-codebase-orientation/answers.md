# Dataset builder codebase orientation

Source topic: Phase 0 → Orientation → 0.2 Codebase orientation in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`

## Questions and answers

### 1) What does `download_hermes.py` do, and why is it intentionally small?
`download_hermes.py` is the ingestion edge of the pipeline. It does one job: fetch a Hugging Face dataset split with `datasets.load_dataset()`, stream each row to JSONL, and save it under `data/raw/`.

Its single responsibility is deliberate. The file defines dataset IDs, an output directory, a `download()` helper, and a tiny CLI for `filtered`, `original`, or `both`. It does not inspect schema, normalize records, or create labels. That separation matters because download failures, schema drift, and label logic should be debugged in different places.

In practical terms, this file translates “remote dataset object” into “raw local JSONL snapshot.” Everything later in the builder depends on that frozen raw artifact.

### 2) What does `inspect_traces.py` do, and what data types does it move through?
`inspect_traces.py` is the exploratory analysis tool for raw or normalized trajectory files. Its `load_jsonl()` function returns `list[dict]`: a full in-memory Python list where each element is one parsed JSON object from the file.

That means the script is working with plain Python dicts and lists, not a Hugging Face `Dataset` object. JSONL on disk is line-oriented serialized text; once loaded here, it becomes normal Python containers.

From there, helper functions treat each record as “some dict that might store a trajectory.” `get_trajectory()` checks `conversations`, then `trajectory`, then `messages`. `get_role()` and `get_content()` similarly accept either normalized keys (`role`, `content`) or ShareGPT-style keys (`from`, `value`). The script then computes summary statistics like trajectory lengths, role counts, tool-call prevalence, and `<think>` usage.

It now also supports focused reports for the next implementation phase:
- `--schema-report` to describe detected trajectory/message shapes
- `--tool-stats` to summarize tool-call density
- `--eligibility-report` to estimate which perturbation rules are structurally likely to fire

The important learning point is that `inspect_traces.py` is not part of the label-producing pipeline. It is the codebase’s microscope.

### 3) Why does `inspect_traces.py` auto-detect the trajectory field name?
It auto-detects because this repo touches more than one schema layer:

1. raw Hermes traces often use `conversations`
2. normalized records use `trajectory`
3. some external or future sources may use `messages`

If inspection assumed exactly one field name, the EDA tool would only work on one representation and would become brittle as soon as the source or downstream format changed. Auto-detection lets one script inspect raw ShareGPT-like input and normalized internal output.

That is important in this repo because Phase 0 explicitly wants the learner to compare raw data and normalized data. A flexible inspection script makes that comparison cheap.

### 4) What transformations happen in `normalize_trajectory.py`?
`normalize_trajectory.py` is the schema bridge from raw Hermes traces to the internal builder format.

The main transformations are:

- detect the trajectory array under `conversations`, `trajectory`, or `messages`
- map roles through `ROLE_MAP`
  - `human` → `user`
  - `gpt` → `assistant`
  - `system` and `tool` stay the same
- convert each message into a normalized `{role, content}` pair
- extract metadata fields such as `category`, `subcategory`, `source`, `task_type`, and `difficulty`
- derive cheap structural metadata like `trajectory_length`, `tool_call_count`, `tool_response_count`, and `has_think`
- add label fields initialized for a clean example:
  - `is_anomalous = false`
  - `anomaly_type = null`
  - `bad_step = null`
  - `generation_rule = null`

So what comes in is a source-specific raw dict. What comes out is a uniform record that downstream perturbation, splitting, and validation code can rely on.

### 5) Why is `source_trace_id` assigned with a hash fallback?
`source_trace_id` is the stable identity of the original trace. The code first prefers a source-provided `id` or `source_id`. If neither exists, it hashes the raw trajectory content with SHA-256 and keeps the first 16 hex characters.

The point is reproducibility. Later, `build_trajad_dataset.py` assigns train/dev/test splits by `source_trace_id`, not by per-variant record ID. If this identity changed across runs, the same original trace could land in different splits on different builds, which would quietly break reproducibility and leakage protection.

So the hash is not decoration. It is the fallback that preserves stable split grouping even when the upstream data lacks a ready-made ID.

### 6) What is the `var_00` suffix convention, and when does it change?
During normalization, every clean record gets an ID like `trace_000123_var_00`. The `var_00` suffix means “this is the original normal variant.”

Later, `apply_perturbation()` in `perturbations.py` replaces that provisional ID with a source-trace-based variant ID like `hermes_abc123_var_04`. The suffix changes when a perturbation rule successfully creates an anomalous variant.

Conceptually:
- `var_00` = canonical clean baseline
- `var_01`, `var_02`, ... = synthetic anomaly variants derived from the same source trace

That convention makes variant families easy to reason about while keeping the split anchor fixed at `source_trace_id`.

### 7) What is the contract of `apply_perturbation(record, rule_fn)` in `perturbations.py`?
The practical contract is: take one normalized clean record, attempt a rule-specific mutation, and either return a fully labeled anomalous copy or `None`.

More precisely, `apply_perturbation()`:
- calls a rule like `p1_replace_tool_choice`
- receives either a modified record or `None` if the record is not eligible
- fills in `anomaly_class` from `ANOMALY_TYPE_TO_CLASS`
- rewrites the record ID to a variant-specific ID
- preserves `source_trace_id`

So the return type is effectively `dict | None`, where `None` means “this rule could not meaningfully apply to this trace.”

That is why the build script can count perturbation failures by rule without treating them as crashes.

### 8) For P1 and P2, what actually changes in the trajectory bytes?
Both P1 and P2 modify the JSON embedded inside an assistant message’s `<tool_call>...</tool_call>` block.

For P1 (`p1_replace_tool_choice`):
- the tool-call JSON is parsed
- the `name` field is replaced with a semantically nearby alternative from `NEARBY_TOOLS` or a fallback `name_v2`
- the rest of the assistant message stays in place

For P2 (`p2_mutate_argument_value`):
- the tool-call JSON is parsed
- one argument value inside `arguments` or `parameters` is mutated
- strings get a `_CORRUPTED` suffix
- ints are nudged
- bools are flipped
- lists may become empty

So these rules do not rewrite the whole trajectory. They surgically alter the serialized JSON bytes inside one assistant turn.

### 9) What is `NEARBY_TOOLS` trying to model, and what is its coverage gap?
`NEARBY_TOOLS` models plausible tool confusion rather than random nonsense. It says that if an agent should have used one tool, an error may instead choose an adjacent-but-wrong tool in the same conceptual neighborhood.

Examples in the mapping include:
- `search_web` ↔ `search_wikipedia` / `search_news`
- `read_file` ↔ `list_directory` / `read_csv` / `read_json`
- `run_python` ↔ `run_bash` / `execute_code`

The gap is coverage. The mapping is hand-written and only covers a small tool vocabulary. If a tool name is unseen, the fallback is to append `_v2`, which preserves the “wrong tool” idea mechanically but is much less semantically realistic.

So the map is a useful MVP approximation, not a complete ontology of tool confusion.

### 10) Why does the repo distinguish `MVP_RULES` from `ALL_RULES`?
`MVP_RULES` is the short, safer subset: P1–P4. `ALL_RULES` adds the more ambitious behaviors like unnecessary continuation, contradiction, premature final answer, and step swapping.

This split exists for practical iteration. The builder can produce an initial dataset with the simpler rules first, then widen coverage once later rules are judged realistic enough. It is a way to trade recall for trustworthiness during early development.

For a first home-lab project, that is a very sane pattern: start with robust rules that are easy to inspect, then add complexity only after validation catches up.

### 11) What does `build_trajad_dataset.py` contribute beyond “call every rule”?
It is the orchestration layer for the full supervised dataset build.

Its responsibilities are:
- load normalized clean records from `data/interim/`
- apply one or more perturbation rules to each clean record
- run the lightweight coherence screen
- combine clean and anomalous examples
- assign train/dev/test splits by `source_trace_id`
- write `train.jsonl`, `dev.jsonl`, `test.jsonl`, and `all.jsonl`
- write a `build_manifest.json` that records rules used, counts, and rejection diagnostics

In other words, it is the repo’s dataset assembly line.

### 12) Why does split assignment by `source_trace_id` prevent leakage?
Leakage would happen if one source trace and its perturbed siblings were split across training and evaluation sets. Then the model could see near-duplicates of the same trace family during training and testing.

The script prevents that by shuffling unique source IDs first, assigning IDs to train/dev/test, and only then placing each record according to its source ID. That keeps all variants of one trace family together.

This is exactly the right policy for perturbation-derived datasets, because the clean baseline and anomaly variants are not independent examples.

### 13) What does `validate_labels.py` check, and what does it not check?
It checks structural and label consistency, including:
- required top-level fields
- non-empty `trajectory`
- valid roles (`system`, `user`, `assistant`, `tool`)
- boolean `is_anomalous`
- normal-record nullability rules
- anomalous-record presence and validity of `bad_step`, `anomaly_type`, and `anomaly_class`
- valid split names
- some rule-aware `bad_step` semantics for P4, P5, and P7

What it does not check is equally important:
- it does not judge whether a perturbation is semantically realistic
- it does not verify that the model-facing trajectory “feels natural”
- it does not deeply validate embedded tool-call JSON beyond what the rules themselves enforce
- it does not run manual-review quality criteria

So the validator is a schema-and-contract checker, not a realism oracle.

### 14) Which anomaly types are listed as valid but have no perturbation rule yet?
The valid anomaly types list includes three types without a generation rule in `ALL_RULES`:

1. `hallucinated_tool`
2. `invalid_tool_json`
3. `unnecessary_replanning`

That tells the learner two things. First, the taxonomy is broader than the current generator coverage. Second, the codebase already anticipates future extensions, but it has not implemented them yet.

## Key takeaway for this project
The Phase 0.2 codebase is intentionally modular. Downloading, inspection, normalization, perturbation, building, and validation each have a narrow job. The most important design threads running across the files are schema translation, stable source identity, leakage-safe grouping, and explicit separation between “structurally valid” and “semantically realistic.”

## Sources
- `dataset_builder/download_hermes.py`
- `dataset_builder/inspect_traces.py`
- `dataset_builder/normalize_trajectory.py`
- `dataset_builder/perturbations.py`
- `dataset_builder/build_trajad_dataset.py`
- `dataset_builder/validate_labels.py`
- `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
- `docs/codebase-baseline.md`
- `docs/data-pipeline-walkthrough.md`
