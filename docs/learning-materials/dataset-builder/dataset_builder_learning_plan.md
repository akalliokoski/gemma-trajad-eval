# Dataset Builder — Learning Plan

**Scope:** `dataset_builder/` only (Subproject A). This is not a training plan for Subproject B.

**Active scope note (2026-04-26):** for the current pass, this learning plan is intentionally narrowed to **Phase 0 + Phase 1 understanding work**. Fine-tuning, SFT execution, and RL/GRPO are being kept for later on purpose; see [`docs/deferred-training-roadmap.md`](../../deferred-training-roadmap.md), [`docs/binary-sft-handoff.md`](../../binary-sft-handoff.md), and [`docs/training-smoke-test-audit.md`](../../training-smoke-test-audit.md).

**Format:** Hierarchical. Leaf tasks are sized for ~30 minutes each — enough to read,
run, or implement one thing fully. Every task either teaches a concept, runs something,
or produces a concrete artefact.

---

## Goals

### Primary goal
Understand the entire `dataset_builder` pipeline deeply — not just "it works" but *why*
each design decision was made — by actually running it, breaking it, and extending it.

### Learning goals
- Understand trajectory anomaly detection as a problem domain (agent traces, not GPS)
- Understand the TrajAD paper's dataset construction methodology
- Learn how synthetic perturbation is used to create ground-truth labels
- Learn the HuggingFace `datasets` library for custom pipelines
- Understand data-leakage prevention in train/test splits
- Learn schema validation patterns for ML datasets
- Learn to measure and report dataset quality

### Active deliverable goals for the current pass
- Raw Hermes filtered traces downloaded locally
- `inspect_traces.py` used to produce empirical Phase 1 notes
- Manual understanding of tool-call structure and perturbation eligibility
- A clean handoff point where dataset understanding is ahead of model-training execution

### Longer-horizon subproject goals (not all part of the current pass)
- All 6 pipeline stages running end-to-end, validated
- Perturbation diagnostics script (success rates per rule)
- Stage A4 manual-review CLI (100–150 samples reviewed)
- Test suite for `normalize_trajectory.py`, `perturbations.py`, `validate_labels.py`
- At least one new or improved perturbation rule (P9: `invalid_tool_json`)
- Dataset ready for HuggingFace Hub publication

---

## Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Perturbation realism — synthetic anomalies are too obvious, trivially detectable, or semantically nonsensical | Medium | High | Manual review (Phase 5); compare to TrajBench paper quality criteria |
| Hermes data format drift — the dataset on HF Hub has evolved since code was written | Low | Medium | Run inspect_traces.py immediately after download; add format assertions |
| Train/test leakage — variants of the same trace appear in both train and test | Low (code is correct) | High | Write an explicit leakage test in Phase 6 |
| Class imbalance — if many perturbation rules fail silently, real ratio diverges from expectation | Medium | Medium | Diagnostics script in Phase 4; compare to TrajBench 1:1 ratio |
| HF Hub authentication — download or push blocked by token expiry | Low | Low | Keep `HF_TOKEN` in `.env`; test login in Phase 0 |
| Missing stub anomaly types create holes in the taxonomy | Low | Medium | Implement `invalid_tool_json` (P9) in Phase 3; document decision on the other two |
| M3/MPS issues during tokenization preview | Low (Phase 7 only) | Low | Use `mlx-lm` for any on-device tokenization; avoid `transformers` + MPS |

---

## Hardware notes (M3 32 GB)

- **Phases 0–6** (pure Python data pipeline): No GPU/MPS needed. Everything runs in
  Python with standard I/O. The 32 GB unified memory is more than sufficient for the
  ~36K-record dataset.
- **Phase 7** (HF publication + optional tokenization preview): If you want to preview
  how a trajectory looks as tokens, use `mlx_lm.load()`, not `AutoTokenizer` +
  `torch.mps`. MPS has no advantage here and adds unnecessary complexity.
- **Multiprocessing**: M3 has 12 performance cores. For large-scale perturbation (if
  you later extend to the full Hermes reasoning traces dataset), `multiprocessing.Pool`
  will give linear speedup. Start with single-process for correctness, parallelize later.

---

## Reference materials (read these as you reach the relevant phase)

| Resource | When to read | Key takeaway for this project |
|----------|-------------|-------------------------------|
| [TrajAD paper (arxiv 2602.06443)](https://arxiv.org/abs/2602.06443) | Phase 0 | TrajBench construction method; perturbation + LLM completion strategy |
| [LM-TAD (arxiv 2409.15366)](https://arxiv.org/abs/2409.15366) | Phase 0 | How trajectories are represented as token sequences for LMs |
| [HF Datasets: create dataset guide](https://huggingface.co/docs/datasets/en/create_dataset) | Phase 7 | Builder classes, `load_dataset("json", ...)`, push_to_hub |
| [HF Datasets: repository structure](https://huggingface.co/docs/datasets/en/repository_structure) | Phase 7 | YAML frontmatter, split naming, Parquet auto-conversion |
| [HF Datasets: dataset cards](https://huggingface.co/docs/hub/datasets-cards) | Phase 7 | What a complete dataset card includes |
| [Detecting Silent Failures (arxiv 2511.04032)](https://arxiv.org/html/2511.04032) | Phase 3 | Alternative anomaly taxonomy for agent traces (structural vs. semantic) |
| [DJLougen/hermes-agent-traces-filtered](https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered) | Phase 1 | Browse dataset card before downloading; read the field descriptions |
| [`docs/labeling-guidelines.md`](labeling-guidelines.md) | Phase 5 | Review criteria for manual annotation |

---

## Phase 0 — Orientation

**Goal:** Understand the domain and the codebase before running anything.

### 0.1 Domain background (~90 min total)

- [x] **Read TrajAD abstract, introduction, and related work** (~30 min)
  - Focus answer: in the agent context, trajectory anomaly detection means auditing an agent's full execution trace — instruction plus reasoning, actions/tool calls, and observations — to detect anomalies and localize the first erroneous step.
  - GPS contrast: GPS trajectory anomaly detection looks for unusual movement in physical space, while agent trajectory anomaly detection looks for procedural failures in task execution such as bad reasoning, bad tool use, loops, or unwarranted continuation.
  - TrajBench note: TrajBench is built with perturb-and-complete, meaning it injects an error and then continues the trajectory from that corrupted state so downstream behavior stays realistic; this is richer than plain one-step perturbation.
  - Q&A notes: [answers.md](learning-materials/dataset-builder/phase-0/0.1-domain-background/trajectory-anomaly-detection/answers.md)
  - Infographic: [PNG](learning-materials/dataset-builder/phase-0/0.1-domain-background/trajectory-anomaly-detection/infographic.png)
  - Podcast: [local MP3](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.1-domain-background/trajectory-anomaly-detection/phase-0_0.1-01_trajectory-anomaly-detection.mp3) · [Audiobookshelf UI](https://vps.taild96651.ts.net:13378/)
  - Video explainer: [local MP4](file:///data/jellyfin/videos/ai-generated/notebooklm-style-explainers/2026-04-21_dataset-builder-phase-0-1-trajectory-anomaly-detection/2026-04-21_dataset-builder-phase-0-1-trajectory-anomaly-detection.mp4) · [Jellyfin UI](https://vps.taild96651.ts.net:8096/)

- [x] **Read TrajAD section 3: dataset construction and anomaly taxonomy** (~30 min)
  - Focus answer: TrajAD organizes anomalies into Task Failure, Process Inefficiency, and Unwarranted Continuation, and TrajBench uses six perturbation families that become more realistic because the paper uses perturb-and-complete rather than one-step corruption.
  - Quality bar: the reported 96.2% anomaly-classification agreement and 94.5% first-error-localization agreement are the benchmark this repo should keep in mind for later manual review.
  - Q&A notes: [answers.md](learning-materials/dataset-builder/phase-0/0.1-domain-background/dataset-construction-and-anomaly-taxonomy/answers.md)
  - Infographic: [PNG](learning-materials/dataset-builder/phase-0/0.1-domain-background/dataset-construction-and-anomaly-taxonomy/infographic.png)
  - Podcast: [local MP3](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.1-domain-background/dataset-construction-and-anomaly-taxonomy/phase-0_0.1-02_dataset-construction-and-anomaly-taxonomy.mp3) · [Audiobookshelf UI](https://vps.taild96651.ts.net:13378/)

- [x] **Browse the Hermes filtered traces HF dataset card + dataset viewer** (~30 min)
  - Focus answer: the dataset is a tool-heavy ShareGPT-style corpus with `conversations` stored as `{from, value}` messages; typical traces are about 32 messages long, roles are `system`, `human`, `gpt`, and `tool`, and tool use is the dominant structural pattern.
  - Structural note: tool calls and tool responses are serialized inside message text with `<tool_call>` / `<tool_response>` markup, so downstream normalization has to reconstruct structure before perturbation or validation.
  - Q&A notes: [answers.md](learning-materials/dataset-builder/phase-0/0.1-domain-background/hermes-filtered-traces-dataset-card-and-viewer/answers.md)
  - Infographic: [PNG](learning-materials/dataset-builder/phase-0/0.1-domain-background/hermes-filtered-traces-dataset-card-and-viewer/infographic.png)
  - Podcast: [local MP3](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.1-domain-background/hermes-filtered-traces-dataset-card-and-viewer/phase-0_0.1-03_hermes-filtered-traces-dataset-card-and-viewer.mp3) · [Audiobookshelf UI](https://vps.taild96651.ts.net:13378/)

### 0.2 Codebase orientation (~120 min total)

- [x] **Read `download_hermes.py` + `inspect_traces.py`** (~30 min)
  - Focus answer: `download_hermes.py` is the ingestion edge that freezes a remote HF dataset into local JSONL, while `inspect_traces.py` is the EDA microscope that works over plain Python `list[dict]` records and can inspect either raw `conversations` or normalized `trajectory` data.
  - Key design note: inspect_traces auto-detects `conversations`, `trajectory`, and `messages` so one script can inspect multiple schema layers instead of breaking on raw-vs-normalized differences.
  - Q&A notes: [answers.md](learning-materials/dataset-builder/phase-0/0.2-codebase-orientation/dataset-builder-codebase-orientation/answers.md)
  - Infographic: [PNG](learning-materials/dataset-builder/phase-0/0.2-codebase-orientation/dataset-builder-codebase-orientation/infographic.png)
  - Podcast: [local MP3](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.2-codebase-orientation/dataset-builder-codebase-orientation/phase-0_0.2-01_dataset-builder-codebase-orientation.mp3) · [Audiobookshelf UI](https://vps.taild96651.ts.net:13378/)

- [x] **Read `normalize_trajectory.py`** (~30 min)
  - Key takeaway: normalization is the schema bridge from ShareGPT-like `{from, value}` messages to internal `{role, content}` trajectories, and `source_trace_id` exists to keep split assignment stable and leakage-safe across rebuilds.
  - `var_00` means the clean baseline record; later perturbation variants replace it with `var_01+` IDs while keeping the same `source_trace_id` family.

- [x] **Read `perturbations.py`** (~30 min)
  - Key takeaway: `apply_perturbation(record, rule_fn) -> dict | None` is a bounded mutation contract that either returns a fully labeled anomalous variant or signals inapplicability with `None`.
  - P1/P2 make surgical edits inside serialized `<tool_call>` JSON, `NEARBY_TOOLS` models plausible wrong-tool confusion, and the `MVP_RULES` / `ALL_RULES` split lets the builder trade rule coverage against early-stage trustworthiness.

- [x] **Read `build_trajad_dataset.py` + `validate_labels.py`** (~30 min)
  - Key takeaway: split assignment by `source_trace_id` prevents train/test leakage across clean-plus-variant trace families, while `validate_labels.py` checks schema and some rule-aware localization semantics but not full semantic realism.
  - The valid-but-unimplemented anomaly types remain `hallucinated_tool`, `invalid_tool_json`, and `unnecessary_replanning`.

### 0.3 Environment setup (~60 min total)

- [x] **Create and activate the Python environment** (~20 min)
  - Canonical plan path: `python3 -m venv .venv && source .venv/bin/activate` followed by `pip install -e ".[dev]"`.
  - Repo-specific note: on this VPS, the practical documented path used `uv` to create `.venv` because system `pip` under `/usr/bin/python3` was unavailable.
  - Q&A notes: [answers.md](learning-materials/dataset-builder/phase-0/0.3-environment-setup/dataset-builder-environment-setup/answers.md)
  - Infographic: [PNG](learning-materials/dataset-builder/phase-0/0.3-environment-setup/dataset-builder-environment-setup/infographic.png)
  - Podcast: [local MP3](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.3-environment-setup/dataset-builder-environment-setup/phase-0_0.3-01_dataset-builder-environment-setup.mp3) · [Audiobookshelf UI](https://vps.taild96651.ts.net:13378/)

- [x] **Configure HuggingFace authentication** (~15 min)
  - The Hermes filtered dataset is public, so auth is mainly future-facing setup for later upload/publication work rather than a blocker for early download and inspection.
  - Expected flow: `pip install huggingface-hub`, `huggingface-cli login`, `huggingface-cli whoami`.

- [x] **Verify directory structure exists** (~10 min)
  - The pipeline’s on-disk contract is `data/raw/` -> `data/interim/` -> `data/processed/`.
  - Directory creation command: `mkdir -p data/{raw,interim,processed}`.

---

## Phase 1 — Data Acquisition & Exploration

**Goal:** Get the raw data onto disk and understand its structure empirically, not just from the docs.

**Stop line for the current pass:** once Phase 1.1–1.3 are complete and documented, pause here. Do not expand this learning-path run into model training; the later path is documented in [`docs/deferred-training-roadmap.md`](../../deferred-training-roadmap.md).

### 1.1 Download (~30 min)

- [x] **Run `download_hermes.py --dataset filtered`** (~20 min)
  - Verified with `uv run python dataset_builder/download_hermes.py --dataset filtered`.
  - Output confirmed: `data/raw/hermes_filtered.jsonl` with `3,679` rows and about `368 MB` on disk.

- [x] **Open one raw JSONL record in a JSON viewer/pretty-printer** (~15 min)
  - A compact pretty-printed preview was saved to [sample-record.json](phase-1/1.1-1.3-raw-data-and-trace-eda/hermes-filtered-traces-phase-1-understanding/sample-record.json).
  - Stable top-level fields observed: `id`, `conversations`, `tools`, `category`, `subcategory`, `task`.
  - Raw messages use `{from, value}` and the exact raw roles are `system`, `human`, `gpt`, and `tool`.

### 1.2 EDA with `inspect_traces.py` (~60 min)

- [x] **Run the full summary** (~20 min)
  - Verified with `uv run python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --schema-report --tool-stats --eligibility-report`.
  - Core results: `3,679` records, trajectory length min `5`, max `54`, average about `32.1`, plus category and role summaries.
  - Combined artifact package: [README](phase-1/1.1-1.3-raw-data-and-trace-eda/hermes-filtered-traces-phase-1-understanding/README.md) · [answers.md](phase-1/1.1-1.3-raw-data-and-trace-eda/hermes-filtered-traces-phase-1-understanding/answers.md) · [PNG](phase-1/1.1-1.3-raw-data-and-trace-eda/hermes-filtered-traces-phase-1-understanding/infographic.png) · [Podcast](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-1-understanding/1.1-1.3-raw-data-and-trace-eda/hermes-filtered-traces-phase-1-understanding/phase-1_1.1-1.3-01_hermes-filtered-traces-phase-1-understanding.mp3)

- [x] **Study role distribution results** (~20 min)
  - `100.0%` of traces have at least one tool call.
  - `99.4%` have at least two assistant/tool-call pairs.
  - This confirms that tool-interaction perturbations are aimed at the core structure of the corpus, not a fringe subset.

- [x] **Manually read 5 complete traces** (~30 min)
  - Verified with `uv run python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl --sample 5`.
  - Representative tasks include config recovery, GraphQL endpoint creation, todo-driven project continuation, background service management, and API documentation work.
  - Key pattern: traces are compound work loops that chain multiple tools rather than isolated one-shot tool calls.

### 1.3 Understand tool call structure (~60 min)

- [x] **Study how tool calls are embedded in assistant messages** (~30 min)
  - Tool calls appear as serialized JSON inside `<tool_call>...</tool_call>` wrappers in assistant messages.
  - Tool outputs appear as serialized JSON inside `<tool_response>...</tool_response>` wrappers in tool messages.
  - Key takeaway: the structure is real but serialized inside text, which is why normalization is essential.

- [x] **Count traces eligible for each perturbation rule** (~30 min)
  - Inspector report snapshot: `P1 3679/3679`, `P2 3678/3679`, `P3/P4/P5 3679/3679`, `P8 3658/3679`.
  - Practical conclusion: eligibility is broad across the corpus; the harder quality problem is perturbation realism, not missing tool structure.

---

## Phase 2 — Normalization Deep Dive

**Goal:** Run normalization, verify output correctness, and understand every design decision.

### 2.1 Run normalization and verify output (~60 min)

- [x] **Run `normalize_trajectory.py`** (~20 min)
  - Verified with `uv run python dataset_builder/normalize_trajectory.py data/raw/hermes_filtered.jsonl data/interim/hermes_normalized_phase2.jsonl`.
  - Result: `3,679` normalized records, `0` errors, row count preserved.

- [x] **Spot-check 10 normalized records** (~30 min)
  - Side-by-side sample saved to [raw-vs-normalized-sample.json](phase-2/2.1-2.2-normalization-deep-dive/hermes-normalization-deep-dive/raw-vs-normalized-sample.json).
  - Verified: role names mapped correctly, `source_trace_id` assigned, clean-label defaults preserved, and metadata populated with structural fields.
  - Combined artifact package: [README](phase-2/2.1-2.2-normalization-deep-dive/hermes-normalization-deep-dive/README.md) · [answers.md](phase-2/2.1-2.2-normalization-deep-dive/hermes-normalization-deep-dive/answers.md) · [PNG](phase-2/2.1-2.2-normalization-deep-dive/hermes-normalization-deep-dive/infographic.png) · [Podcast](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-2-understanding/2.1-2.2-normalization-deep-dive/hermes-normalization-deep-dive/phase-2_2.1-2.2-01_hermes-normalization-deep-dive.mp3)
  - The current corpus did **not** produce a partial/missing-metadata sample; that absence is itself documented as a finding.

- [x] **Understand source_trace_id stability** (~20 min)
  - Stability audit saved to [normalization-stability-and-edge-cases.json](phase-2/2.1-2.2-normalization-deep-dive/hermes-normalization-deep-dive/normalization-stability-and-edge-cases.json).
  - Repeated checks confirmed `stable_on_repeat: true`.
  - Key insight confirmed: split assignment depends on stable trace-family identity, so deterministic `source_trace_id` is a data-leakage safeguard, not just a convenience.

### 2.2 Edge cases (~60 min)

- [x] **Find and examine records with non-standard role names** (~30 min)
  - Observed raw roles: `gpt`, `human`, `system`, `tool`.
  - Observed normalized roles: `assistant`, `user`, `system`, `tool`.
  - No non-standard role names were found in this corpus snapshot, so `normalize_role()` cleanly covers the observed role inventory.

- [x] **Find records that stress the metadata extraction** (~30 min)
  - Edge-case audit found `missing_category_count: 0`, `missing_subcategory_count: 0`, and `empty_metadata_count: 0`.
  - Practical takeaway: the graceful metadata-extraction path still matters, but this specific filtered corpus is cleaner than the hypothetical missing-metadata edge case suggested.

---

## Phase 3 — Perturbation Engine

**Goal:** Understand each perturbation rule deeply, measure success rates, and implement a missing rule.

> **Why study rules one by one?** Each rule represents a specific failure mode hypothesis.
> When the model later fails to detect a certain anomaly type, you'll want to know if the
> problem is in the perturbation quality (too easy/hard) or in the model. You can't diagnose
> this without understanding the rules at code level.

### 3.1 Domain context (~60 min)

- [x] **Re-read TrajAD perturbation strategy vs. this project** (~30 min)
  - TrajAD's `perturb-and-complete` strategy regenerates steps `K+1..N` after the injected error, while this repo's direct perturbation edits step `K` and usually leaves later steps unchanged.
  - Main tradeoff: direct perturbation is deterministic and easy to inspect, but it is weaker on downstream realism because later steps may still assume the clean world state.
  - Key failure-mode examples: P6 `contradicted_tool_result` and P7 `premature_final_answer` are useful anomalies, but they also expose the realism limit of one-step editing.

- [x] **Study the TrajAD anomaly taxonomy and compare to this project** (~30 min)
  - TrajAD's top-level classes remain Task Failure, Process Inefficiency, and Unwarranted Continuation.
  - This repo currently maps `10` anomaly subtypes into those three classes, with `9` implemented perturbation rules after the addition of P9 `invalid_tool_json`.
  - Current stub subtypes are `hallucinated_tool` and `unnecessary_replanning`, which means Task Failure is best covered while continuation/replanning realism is still thinner.
  - Combined artifact package: [README](phase-3/3.1-domain-context/trajad-perturbation-context/README.md) · [answers.md](phase-3/3.1-domain-context/trajad-perturbation-context/answers.md) · [PNG](phase-3/3.1-domain-context/trajad-perturbation-context/infographic.png) · [Podcast](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-3-perturbation-engine/3.1-domain-context/trajad-perturbation-context/phase-3_3.1-01_trajad-perturbation-context.mp3)

### 3.2 Walk through each perturbation rule (~4 hours total, 8 × 30 min)

For each rule, do all three steps in one session:
1. Read the rule's code carefully
2. Run `apply_perturbation()` on 3 manually selected records
3. Read both the input and output trajectories to verify the change is correct

- [x] **P1: `replace_tool_choice`** — wrong_tool_choice (~30 min)
  - Real corpus walkthrough saved to [README](phase-3/3.2-rule-walkthroughs/p1-replace-tool-choice-walkthrough/README.md) and [answers.md](phase-3/3.2-rule-walkthroughs/p1-replace-tool-choice-walkthrough/answers.md); sampled before/after cases are in [p1-sample-comparisons.json](phase-3/3.2-rule-walkthroughs/p1-replace-tool-choice-walkthrough/p1-sample-comparisons.json).
  - Mapped example: `read_file -> list_directory` preserved arguments and produced the clearest believable wrong-tool choice; unmapped examples like `search_files -> search_files_v2` and `terminal -> terminal_v2` stayed structurally valid but looked synthetic.
  - Implementation fix discovered during the walkthrough: multi-tool assistant messages were being over-mutated because `replace_tool_call()` rewrote every `<tool_call>` block. The helper now replaces only the first match (`count=1`), with regression coverage in `tests/test_perturbations.py`.
  - Verified with `uv run pytest tests/test_perturbations.py::test_replace_tool_call_only_replaces_first_tool_call_in_message -v` and `uv run pytest tests/test_perturbations.py -v` (`7 passed`).
  - Infographic: [PNG](phase-3/3.2-rule-walkthroughs/p1-replace-tool-choice-walkthrough/infographic.png)
  - Podcast: [local MP3](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-3-perturbation-engine/3.2-rule-walkthroughs/p1-replace-tool-choice-walkthrough/phase-3_3.2-01_p1-replace-tool-choice-walkthrough.mp3) · [Audiobookshelf UI](https://vps.taild96651.ts.net:13378/)

- [ ] **P2: `mutate_argument_value`** — bad_tool_arguments (~30 min)
  - Apply P2 to a trace with a string argument. How does `_CORRUPTED` suffix change the semantics?
  - Apply to a trace with an integer argument. How does `±999` change the semantics?
  - *Question to answer:* Is corrupting by adding `_CORRUPTED` too obvious for the model? What would be subtler?

- [ ] **P3: `remove_step_pair`** — skipped_required_step (~30 min)
  - Apply P3 to a trace. Verify the `(assistant_tool_call, tool_response)` pair is gone.
  - What is the minimum trajectory length for P3 to succeed? What is `bad_step` set to?
  - Does the resulting trajectory still "make sense" narratively? (It won't — that's the point)

- [ ] **P4: `duplicate_tool_step`** — repeated_step (~30 min)
  - Apply P4. Verify the duplicated pair appears at the expected index.
  - Is `bad_step` set to the first occurrence or the second (the duplicate)?
  - *Verify:* the duplicate should have identical content — not a paraphrase, exactly the same bytes

- [ ] **P5: `append_continuation`** — continued_after_sufficient_evidence (~30 min)
  - Apply P5. What fake tool call gets appended?
  - Is the appended step realistic? Does the tool name exist in the trace's established tool set?
  - What is `bad_step` set to? Verify it points to the correct step index.

- [ ] **P6: `contradict_final_answer`** — contradicted_tool_result (~30 min)
  - Apply P6. How does it modify the final assistant message?
  - Is the `[CONTRADICTION]` prefix a realistic signal, or is it too obvious?
  - *Design question:* An alternative would be to change a factual detail in the conclusion
    while leaving the structure intact. Document this as a potential improvement.

- [ ] **P7: `truncate_before_decision`** — premature_final_answer (~30 min)
  - Apply P7. What gets removed and what fake final answer gets added?
  - What is the resulting trajectory length compared to the original?
  - *Edge case:* what happens if the trace only has 1 tool call step?

- [ ] **P8: `swap_dependent_steps`** — skipped_required_step (~30 min)
  - Apply P8. What two step pairs get swapped?
  - Does the resulting trajectory have an obvious error (step N references results from step N+1
    that the model hasn't seen yet)?
  - Why does P8 produce `skipped_required_step` rather than its own subtype?

### 3.3 Perturbation diagnostics (~60 min)

- [x] **Write a perturbation diagnostics script** (~30 min)
  - Implemented `dataset_builder/perturbation_diagnostics.py` and generated `data/processed/perturbation_diagnostics.json`.
  - Learning package saved in `phase-3/3.3-perturbation-diagnostics/rule-diagnostics-script/` with answer doc, infographic, podcast, and diagnostics snapshot.
  - Verification: `uv run pytest tests/test_perturbation_diagnostics.py -v`; `uv run pytest tests/test_perturbation_diagnostics.py tests/test_perturbations.py -v`; `uv run python dataset_builder/perturbation_diagnostics.py --input data/interim/hermes_normalized_phase2.jsonl --output data/processed/perturbation_diagnostics.json`.
  - First corpus result on 3,679 records: `P1 86.2% (509 failures)`, `P2 99.1% (32 failures)`, all other rules `100.0%` on eligible records.

- [x] **Analyze low-success rules and improve NEARBY_TOOLS coverage** (~30 min)
  - Completed in `phase-3/3.3-perturbation-diagnostics/p1-realism-and-nearby-tools-coverage/` with corpus-wide before/after diagnostics in `p1-realism-coverage-comparison.json`.
  - Added curated Hermes-corpus mappings for `search_files`, `terminal`, `browser_snapshot`, `browser_console`, `browser_get_images`, and `browser_scroll`.
  - Removed the generic `_v2` fallback entirely; unmapped tools now skip P1 instead of fabricating fake API names.
  - Added argument adaptation for `search_files -> terminal` and `terminal -> execute_code` so replacement calls better match the target tool.
  - Before/after on 3,679 normalized records: `P1 success 3679 -> 3170`, `fake _v2 outputs 509 -> 0`.

### 3.4 Implement missing anomaly type: P9 invalid_tool_json (~60 min)

- [ ] **Design P9: `invalidate_tool_json`** (~30 min)
  - Read the `parse_tool_call()` and `replace_tool_call()` helpers
  - Design a function that takes a valid `<tool_call>{"name": "...", "arguments": {...}}</tool_call>`
    and produces one with a specific JSON corruption. Options:
    - Remove closing brace: `{"name": "search_web", "arguments": {"q": "Paris"` ← truncated
    - Add a trailing comma: `{"name": "search_web", "arguments": {"q": "Paris",}}`
    - Use single quotes: `{'name': 'search_web', 'arguments': {'q': 'Paris'}}`
  - Choose the most realistic option (hint: trailing comma is the most common real LLM mistake)
  - Write the function signature and logic on paper/notes before coding

- [ ] **Implement and integrate P9** (~30 min)
  - Implement `invalidate_tool_json(record)` in `perturbations.py`
  - Add it to `ALL_RULES` with rule id `"P9"`
  - Set `anomaly_type="invalid_tool_json"`, `generation_rule="P9"`, `bad_step=<step_index>`
  - Test: apply to 5 traces, verify the JSON is invalid, verify the field is not in the
    `<tool_call>` tag completely, verify validate_labels.py still accepts the record
  - Add a note in the code about why `invalid_tool_json` is excluded from `MVP_RULES`

---

## Phase 4 — Pipeline Assembly & Validation

**Goal:** Run the full pipeline end-to-end, understand the output statistics, and catch quality issues.

### 4.1 Build MVP dataset (~60 min)

- [ ] **Run `build_trajad_dataset.py --mvp`** (~20 min)
  - Observe the class distribution printed to stdout
  - Check file sizes: `data/processed/train.jsonl`, `dev.jsonl`, `test.jsonl`, `all.jsonl`
  - Calculate: how many normal vs. anomalous records in each split?

- [ ] **Verify no train/test leakage by source_trace_id** (~30 min)
  - Write a script that:
    1. Reads all `source_trace_id` values from train, dev, test splits
    2. Checks for any ID that appears in more than one split
    3. Asserts zero overlap
  - *Expected result:* zero overlap (the code is designed for this)
  - *Why this matters:* variants of the same trace in both train and test means the model
    can "memorize" the specific trace structure rather than learning the anomaly pattern

- [ ] **Inspect class distribution and compare to TrajBench** (~20 min)
  - TrajBench: 31,742 normal + 31,742 anomalous (1:1 ratio)
  - Your dataset: normal = ~3,679, anomalous = 3,679 × 4 = ~14,716 (1:4 ratio for MVP with P1–P4)
  - Is this ratio appropriate? What are the implications for model training?
  - Document the decision: keep 1:4 (more anomaly examples = better anomaly detection?) or
    consider downsampling anomalies to 1:1?

### 4.2 Full dataset build (P1–P8 + P9) (~60 min)

- [ ] **Run `build_trajad_dataset.py` with all rules** (~20 min)
  - Compare total counts to MVP run
  - What is the ratio now? How did P9 change the distribution?
  - Check that all 11 anomaly subtypes now have ≥1 example in each split
    (note: `hallucinated_tool`, `unnecessary_replanning` will still have 0 — that's expected)

- [ ] **Analyze per-category balance** (~30 min)
  - Group records by `metadata.category` in train set
  - Is any category over-represented? Does this matter for the anomaly detection task?
  - Is the perturbation rule distribution uniform across categories, or do some categories
    have more successes? (e.g., coding tasks may have richer tool arguments → P2 succeeds more)

- [ ] **Check trajectory length distribution in processed data** (~20 min)
  - Compute min/mean/max/p95 trajectory length in the processed train split
  - Note: this affects how the model will see the data in training (long sequences = more tokens)
  - Check if P7 (truncation) creates very short trajectories that might confuse training

### 4.3 Validation (~60 min)

- [ ] **Run `validate_labels.py --strict` on all splits** (~20 min)
  - Fix any validation errors that appear (there may be none if everything is correct)
  - Understand the difference between `--strict` (exit on error) vs. default (report only)

- [ ] **Identify what validate_labels.py does NOT check** (~30 min)
  - Read `validate_record()` carefully. The current checks are structural (field presence, type)
    not semantic (does `bad_step` actually contain the anomalous content?)
  - Write a list of at least 3 semantic checks that would add value:
    - Example: "for P1 records, does the step at `bad_step` contain a `<tool_call>` block?"
    - Example: "for P2 records, does the tool call at `bad_step` contain `_CORRUPTED`?"
    - Example: "is there an assistant message at position `bad_step`?"

- [ ] **Implement 2 semantic checks in `validate_labels.py`** (~30 min)
  - Add a `validate_semantic_consistency(record)` function
  - Check at minimum: for records with `generation_rule` in {"P1","P2","P3","P4"},
    verify the step at `bad_step` has a `<tool_call>` block in its content
  - This catches bugs like wrong step index assignment

---

## Phase 5 — Manual Review (Stage A4)

**Goal:** Ground-truth quality check on 100–150 samples to measure perturbation realism.

> **Why this matters:** Synthetic perturbations can produce obvious, trivial, or semantically
> broken anomalies. The manual review catches systematic quality problems that automated
> checks miss. The TrajAD paper's 96.2% human agreement rate is your quality benchmark.

### 5.1 Review tooling (~60 min)

- [ ] **Re-read `docs/labeling-guidelines.md`** (~30 min)
  - Understand the acceptance criteria for each anomaly type
  - Note: what makes an anomaly "realistic"? What makes it "too obvious"?
  - What is the criteria for a "bad_step" being correct?

- [ ] **Build a CLI review tool** (~30 min)
  - Write `dataset_builder/manual_review.py` (30–50 lines)
  - Interface: display one record at a time, show step at `bad_step` highlighted, prompt:
    `[a]ccept / [r]eject / [f]lag for discussion / [q]uit`
  - Save decisions to `data/review/review_log.jsonl` with `{id, decision, reviewer_note}`
  - Support resuming (skip already-reviewed records)
  - Use `random.seed(42)` to select a reproducible 150-record sample from the test split

### 5.2 Conduct review (~120 min)

- [ ] **Review 50 samples: rules P1 and P2** (~30 min)
  - Filter to P1 and P2 records. Review 25 of each.
  - Focus question: Is the anomaly realistic? Would it fool a capable model?

- [ ] **Review 50 samples: rules P3 and P4** (~30 min)
  - Filter to P3 and P4 records. Review 25 of each.
  - Focus question: After removing a step pair (P3), does the remaining trajectory make sense
    as a coherent (but flawed) agent trace?

- [ ] **Review 50 samples: rules P5–P9** (~30 min)
  - At least 10 per rule where available. For P9, check that the malformed JSON is
    realistic (not obviously broken in a way no real LLM would produce).
  - Focus question: Do P5 and P6 feel like "real agent mistakes" or "mechanical edits"?

- [ ] **Analyze review results and document findings** (~30 min)
  - Calculate: acceptance rate per rule, most common rejection reason per rule
  - If any rule has <70% acceptance, it needs redesign — document the specific problems
  - Write findings to `data/review/review_summary.md`

### 5.3 Fix issues found in review (~30 min per issue, as needed)

- [ ] **Fix the top problem found in P1 (likely: fallback `_v2` tool names are unrealistic)**
  - Expand `NEARBY_TOOLS` map based on real tool names seen in the dataset
  - Or: for tools with no nearby mapping, make P1 return `None` (skip) rather than using fallback

- [ ] **Fix the top problem found in P6 (likely: `[CONTRADICTION]` prefix is too obvious)**
  - Change P6 to modify the factual content of the final answer rather than prepending a tag
  - Example: if tool returned "Paris", change final answer to say "Berlin" (or some other city)
  - This requires parsing the tool response — more complex, but far more realistic

---

## Phase 6 — Test Suite

**Goal:** Build automated tests that give you confidence the pipeline produces correct output after any change.

> **Learning goal for this phase:** Understand how to test data transformation pipelines —
> not just "does it run?" but "is the output semantically correct?"

### 6.1 Pytest fundamentals (~60 min)

- [ ] **Learn pytest basics** (~30 min)
  - Read: https://docs.pytest.org/en/stable/getting-started.html
  - Understand: test discovery (files named `test_*.py`), fixture system, `assert`
  - Run `pytest --collect-only` to see what tests exist (likely none yet)

- [ ] **Understand fixture-based testing for data pipelines** (~30 min)
  - Learn `@pytest.fixture` for reusable test data
  - Key pattern for this project: create a minimal fake trajectory record as a fixture, then
    test each transformation function against it
  - Understand parametrize: `@pytest.mark.parametrize("role,expected", [("gpt","assistant"), ...])`

### 6.2 Tests for `normalize_trajectory.py` (~90 min)

- [ ] **Write `tests/test_normalize_trajectory.py` — role mapping tests** (~30 min)
  - Test `normalize_role()` for every input: `gpt`, `human`, `tool`, `system`, `assistant`,
    `user`, and an unknown role (expect passthrough or raise?)
  - Use `@pytest.mark.parametrize` for concise coverage

- [ ] **Write tests for `extract_metadata()`** (~30 min)
  - Test: record with all fields present
  - Test: record with no metadata at all (all fields default to `None`)
  - Test: record with metadata nested under a `"metadata"` key
  - Test: record with some but not all metadata fields

- [ ] **Write tests for `normalize_record()`** (~30 min)
  - Create a fixture with a minimal Hermes record
  - Test: output has all required fields
  - Test: `is_anomalous=False`, `anomaly_type=None`, `bad_step=None`
  - Test: `source_trace_id` is stable across two calls on the same input

### 6.3 Tests for `perturbations.py` (~4 hours, 8 × 30 min)

Create a `@pytest.fixture` called `sample_trajectory` that has:
- A system message
- A user message  
- An assistant message with `<tool_call>{"name": "search_web", "arguments": {"query": "test"}}</tool_call>`
- A tool message with `<tool_response>{"result": "test result"}</tool_response>`
- A final assistant message "The answer is test result."

- [ ] **Test P1 (`replace_tool_choice`)** (~30 min)
  - Test: `search_web` gets replaced with a known nearby tool
  - Test: result has `is_anomalous=True`, `anomaly_type="wrong_tool_choice"`, `generation_rule="P1"`
  - Test: record with unknown tool name returns fallback (not None)

- [ ] **Test P2 (`mutate_argument_value`)** (~30 min)
  - Test: string argument gets `_CORRUPTED` appended
  - Test: `bad_step` is the index of the assistant step with the tool call
  - Test: record with no tool arguments returns None

- [ ] **Test P3 (`remove_step_pair`)** (~30 min)
  - Test: tool call pair is absent from output trajectory
  - Test: trajectory length is reduced by 2
  - Test: record with no tool calls returns None

- [ ] **Test P4 (`duplicate_tool_step`)** (~30 min)
  - Test: output trajectory length is original + 2
  - Test: duplicated step has identical content to original
  - Test: `bad_step` points to the duplicate (not the original)

- [ ] **Test P5 (`append_continuation`)** (~30 min)
  - Test: output trajectory is longer than input by 2 steps
  - Test: new last-2 steps contain a `<tool_call>` block
  - Test: `bad_step` is len(original_trajectory)

- [ ] **Test P6 (`contradict_final_answer`)** (~30 min)
  - Test: final assistant message is modified
  - Test: `bad_step` is the index of the final assistant message

- [ ] **Test P7 (`truncate_before_decision`)** (~30 min)
  - Test: output trajectory is shorter than input
  - Test: new final assistant message is a fake conclusion (not a tool call)

- [ ] **Test P8 (`swap_dependent_steps`)** (~30 min)
  - Requires a fixture with ≥2 tool call pairs
  - Test: the order of the two pairs is reversed
  - Test: record with only 1 tool call returns None

### 6.4 Tests for pipeline integrity (~60 min)

- [ ] **Test leakage prevention in split assignment** (~30 min)
  - Create 20 fake normalized records with 5 distinct source_trace_ids
  - Run `build()` and verify all records with the same source_trace_id land in the same split

- [ ] **Test that `validate_labels.py` catches known-bad records** (~30 min)
  - Create records with: missing `trajectory`, `is_anomalous="yes"` (wrong type),
    anomalous record with `bad_step=None`, `bad_step` out of range
  - Verify `validate_record()` returns ≥1 error for each

---

## Phase 7 — HuggingFace Dataset Publication

**Goal:** Prepare the dataset for Hub publication. This is the deliverable for Subproject A.

### 7.1 Learn HF Hub dataset publication (~90 min)

- [ ] **Read the HF Datasets "create dataset" guide** (~30 min)
  - Focus: the `load_dataset("json", data_files=...)` pattern
  - Understand: you do NOT need to write a custom `GeneratorBasedBuilder` for JSONL files
  - Note: `push_to_hub()` auto-converts JSONL to Parquet and generates Croissant metadata

- [ ] **Read the HF repository structure docs** (~30 min)
  - Learn: YAML frontmatter in README.md controls split names, file paths, and feature schema
  - Learn: how `configs` work for multi-config datasets (you may want an `mvp` and `full` config)
  - Study an example from a similar dataset card on the Hub

- [ ] **Read the HF dataset card docs** (~30 min)
  - Understand what fields make a complete dataset card: description, citation, license, 
    homepage, features, splits, size, language
  - Note: the Hub shows dataset statistics automatically if the Parquet conversion succeeds

### 7.2 Prepare dataset for publication (~120 min)

- [ ] **Define the Features schema** (~30 min)
  - Write the `datasets.Features` definition for the dataset
  - Consider: should `anomaly_type` use `ClassLabel` (auto-maps to ints) or `Value("string")`?
  - Consider: should `bad_step` be `int32` with `-1` for normal, or nullable?
  - Note: `None` in JSONL becomes Arrow null, but `ClassLabel` does not support null — use
    `Value("string")` for nullable categorical fields

- [ ] **Write the dataset README / data card** (~30 min)
  - Write `data/processed/README.md` with YAML frontmatter describing:
    - splits: train, validation (dev), test
    - features schema (matching the Features definition above)
    - task_categories: `text-classification`
    - tags: `anomaly-detection`, `agent-trajectories`, `synthetic`, `tool-use`
  - Body should describe: source data, perturbation rules summary, anomaly taxonomy,
    intended use (fine-tuning Gemma for trajectory anomaly detection)

- [ ] **Verify push_to_hub works with a private draft** (~30 min)
  - Create a private draft dataset on HF Hub
  - Run: `ds.push_to_hub("your-username/gemma-trajad-draft", private=True)`
  - Verify: dataset viewer shows records correctly, splits are named correctly,
    feature types match the schema

- [ ] **Write the JSON Schema for the dataset record format** (~30 min)
  - Create `dataset_builder/schema/record.schema.json` (formal JSON Schema v7)
  - This documents the format for external consumers and enables IDE validation
  - Include: field names, types, allowed values for `anomaly_type`, constraints
    (e.g., `bad_step` is null iff `is_anomalous=false`)

---

## Completion criteria

Before considering Subproject A complete, verify all of the following:

- [ ] `python dataset_builder/download_hermes.py --dataset filtered` → `data/raw/hermes_filtered.jsonl`
- [ ] `python dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl` → clean stats output
- [ ] `python dataset_builder/normalize_trajectory.py data/raw/... data/interim/...` → 0 errors
- [ ] `python dataset_builder/build_trajad_dataset.py --mvp --seed 42` → 4 split files
- [ ] `python dataset_builder/validate_labels.py data/processed/train.jsonl --strict` → "All records valid"
- [ ] Perturbation diagnostics script exists and runs
- [ ] 100+ samples manually reviewed, acceptance rate ≥ 70% per rule
- [ ] `pytest tests/` → all tests pass, ≥ 80% coverage on `normalize_trajectory.py` and `perturbations.py`
- [ ] P9 (`invalid_tool_json`) implemented and tested
- [ ] Dataset README / data card written and reviewed
- [ ] Draft dataset visible on HF Hub

---

## Appendix: Key concepts quick reference

**ShareGPT format vs. OpenAI chat format**
- ShareGPT uses `conversations: [{from: "gpt"|"human"|"system", value: "..."}]`
- OpenAI chat uses `messages: [{role: "assistant"|"user"|"system", content: "..."}]`
- This project normalizes both to `trajectory: [{role: "assistant"|"user"|"system"|"tool", content: "..."}]`

**Hermes tool call format** (embedded in assistant messages)
```
<think>Reasoning here...</think>
<tool_call>{"name": "search_web", "arguments": {"query": "capital of France"}}</tool_call>
```
```
<tool_response>{"result": "Paris is the capital of France"}</tool_response>
```

**Why split by source_trace_id, not by record id?**
All variants of a source trace (normal + 4–8 perturbed variants) share the same prefix text.
If they were split randomly, the model would see the normal version at training and the anomalous
version at test — making the test trivially easy (the model just needs to recognize the trajectory
structure, not the anomaly).

**Perturbation success rate math**
With ~3,679 normal records and 4 MVP rules (P1–P4), the maximum possible is 3,679 × 4 = 14,716
anomalous records. Actual will be lower because:
- P1 fails when the tool isn't in NEARBY_TOOLS
- P3/P4 fail when the trace has no tool calls
- P8 fails when the trace has fewer than 2 tool call pairs

The diagnostics script (Phase 4) will give you the actual success rates.

**`bad_step` indexing**
Step indices are 0-based and index into the `trajectory` array. Step 0 is always the system message.
Step 1 is the first user message. The anomalous step is typically 2+ (the first assistant with a tool call).
Normal records have `bad_step: null`.
