# TrajAD perturbation context

## Overview
This infographic explains why Phase 3 begins with generation strategy and taxonomy before diving into individual perturbation rules. It compares TrajAD's perturb-and-complete pipeline against this repo's direct perturbation approach, maps the repo's anomaly subtypes into the three TrajAD classes, and highlights where current implementation coverage is strong or thin.

## Learning Objectives
The viewer will understand:
1. that `perturb-and-complete` and `direct perturbation` produce different realism tradeoffs
2. that this repo's anomaly taxonomy maps 10 subtypes into TrajAD's three top-level classes with uneven coverage
3. that the next rule-by-rule study should judge both taxonomy fit and realism

---

## Section 1: Why this stage exists

**Key Concept**: Phase 3 starts by asking whether the dataset builder is creating believable procedural failures, not just labeled edits.

**Content**:
- TrajAD evaluates anomaly detection plus first-error localization
- rollback-and-retry only works if the first error step is labeled correctly
- understanding rule realism matters before reading P1 through P9 one by one

**Visual Element**:
- Type: framing panel
- Subject: Phase 2 leading into Phase 3 with "realism" as the gate
- Treatment: bridge card from normalization to perturbation-engine study

**Text Labels**:
- Headline: "Why Phase 3 starts here"
- Subhead: "Taxonomy and realism come before rule-by-rule inspection"
- Labels: "anomaly detection", "first-error localization", "rollback-and-retry"

---

## Section 2: Two generation strategies

**Key Concept**: TrajAD regenerates the trajectory after the error; this repo mainly edits one step and keeps the rest.

**Content**:
- TrajAD: `perturb-and-complete`
- inject error at step K
- generate steps K+1..N as if the error were real
- this repo: `direct perturbation`
- modify step K
- leave later steps mostly unchanged

**Visual Element**:
- Type: split comparison
- Subject: left pipeline for perturb-and-complete, right pipeline for direct perturbation
- Treatment: step diagrams with highlighted error insertion point and downstream consequences

**Text Labels**:
- Headline: "Two dataset philosophies"
- Subhead: "Regenerate the rest vs edit one step"
- Labels: "perturb-and-complete", "direct perturbation", "step K", "steps K+1..N"

---

## Section 3: Realism tradeoff

**Key Concept**: Direct perturbation is simple and deterministic, but weaker on downstream realism.

**Content**:
- TrajBench summary: `63,484` samples across `13` tasks and `5` domains
- perturb-and-complete creates coherent bad trajectories
- direct perturbation is cheap, deterministic, and easy to test
- direct perturbation can leave later steps assuming the clean world state

**Visual Element**:
- Type: pros/cons module
- Subject: realism benefits on one side, simplicity benefits on the other
- Treatment: balanced scorecard with warning stripe on the direct-perturbation side

**Text Labels**:
- Headline: "Realism vs simplicity"
- Subhead: "Why the cheaper approach has a quality cost"
- Labels: "63,484", "13 tasks", "5 domains", "deterministic", "coherent downstream behavior"

---

## Section 4: Where direct perturbation breaks

**Key Concept**: Some current rules are useful but visibly reveal the limits of one-step editing.

**Content**:
- `P6 contradicted_tool_result`
- final answer changes, but the rest of the trace still reflects the clean evidence path
- `P7 premature_final_answer`
- trajectory is cut short and replaced with a fake early conclusion
- P3 and P8 also create structurally clear failures without regenerated downstream behavior

**Visual Element**:
- Type: warning / pitfall zone
- Subject: highlighted realism-risk examples
- Treatment: bright warning panel with example rule chips and contradiction arrows

**Text Labels**:
- Headline: "Where realism cracks show"
- Subhead: "The anomaly is valid, but the trajectory may still feel mechanically edited"
- Labels: "P6 contradicted_tool_result", "P7 premature_final_answer", "later steps not regenerated"

---

## Section 5: TrajAD top-level taxonomy

**Key Concept**: The paper's three-class taxonomy gives a process-level interpretation for the repo's rule inventory.

**Content**:
- `Task Failure`
- `Process Inefficiency`
- `Unwarranted Continuation`

**Visual Element**:
- Type: tree / taxonomy diagram
- Subject: one root splitting into three top-level classes
- Treatment: central taxonomy module with color-coded branches

**Text Labels**:
- Headline: "Three top-level classes"
- Subhead: "The process-level categories behind the rule names"
- Labels: "Task Failure", "Process Inefficiency", "Unwarranted Continuation"

---

## Section 6: Repo coverage map

**Key Concept**: The repo now has `10 anomaly subtypes` and `9 implemented rules`, but coverage is uneven across classes.

**Content**:
- `wrong_tool_choice` -> `Process Inefficiency` -> P1
- `bad_tool_arguments` -> `Task Failure` -> P2
- `skipped_required_step` -> `Task Failure` -> P3 and P8
- `repeated_step` -> `Process Inefficiency` -> P4
- `continued_after_sufficient_evidence` -> `Unwarranted Continuation` -> P5
- `contradicted_tool_result` -> `Task Failure` -> P6
- `premature_final_answer` -> `Task Failure` -> P7
- `invalid_tool_json` -> `Task Failure` -> P9
- `hallucinated_tool` -> `Task Failure` -> stub
- `unnecessary_replanning` -> `Process Inefficiency` -> stub

**Visual Element**:
- Type: coverage grid
- Subject: subtype chips grouped under the three top-level classes
- Treatment: implemented chips vs stub chips with visual distinction

**Text Labels**:
- Headline: "Coverage by anomaly class"
- Subhead: "Strongest on task failure, thinner on continuation and replanning"
- Labels: "10 anomaly subtypes", "9 implemented rules", "stub", "implemented"

---

## Section 7: Main takeaway

**Key Concept**: The next step is to inspect each rule with two questions: is the label right, and is the trajectory realistic?

**Content**:
- taxonomy and generation strategy are inseparable
- deterministic local edits are great for inspection but weaker on downstream realism
- the remaining stubs show where the current dataset is still thin
- next: Phase 3.2 rule-by-rule walkthrough

**Visual Element**:
- Type: takeaway module
- Subject: two evaluation questions plus a forward arrow into rule study
- Treatment: bold summary card with one next-step pointer

**Text Labels**:
- Headline: "What to carry into Phase 3.2"
- Subhead: "Judge every rule on taxonomy fit and realism"
- Labels: "Is the label right?", "Is the trajectory realistic?", "next: P1-P9 walkthrough"

---

## Data Points (Verbatim)

### Statistics
- "63,484"
- "13"
- "5"
- "10 anomaly subtypes"
- "9 implemented rules"

### Key Terms
- "perturb-and-complete"
- "direct perturbation"
- "Task Failure"
- "Process Inefficiency"
- "Unwarranted Continuation"
- "hallucinated_tool"
- "unnecessary_replanning"
- "P6 contradicted_tool_result"
- "P7 premature_final_answer"

---

## Design Instructions

### Style Preferences
- Technical and implementation-grounded
- Emphasize tradeoffs, taxonomy, and realism warnings more than prose-heavy explanation
- Prefer readable headings and chips over paragraph blocks

### Layout Preferences
- Use a dense modular layout that can hold comparison, taxonomy, coverage, and warning panels together
- Keep the side-by-side generation-strategy comparison visually central

### Other Requirements
- `infographic.png` must be the generated canonical artifact
- Make the asset feel like a debrief of what makes anomalous trajectories believable in practice
