# Dataset Builder Phase-0 Improvements Implementation Plan

> For Hermes: use subagent-driven-development when executing this plan task-by-task.

**Goal:** Upgrade `dataset_builder/` using the findings from Phase 0 so the pipeline becomes more trustworthy, more realistic, and easier to extend without turning into an over-engineered platform project.

**Architecture:** Keep the current script-first pipeline and improve quality at the seams: raw-schema inspection, normalization metadata, perturbation realism, anomaly taxonomy, build diagnostics, and validation depth. Treat the VPS as the default control plane, prefer Modal serverless GPU as the default GPU tier when any GPU-backed step becomes necessary, and keep Apple Silicon as the secondary local option for bounded fallback work.

**Tech Stack:** Python, pytest, JSONL, Hugging Face datasets, markdown docs, Hermes Agent, Modal serverless GPU (default GPU path), Apple Silicon (secondary fallback), Audiobookshelf podcast pipeline, baoyu infographic workflow.

---

## Why this plan exists

Phase 0 clarified several facts that should directly shape the implementation:

1. Hermes traces are long, tool-centric execution traces, not short chat samples.
2. The raw dataset is ShareGPT-like (`from`, `value`) with serialized `<tool_call>` / `<tool_response>` markup, not native structured OpenAI tool-call objects.
3. The current builder already has a good simple backbone: normalization, synthetic perturbations, source-trace split assignment, and basic label validation.
4. The biggest remaining weakness is not missing infrastructure. It is dataset quality discipline.
5. TrajAD's key advantage is coherent anomalous trajectories, especially after the first wrong step. This repo currently uses direct perturbation only, which is simple and fine for v1, but can produce internally inconsistent trajectories.

This plan therefore prefers quality-focused, local improvements over architecture sprawl.

## Design choices and best-practice guidance

### 1. Keep the pipeline script-first
Use plain Python modules and JSONL files. Avoid adding workflow engines, databases, or distributed orchestration for this stage. The current scale does not justify them.

### 2. Improve observability before sophistication
Before adding new perturbation families or model-assisted continuation, make inspection, manifests, and validation stronger. Good visibility prevents accidental low-quality data.

### 3. Separate schema correctness from semantic plausibility
- `validate_labels.py` should keep checking schema-level invariants.
- A new lightweight coherence layer should catch obviously implausible perturbation outputs.
This preserves simplicity while acknowledging that "valid JSONL" is not the same thing as "good training data".

### 4. Encode the anomaly taxonomy explicitly
Store both the specific `anomaly_type` and the higher-level `anomaly_class` so the dataset aligns better with TrajAD's conceptual framing.

### 5. Favor deterministic metadata over premature structure expansion
Do not redesign the whole trajectory schema yet. Add small derived metadata fields that are cheap to compute and useful for diagnostics and filtering.

### 6. Prefer Modal serverless GPU by default for GPU work
If a future extension needs GPU-backed continuation, filtering, or model evaluation, use Modal serverless GPU first. Apple Silicon remains valuable for secondary local experimentation and bounded fallback work, but is no longer the default GPU path.

### 7. Preserve YAGNI and DRY
Every new field, helper, or validation rule must support a current need in perturbation quality, dataset analysis, or reproducibility. Avoid adding abstractions whose only job is to anticipate hypothetical future scale.

---

## Target improvements

This plan implements seven practical improvements:

1. Raw-schema-safe trace inspection
2. Derived metadata that reflects tool-centric structure
3. Explicit top-level anomaly classes
4. Lightweight perturbation coherence screening
5. More realistic unwarranted-continuation / contradiction rules
6. Stronger rule-aware localization validation
7. Reproducible build manifests and perturbation diagnostics

---

### Task 1: Repair raw-data inspection for ShareGPT-style Hermes traces

**Status:** Done (2026-04-23)
**Verification:** `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_inspect_traces.py -v` and `python3 dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl`
**Implementation infographic:** `infographic/task-1-raw-inspection/infographic.png`

**Objective:** Make the inspection path trustworthy on the real raw dataset before deeper changes.

**Files:**
- Modify: `dataset_builder/inspect_traces.py`
- Test: `tests/test_inspect_traces.py`

**Why this task matters:**
Phase 0 showed that raw Hermes records use `from/value`, but `inspect_traces.py` currently assumes `role/content` and fails on the real file. A broken inspection script undermines every later decision.

**Step 1: Write failing tests for raw-format compatibility**
Create tests that cover:
- a raw ShareGPT-style record with `from/value`
- a normalized record with `role/content`
- mixed tool-call and non-tool-call messages

Example cases to include:
```python
raw_traj = [
    {"from": "system", "value": "sys"},
    {"from": "human", "value": "hi"},
    {"from": "gpt", "value": "<tool_call>{"name": "search_web", "arguments": {"query": "x"}}</tool_call>"},
    {"from": "tool", "value": "<tool_response>ok</tool_response>"},
]
```

**Step 2: Run test to verify failure**
Run:
```bash
pytest tests/test_inspect_traces.py -v
```
Expected: FAIL against the current implementation.

**Step 3: Implement minimal compatibility helpers**
In `dataset_builder/inspect_traces.py`, add tiny helpers like:
- `get_role(msg)` -> `msg.get("role", msg.get("from", "?"))`
- `get_content(msg)` -> `msg.get("content", msg.get("value", "")) or ""`

Use these in:
- `count_roles()`
- `print_summary()`
- `print_sample()`

**Step 4: Add a clearer summary block**
While touching the file, add outputs for:
- percentage of traces with at least one tool call
- percentage of traces with at least two assistant/tool-call pairs
These are directly motivated by Phase 0 findings.

**Step 5: Run tests and real inspection**
Run:
```bash
pytest tests/test_inspect_traces.py -v
python3 dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl
```
Expected:
- tests pass
- real raw file prints a summary instead of throwing `KeyError: 'role'`

**Step 6: Commit**
```bash
git add dataset_builder/inspect_traces.py tests/test_inspect_traces.py
git commit -m "fix: support raw Hermes trace schema in inspection"
```

---

### Task 2: Add derived structural metadata during normalization

**Status:** Done (2026-04-23)
**Verification:** `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_normalize_trajectory.py -v` and `python3 dataset_builder/normalize_trajectory.py data/raw/hermes_filtered.jsonl data/interim/hermes_normalized.jsonl`
**Implementation infographic:** `infographic/task-2-derived-metadata/infographic.png`

**Objective:** Preserve more useful signal about tool-heavy trajectories without redesigning the schema.

**Files:**
- Modify: `dataset_builder/normalize_trajectory.py`
- Test: `tests/test_normalize_trajectory.py`

**Why this task matters:**
Phase 0 established that the corpus is tool-dense and structure-heavy. The current normalized format is appropriately simple, but it throws away cheap-to-compute metadata that would help diagnostics and filtering.

**Step 1: Write failing tests for derived metadata**
Add tests for normalized output containing metadata keys such as:
- `tool_call_count`
- `tool_response_count`
- `has_think`
- optionally `trajectory_length`

**Step 2: Run test to verify failure**
Run:
```bash
pytest tests/test_normalize_trajectory.py -v
```
Expected: FAIL because these keys do not yet exist.

**Step 3: Implement metadata extraction helpers**
In `dataset_builder/normalize_trajectory.py`, add a small helper such as `derive_trace_metadata(trajectory)` that computes:
- total trajectory length
- count of `<tool_call>` blocks
- count of `<tool_response>` blocks
- whether any message contains `<think>`

Merge those values into `metadata` without removing existing source metadata.

**Step 4: Keep schema simple**
Do not change the core trajectory item shape. Keep:
```python
{"role": ..., "content": ...}
```
Only enrich `metadata`.

**Step 5: Run tests and a normalization smoke test**
Run:
```bash
pytest tests/test_normalize_trajectory.py -v
python3 dataset_builder/normalize_trajectory.py data/raw/hermes_filtered.jsonl data/interim/hermes_normalized.jsonl
```
Expected:
- tests pass
- normalized file still writes successfully
- metadata contains the new keys

**Step 6: Commit**
```bash
git add dataset_builder/normalize_trajectory.py tests/test_normalize_trajectory.py
git commit -m "feat: derive structural metadata during normalization"
```

---

### Task 3: Add explicit top-level anomaly classes

**Status:** Done (2026-04-23)
**Verification:** `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_validate_labels.py tests/test_perturbations.py -q`, `python3 dataset_builder/build_trajad_dataset.py --mvp --seed 42`, and `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`
**Implementation infographic:** `infographic/task-3-top-level-anomaly-classes/infographic.png`

**Objective:** Align the dataset output with the Phase-0 anomaly taxonomy while keeping the current rule-level labels.

**Files:**
- Modify: `dataset_builder/perturbations.py`
- Modify: `dataset_builder/validate_labels.py`
- Modify: `dataset_builder/build_trajad_dataset.py`
- Test: `tests/test_validate_labels.py`

**Why this task matters:**
Phase 0 framed the problem in top-level classes:
- task failure
- process inefficiency
- unwarranted continuation

The repo currently stores only leaf anomaly labels, which makes later analysis less clear than it should be.

**Step 1: Write failing validation tests**
Add tests that assert:
- anomalous records must include `anomaly_class`
- `anomaly_class` must belong to the valid set
- normal records keep `anomaly_class=None`

**Step 2: Run test to verify failure**
Run:
```bash
pytest tests/test_validate_labels.py -v
```
Expected: FAIL on missing field / unsupported checks.

**Step 3: Add a single mapping table**
In `dataset_builder/perturbations.py`, define a mapping from `anomaly_type` to `anomaly_class`, for example:
- `wrong_tool_choice` -> `task_failure`
- `bad_tool_arguments` -> `task_failure`
- `contradicted_tool_result` -> `task_failure`
- `premature_final_answer` -> `task_failure`
- `repeated_step` -> `process_inefficiency`
- `continued_after_sufficient_evidence` -> `unwarranted_continuation`

Decide deliberately whether `skipped_required_step` belongs under `task_failure` or `process_inefficiency`; document the reasoning inline.

**Step 4: Populate the field consistently**
Whenever a perturbation succeeds, set both:
- `anomaly_type`
- `anomaly_class`

Ensure normals keep `None`.

**Step 5: Extend schema validation**
Update `validate_labels.py` to check valid anomaly classes.

**Step 6: Rebuild and validate**
Run:
```bash
python3 dataset_builder/build_trajad_dataset.py --mvp --seed 42
python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict
```
Expected: successful rebuild and validation with the new field present.

**Step 7: Commit**
```bash
git add dataset_builder/perturbations.py dataset_builder/validate_labels.py dataset_builder/build_trajad_dataset.py tests/test_validate_labels.py
git commit -m "feat: add top-level anomaly classes"
```

---

### Task 4: Add a lightweight coherence screen after perturbation

**Status:** Done (2026-04-23)
**Verification:** `PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_coherence.py tests/test_perturbations.py tests/test_validate_labels.py tests/test_build_trajad_dataset.py -q`, `python3 dataset_builder/build_trajad_dataset.py --mvp --seed 42`, `python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict`, and `diff -u /tmp/task4_build1.log /tmp/task4_build2.log`
**Implementation infographic:** `infographic/task-4-lightweight-coherence-screen/infographic.png`

**Objective:** Filter out obviously implausible anomalous records without adding a full perturb-and-complete system.

**Files:**
- Create: `dataset_builder/coherence.py`
- Modify: `dataset_builder/build_trajad_dataset.py`
- Test: `tests/test_coherence.py`

**Why this task matters:**
This is the highest-value quality improvement from Phase 0. The current system directly perturbs one step and leaves the rest unchanged. That simplicity is good, but it can create broken-looking trajectories. A small coherence filter gives most of the benefit without requiring LLM-generated continuation.

**Step 1: Write failing tests for obvious bad cases**
Cover simple rejection patterns such as:
- an assistant `<tool_call>` that now has no plausible follow-up where the trace otherwise strongly implies one
- malformed assistant/tool pair ordering after swaps/removals
- duplicate or dangling fragments created by a perturbation

**Step 2: Run test to verify failure**
Run:
```bash
pytest tests/test_coherence.py -v
```
Expected: FAIL because no coherence screen exists yet.

**Step 3: Implement a tiny rule-based screen**
Create `dataset_builder/coherence.py` with a function like:
```python
def is_plausible_trajectory(record: dict) -> tuple[bool, str | None]:
    ...
```
Keep it intentionally small and deterministic.

Good first checks:
- count malformed assistant/tool pair transitions
- detect assistant tool-call steps that are left hanging in clearly broken ways
- reject exact contradictions introduced by structural corruption, not semantic disagreement alone

**Step 4: Integrate it into the builder**
In `build_trajad_dataset.py`, after `apply_perturbation(...)`:
- keep the record if plausible
- otherwise drop it and count the rejection reason

**Step 5: Surface rejection counts**
Print counts by rejection reason at the end of the build.

**Step 6: Re-run build and validation**
Run:
```bash
pytest tests/test_coherence.py -v
python3 dataset_builder/build_trajad_dataset.py --mvp --seed 42
python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict
```
Expected:
- tests pass
- dataset still builds
- builder reports kept vs rejected anomalies

**Step 7: Commit**
```bash
git add dataset_builder/coherence.py dataset_builder/build_trajad_dataset.py tests/test_coherence.py
git commit -m "feat: screen implausible perturbed trajectories"
```

---

### Task 5: Make P5 and P6 more realistic

**Objective:** Improve the most obviously synthetic perturbations without adding model-generated continuation.

**Files:**
- Modify: `dataset_builder/perturbations.py`
- Test: `tests/test_perturbations.py`

**Why this task matters:**
Phase 0 made it clear that unrealistic anomalies hurt dataset quality. Right now:
- `P5` creates a dangling continuation pattern
- `P6` uses an explicit contradiction marker that is too artificial

**Step 1: Write failing tests that encode the new expectations**
Add tests asserting:
- `P5` produces a structurally complete extra continuation pattern, not a dangling one
- `P6` contradicts the tool result without using an explicit bracketed marker like `[CONTRADICTION]`

**Step 2: Run test to verify failure**
Run:
```bash
pytest tests/test_perturbations.py -v
```
Expected: FAIL on the new expectations.

**Step 3: Refine P5**
Choose one practical path:
- append a redundant natural-language assistant action, or
- append assistant tool-call + tool response + redundant assistant wrap-up

Prefer the second option if it remains simple and deterministic.

**Step 4: Refine P6**
Replace the explicit contradiction marker with a subtle but wrong natural-language conclusion that mismatches the last tool result.

**Step 5: Re-run targeted tests**
Run:
```bash
pytest tests/test_perturbations.py -v
```
Expected: PASS.

**Step 6: Rebuild and sanity-check**
Run:
```bash
python3 dataset_builder/build_trajad_dataset.py --seed 42
python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict
```
Expected: full build still succeeds.

**Step 7: Commit**
```bash
git add dataset_builder/perturbations.py tests/test_perturbations.py
git commit -m "feat: improve realism of continuation and contradiction rules"
```

---

### Task 6: Deepen validation for first-error localization

**Objective:** Make label validation care more about the intended first-bad-step semantics, not just type/range checks.

**Files:**
- Modify: `dataset_builder/validate_labels.py`
- Test: `tests/test_validate_labels.py`

**Why this task matters:**
Phase 0 emphasized first-error localization as a core supervision target. Current validation mostly checks that `bad_step` exists and is in range. That is necessary, but not enough.

**Step 1: Add failing rule-aware tests**
Cover expectations such as:
- duplicated-pair anomalies point at the inserted duplicate
- truncation anomalies point at the cut point
- skipped-step anomalies can point at the missing position
- continuation anomalies point at the first unnecessary extra step

**Step 2: Run test to verify failure**
Run:
```bash
pytest tests/test_validate_labels.py -v
```
Expected: FAIL because these semantics are not yet enforced.

**Step 3: Implement minimal rule-aware checks**
In `validate_labels.py`, keep the logic simple:
- continue doing generic checks first
- then branch on `generation_rule` for a few high-value assertions

Avoid trying to infer semantics for every future rule. Support only the rules that actually exist now.

**Step 4: Re-run validation tests and full dataset validation**
Run:
```bash
pytest tests/test_validate_labels.py -v
python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict
```
Expected: PASS.

**Step 5: Commit**
```bash
git add dataset_builder/validate_labels.py tests/test_validate_labels.py
git commit -m "feat: add rule-aware bad-step validation"
```

---

### Task 7: Add build manifests and perturbation diagnostics

**Objective:** Make every dataset build reproducible and inspectable.

**Files:**
- Modify: `dataset_builder/build_trajad_dataset.py`
- Create: `dataset_builder/diagnostics.py` (optional helper if needed)
- Test: `tests/test_build_manifest.py`

**Why this task matters:**
A home lab benefits more from repeatability than from platform complexity. Right now the builder prints useful counts but does not save them.

**Step 1: Write failing tests for build manifest output**
Add tests that expect a manifest JSON to contain:
- seed
- rules used
- source input paths
- split counts
- anomaly-type counts
- anomaly-class counts
- perturbation failures / coherence rejections

**Step 2: Run test to verify failure**
Run:
```bash
pytest tests/test_build_manifest.py -v
```
Expected: FAIL because no manifest exists yet.

**Step 3: Implement manifest writing**
At the end of `build_trajad_dataset.py`, write something like:
- `data/processed/build_manifest.json`

Include:
- timestamp
- seed
- rule names
- normal/anomalous totals
- split sizes
- counts per anomaly type
- counts per anomaly class
- failures and coherence rejections per rule

**Step 4: Add human-friendly diagnostics output**
Print a short table or grouped summary to stdout so the command remains pleasant to use interactively.

**Step 5: Verify**
Run:
```bash
pytest tests/test_build_manifest.py -v
python3 dataset_builder/build_trajad_dataset.py --seed 42
python3 -m json.tool data/processed/build_manifest.json > /tmp/build_manifest.pretty.json
```
Expected:
- tests pass
- manifest exists and is readable

**Step 6: Commit**
```bash
git add dataset_builder/build_trajad_dataset.py tests/test_build_manifest.py data/processed/build_manifest.json
git commit -m "feat: record build manifests and perturbation diagnostics"
```

---

## Recommended execution order

1. Task 1 — raw inspection reliability
2. Task 2 — derived normalization metadata
3. Task 3 — anomaly taxonomy alignment
4. Task 4 — coherence screening
5. Task 5 — perturbation realism upgrades
6. Task 6 — rule-aware localization validation
7. Task 7 — reproducibility manifest and diagnostics

## GPU / compute policy for this plan

- Default GPU path: Modal serverless GPU
- Secondary GPU/local experimentation path: Apple Silicon
- Default execution tier for Tasks 1–7: VPS CPU, because these tasks are Python + JSONL data engineering
- If a future extension adds model-assisted perturb-and-complete, sample auditing, or semantic filtering, start with Modal rather than assuming Apple Silicon
- Only use Apple Silicon as a secondary option for bounded local experimentation or when a specific local validation need exists

## Verification checklist

- [ ] `inspect_traces.py` works on the raw Hermes JSONL file
- [ ] normalized records include cheap structural metadata
- [ ] anomalous records carry both `anomaly_type` and `anomaly_class`
- [ ] the builder rejects obviously implausible perturbations
- [ ] P5 and P6 look less synthetic than before
- [ ] validation checks some first-error semantics, not just field presence
- [ ] each build writes a readable manifest with counts and diagnostics
- [ ] the full dataset still builds and validates cleanly after the improvements

## Expected outcome

After this plan, `dataset_builder/` should still feel simple, but noticeably more disciplined:
- better raw-data visibility
- better alignment with the domain taxonomy
- better perturbation realism
- better label trustworthiness
- better reproducibility

That is the right kind of progress for a home AI lab: practical, elegant, and understandable.
