# Interactive Trajectory Visualization Implementation Plan

> For Hermes: use subagent-driven-development when executing this plan task-by-task.

**Goal:** Add a polished, interactive, single-page visualization experience that explains the gemma-trajad-eval project, lets a reader inspect normal vs anomalous trajectories, and makes dataset/evaluation behavior legible in the browser.

**Architecture:** Follow the interactive-turboquant pattern on purpose: a static, single-page, desktop-first HTML experience with a sticky table of contents, tactical-HUD visual styling, and self-contained interactive demos implemented in plain JavaScript plus Canvas 2D. Keep the implementation buildless at first: one HTML entrypoint, small adjacent JSON assets generated from the existing Python pipeline, and zero frontend framework dependency unless the static approach demonstrably breaks down.

**Tech Stack:** HTML, CSS custom properties, JavaScript, Canvas 2D API, optional MathJax for equations, repo-generated JSON payloads, Python export helpers, uv, existing dataset_builder/training artifacts.

---

## Why this plan exists

Reference visualization:
- GitHub: https://github.com/ArkAung/interactive-turboquant
- Live demo: https://arkaung.github.io/interactive-turboquant/

The reference project `interactive-turboquant` is useful here not because this repo needs quantization demos, but because it proves a strong product pattern:

1. one-file or near-one-file static delivery
2. narrative + interactivity tightly coupled
3. custom Canvas demos instead of heavyweight plotting libraries
4. CSS-variable theming that also drives canvas colors
5. immediate usability on GitHub Pages or local file open

For gemma-trajad-eval, the analogous experience should teach and demonstrate:

- what a Hermes trajectory looks like
- how the dataset pipeline transforms raw traces into labeled examples
- where perturbations are injected
- what anomaly localization means at the step level
- how model outputs, baselines, and errors should be interpreted

---

## Product shape

The target artifact is a desktop-first static explainer at something like:

- `apps/trajectory_explorer/index.html`

Backed by generated browser payloads such as:

- `apps/trajectory_explorer/assets/overview_payload.json`
- `apps/trajectory_explorer/assets/sample_trajectories.json`
- `apps/trajectory_explorer/assets/evaluation_payload.json`

The page should be usable in three modes:

1. local open in browser for development
2. simple static hosting such as GitHub Pages
3. optional embedding or linking from repo docs/wiki

---

## Scope principles

### Hard constraints

- Prefer buildless static delivery in V1.
- Prefer Canvas 2D for custom visuals over React/D3/Plotly.
- Reuse repo-truth data exported from Python instead of hand-maintained frontend constants.
- Keep the first version desktop-first; mobile adaptation is a later concern.
- Do not require the browser to load large raw JSONL files directly.

### Non-goals for V1

- no full annotation tool
- no live training dashboard
- no backend server requirement
- no browser-side processing of the full corpus
- no WebGL unless 2D canvas genuinely becomes insufficient

---

## Narrative sections to include

### Section 1: Project overview

Explain the project in one screen:

- source traces
- perturbation engine
- supervised tasks
- fine-tuning/evaluation path
- VPS/Mac/Modal execution topology

Primary visual:
- architecture flow graphic, evolved from `docs/infographics/gemma-trajad-project-overview.html`

### Section 2: What a trajectory actually is

Interactive demo ideas:
- step-by-step trajectory timeline
- role-colored message ladder
- expandable assistant/tool pairs
- token/step count badges

Primary learning goal:
- make the raw structure legible before talking about anomalies

### Section 3: How anomalies are created

Interactive demo ideas:
- before/after comparison of a normal trace and one perturbed variant
- highlighted bad step index
- perturbation-rule selector for P1/P2/P3/etc.
- side-by-side diff view for tool-call and final-answer mutations

Primary learning goal:
- show that labels are not magic; they come from explicit transformations

### Section 4: Localization and taxonomy

Interactive demo ideas:
- anomaly-type grid
- step-localization heat strip over a trajectory
- hover to reveal anomaly metadata, rule, subtype, and explanation

Primary learning goal:
- connect `is_anomalous`, `bad_step`, and `anomaly_type`

### Section 5: Dataset behavior and perturbation coverage

Interactive demo ideas:
- split-size bar chart
- subtype distribution chart
- perturbation-rule coverage chart
- sample-count funnel from raw traces to processed examples

Primary learning goal:
- make dataset construction legible and show what the browser examples represent

### Section 6: Fine-tuning pipeline and training lifecycle

Interactive demo ideas:
- staged pipeline walkthrough from processed JSONL -> SFT formatting -> adapters -> reports
- training configuration cards for binary / localize / joint tasks
- small-multiple run comparison for E2B-first, optional E4B, and later RL/GRPO phases
- artifact flow showing where prompts, adapters, checkpoints, and reports land in the repo

Primary learning goal:
- explain the later project parts, especially how fine-tuning is structured and what gets produced at each stage

### Section 7: Evaluation and error analysis

Interactive demo ideas:
- baseline vs model metrics cards
- task-wise metric bands for T1/T2/T3
- confusion-style view for model errors
- drill-down into false positives, false negatives, and localization misses
- calibration/confidence view if that data exists in exports

Primary learning goal:
- make the evaluation plan operational rather than abstract, and show how model quality is judged after training

### Section 8: Execution topology and reproducibility

Interactive demo ideas:
- static/animated system map for VPS control plane, Mac worker, and Modal escalation
- artifact-flow map from raw data to reports

Primary learning goal:
- show how the repo operates as a Hermes-first system, not just a pile of scripts

---

## Proposed file layout

### New files likely required

- `docs/visualization/trajectory-explorer-spec.md`
- `docs/visualization/trajectory-explorer-data-contract.md`
- `docs/visualization/trajectory-explorer-storyboard.md`
- `apps/trajectory_explorer/index.html`
- `apps/trajectory_explorer/README.md`
- `apps/trajectory_explorer/assets/overview_payload.json`
- `apps/trajectory_explorer/assets/sample_trajectories.json`
- `apps/trajectory_explorer/assets/evaluation_payload.json`
- `apps/trajectory_explorer/assets/training_payload.json`
- `scripts/export_trajectory_explorer_payload.py`
- `tests/test_export_trajectory_explorer_payload.py`

### Existing files likely to inspect or reuse

- `docs/project-spec.md`
- `docs/evaluation-plan.md`
- `docs/infographics/gemma-trajad-project-overview.html`
- `dataset_builder/build_trajad_dataset.py`
- `dataset_builder/perturbations.py`
- `dataset_builder/perturbation_diagnostics.py`
- `training/evaluate.py`
- `data/processed/all.jsonl`
- `data/processed/perturbation_diagnostics.json`

---

## Data contract direction

The frontend should not parse the entire training corpus. Export small, curated browser payloads instead.

### Payload A: overview payload

Purpose:
- counts, splits, taxonomy summary, architecture metadata

Suggested schema:

```json
{
  "generated_at": "2026-04-27T12:00:00Z",
  "project": {
    "name": "gemma-trajad-eval",
    "tagline": "Local trajectory anomaly detection for tool-using agents"
  },
  "counts": {
    "raw_traces": 3679,
    "processed_examples": 18355,
    "train": 13767,
    "dev": 1833,
    "test": 2755
  },
  "taxonomy": [
    {"id": "wrong_tool_choice", "class": "process_inefficiency", "label": "Wrong tool choice"}
  ],
  "execution_topology": [
    {"node": "vps", "role": "control-plane"}
  ]
}
```

### Payload B: sample trajectories payload

Purpose:
- a compact set of handpicked normal/anomalous traces for interactive inspection

Suggested schema:

```json
{
  "samples": [
    {
      "id": "trace_000123_var_02",
      "source_trace_id": "uuid",
      "is_anomalous": true,
      "anomaly_type": "bad_tool_arguments",
      "bad_step": 4,
      "generation_rule": "P2",
      "messages": [
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "...", "tool_name": "browser_type"},
        {"role": "tool", "content": "..."}
      ],
      "diff_hints": {
        "changed_message_indexes": [5],
        "explanation": "Argument mutated from valid path to missing path"
      }
    }
  ]
}
```

### Payload C: training payload

Purpose:
- fine-tuning stages, run metadata, task modes, and artifact locations for later-part visuals

Suggested schema:

```json
{
  "training_stages": [
    {
      "stage_id": "phase-a-binary-sft",
      "label": "Binary anomaly detection SFT",
      "input_artifact": "data/processed/train_sft_binary.jsonl",
      "script": "training/train_e2b.py",
      "output_artifact": "outputs/adapters/e2b-binary-run1"
    }
  ],
  "runs": [
    {
      "run_id": "e2b-binary-run1",
      "model": "google/gemma-4-E2B-it",
      "task_mode": "binary",
      "status": "planned",
      "artifacts": ["outputs/adapters/e2b-binary-run1"]
    }
  ]
}
```

### Payload D: evaluation payload

Purpose:
- metrics, distributions, and small error slices for charts

Suggested schema:

```json
{
  "runs": [
    {
      "run_id": "baseline-rule-based",
      "metrics": {
        "t1_f1": 0.0,
        "t2_exact": 0.0,
        "t3_macro_f1": 0.0
      }
    }
  ],
  "subtype_distribution": [
    {"label": "wrong_tool_choice", "count": 100}
  ],
  "error_slices": [
    {
      "sample_id": "trace_000123_var_02",
      "predicted_type": "repeated_step",
      "true_type": "bad_tool_arguments"
    }
  ]
}
```

---

## UI and interaction direction

### Layout

Adopt the same broad structure as the reference:

- sticky left navigation
- scrollable narrative main column
- section-level cards
- desktop-wide layout first

### Styling language

Reuse and extend the current repo infographic style:

- dark tactical/HUD theme
- CSS variables for all colors
- monospace metric readouts
- subtle grid/scanline background
- corner-bracket card accents
- theme toggle only if it stays cheap

### Canvas-first component list

Implement custom demos with `canvas.getContext('2d')` where interactivity matters:

1. trajectory timeline canvas
2. anomaly-step heat strip canvas
3. before/after perturbation diff strip
4. subtype histogram canvas
5. confusion-matrix or error-grid canvas
6. topology flow mini-map

### DOM-first component list

Use normal HTML for:

- narrative text
- controls
- badges and metric readouts
- code/data snippets
- legend rows

### Interaction wiring pattern

Keep the reference repo's simplicity:

- slider/select/button event -> recompute state -> redraw canvas -> update readouts
- one closure/IIFE per section or module
- no state library

---

## Implementation tasks

### Task 1: Write the visualization product spec

**Objective:** Freeze the scope, the audience, and the V1 interaction list before writing frontend code.

**Files:**
- Create: `docs/visualization/trajectory-explorer-spec.md`
- Create: `docs/visualization/trajectory-explorer-storyboard.md`
- Reference: `docs/project-spec.md`
- Reference: `docs/evaluation-plan.md`
- Reference: `docs/infographics/gemma-trajad-project-overview.html`

**Step 1: Capture user stories**

Write concise stories for:
- a newcomer understanding trajectories
- a researcher inspecting perturbations
- the user presenting the project visually

**Step 2: Freeze V1 scenes**

List each section and interactive demo with one sentence of purpose.

**Step 3: Define acceptance criteria**

Examples:
- a reader can inspect at least one normal and one anomalous trajectory
- the page explains `bad_step` visually
- all visuals still render from static files only

**Step 4: Verify**

Re-read the spec and confirm that every planned visual ties back to a concrete repo concept.

---

### Task 2: Define the browser payload contract

**Objective:** Create a strict contract between Python exports and browser rendering, including the later fine-tuning and evaluation parts.

**Files:**
- Create: `docs/visualization/trajectory-explorer-data-contract.md`
- Create: `scripts/export_trajectory_explorer_payload.py`
- Create: `tests/test_export_trajectory_explorer_payload.py`
- Inspect: `data/processed/all.jsonl`
- Inspect: `data/processed/perturbation_diagnostics.json`
- Inspect: `training/evaluate.py`

**Step 1: Enumerate required frontend fields**

Document which metrics, trajectory fields, labels, training-run metadata, and artifact references the browser actually needs.

**Step 2: Keep payloads small**

Define caps for sample count, message count, and error examples.

**Step 3: Add export tests first**

Write tests that validate the generated JSON structure and size expectations.

**Step 4: Implement exporter**

Generate deterministic payloads from repo artifacts.

**Step 5: Verify**

Run the exporter and inspect the JSON files.
Expected: valid, compact payloads with no dependence on raw full-corpus browser parsing.

---

### Task 3: Build the static shell and visual system

**Objective:** Create the single-page scaffold that all later demos plug into.

**Files:**
- Create: `apps/trajectory_explorer/index.html`
- Create: `apps/trajectory_explorer/README.md`
- Reference: `docs/infographics/gemma-trajad-project-overview.html`

**Step 1: Create semantic sections**

Add the sticky TOC, section cards, hero, and footer.

**Step 2: Port the HUD theme**

Move the current infographic language into reusable CSS variables and card styles.

**Step 3: Add theme-aware canvas helpers**

Create shared JS helpers that read CSS variables for drawing colors.

**Step 4: Verify**

Open the page locally and confirm the layout works before any major demo logic exists.

---

### Task 4: Implement the trajectory-structure explorer

**Objective:** Make the raw message structure understandable to a human reader.

**Files:**
- Modify: `apps/trajectory_explorer/index.html`
- Use payload: `apps/trajectory_explorer/assets/sample_trajectories.json`

**Step 1: Build the sample selector**

Allow switching between normal and anomalous examples.

**Step 2: Draw the timeline canvas**

Show message order, roles, tool-call points, and the highlighted bad step if present.

**Step 3: Add linked readouts**

When a step is hovered or selected, show role, tool name, and content excerpt in the DOM.

**Step 4: Verify**

Confirm a first-time reader can identify where the trajectory starts, where tool use occurs, and what step is anomalous.

---

### Task 5: Implement perturbation before/after comparison

**Objective:** Show exactly how a synthetic anomaly differs from the original trace.

**Files:**
- Modify: `apps/trajectory_explorer/index.html`
- Extend exporter: `scripts/export_trajectory_explorer_payload.py`
- Test: `tests/test_export_trajectory_explorer_payload.py`

**Step 1: Pair source and variant samples**

Export source/variant pairs with changed-message indexes.

**Step 2: Build the comparison UI**

Show normal vs anomalous trajectories side by side or as an A/B toggle.

**Step 3: Highlight mutation boundaries**

Use accent color, strike/replace treatment, or focused detail cards to show what changed.

**Step 4: Verify**

Confirm that P1/P2/P4/P6-style mutations are visually legible without reading full raw JSON.

---

### Task 6: Implement taxonomy and localization views

**Objective:** Make labels and step-localization semantics intuitive.

**Files:**
- Modify: `apps/trajectory_explorer/index.html`
- Use payloads: `overview_payload.json`, `sample_trajectories.json`
- Reference: `docs/project-spec.md`

**Step 1: Build the subtype matrix or card grid**

Render the anomaly taxonomy with class grouping.

**Step 2: Add localization heat-strip logic**

Represent `bad_step` as a position-aware marker over the trajectory.

**Step 3: Link taxonomy to examples**

Selecting a subtype should jump to or load a matching sample.

**Step 4: Verify**

A reader should be able to answer: what kind of anomaly is this, and where does it occur?

---

### Task 7: Implement fine-tuning pipeline views

**Objective:** Visualize the later project parts so training is explained as clearly as dataset-building.

**Files:**
- Modify: `apps/trajectory_explorer/index.html`
- Use payload: `apps/trajectory_explorer/assets/training_payload.json`
- Inspect: `training/prepare_sft_data.py`
- Inspect: `training/train_e2b.py`
- Inspect: `training/train_e4b.py`
- Inspect: `docs/project-spec.md`
- Inspect: `docs/deferred-training-roadmap.md`

**Step 1: Render the training lifecycle**

Show the staged path from processed dataset -> SFT data -> training run -> adapter outputs -> evaluation reports.

**Step 2: Render task-mode views**

Explain binary, localize, and joint modes, plus where later RL/GRPO work would fit.

**Step 3: Render run/artifact cards**

Show model choice, task mode, major scripts, and output locations in a presentation-friendly way.

**Step 4: Verify**

A reader should be able to explain how the repo moves from processed examples into a fine-tuned model artifact.

---

### Task 8: Implement evaluation and error-analysis panels

**Objective:** Turn the existing evaluation and distribution docs into interactive evidence.

**Files:**
- Modify: `apps/trajectory_explorer/index.html`
- Use payload: `apps/trajectory_explorer/assets/evaluation_payload.json`
- Inspect: `docs/evaluation-plan.md`
- Inspect/extend as needed: `training/evaluate.py`

**Step 1: Render split and subtype distributions**

Draw compact bar/histogram views from exported counts.

**Step 2: Render metrics cards and baseline comparisons**

Show T1/T2/T3 metrics in a way that is presentation-ready.

**Step 3: Add error slices**

Include a few qualitative false positive/false negative examples if available.

**Step 4: Verify**

Make sure the page reflects repo-truth and not hand-entered numbers.

---

### Task 9: Document development and publishing workflow

**Objective:** Make the visualization maintainable and easy to regenerate.

**Files:**
- Update: `apps/trajectory_explorer/README.md`
- Update: `README.md`
- Update: relevant wiki pages under `wiki/`

**Step 1: Document the regeneration commands**

Include exporter commands, where payloads land, and how to open the page.

**Step 2: Document hosting options**

Describe local file open and static hosting.

**Step 3: Verify**

A newcomer should be able to rebuild the payloads and open the visualization without guessing.

---

## Validation plan

### Functional checks

- exporter script runs cleanly under `uv run`
- generated payload files are valid JSON
- the HTML page renders without console errors
- sample switching updates the correct visual state
- taxonomy selection maps to matching example views
- theme-aware canvas redraws stay readable

### Data checks

- counts shown on the page match repo-generated payloads
- sample traces are deterministic and documented
- bad-step highlighting matches labeled metadata
- evaluation metrics originate from exported artifacts, not hand-coded constants

### Quality checks

- no frontend build step required for V1
- page remains reasonably understandable in a local browser with static files only
- visuals remain presentation-grade even without live backend services

---

## Risks and tradeoffs

### Risk 1: Single-file HTML becomes too large

Mitigation:
- allow adjacent JSON payloads and tiny helper modules while keeping the no-build constraint

### Risk 2: Raw trajectory text is too verbose for the page

Mitigation:
- export curated excerpts plus expandable full-content panes

### Risk 3: Evaluation data is not yet rich enough

Mitigation:
- ship the page first with dataset and perturbation views, leaving model-performance panels as progressively richer sections

### Risk 4: Canvas implementation complexity grows

Mitigation:
- reserve DOM/SVG for simple charts; use canvas only where interaction and custom drawing matter

### Risk 5: The repo's current visual assets diverge stylistically

Mitigation:
- reuse the existing infographic palette and system-map language as the seed design system

---

## Recommended execution order

1. Task 1 — product spec and storyboard
2. Task 2 — data contract and exporter tests
3. Task 3 — static shell and HUD visual system
4. Task 4 — trajectory explorer
5. Task 5 — perturbation comparison
6. Task 6 — taxonomy/localization views
7. Task 7 — fine-tuning pipeline views
8. Task 8 — evaluation and error-analysis panels
9. Task 9 — docs and publishing workflow

---

## First acceptance target

The first meaningful milestone is not "complete visualization system." It is:

- one static HTML page
- one exporter script
- one curated payload bundle
- one normal trajectory and one anomalous trajectory explorable in-browser
- one visible explanation of `bad_step`
- one architecture panel and one dataset distribution panel
- one fine-tuning lifecycle panel and one evaluation panel

If that milestone lands cleanly, the rest can iterate without changing the overall architecture.
