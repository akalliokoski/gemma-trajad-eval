# TrajAD perturbation context

Source topic: Phase 3 -> Perturbation Engine -> 3.1 Domain context in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`

## What this artifact covers

This package combines the two Phase 3.1 study questions into one learning slice:
1. compare TrajAD's `perturb-and-complete` generation strategy against this repo's `direct perturbation` strategy
2. map this repo's anomaly subtypes onto the TrajAD top-level taxonomy and identify what is implemented versus still stubbed

## Questions and answers

### 1) What does TrajAD mean by `perturb-and-complete`?
TrajAD starts from a successful trajectory, injects an anomaly at a chosen step, and then continues the rest of the trajectory from that corrupted state.

That means the later reasoning, actions, and observations are no longer copied from the clean run. They are regenerated as if the mistake were real. The paper uses this to make downstream behavior look like a coherent bad execution path rather than a one-line edit pasted into an otherwise clean trace.

This matters because TrajAD is trying to supervise two things at once:
- anomaly detection
- first-error localization for rollback-and-retry

A trajectory that evolves naturally after the first error gives the verifier a much more realistic process-level signal.

### 2) What does this repo currently do instead?
This repo currently uses direct perturbation.

In practice, that means a rule edits one step inside an already-normalized trajectory and leaves the later steps mostly unchanged. Examples in `dataset_builder/perturbations.py`:
- P1 changes the tool name inside an existing `<tool_call>`
- P2 mutates one argument value
- P3 removes a tool-call / tool-response pair
- P4 duplicates one pair
- P5 appends extra unnecessary continuation steps
- P6 alters the final answer so it contradicts the tool result
- P7 truncates the trajectory before the real decision and inserts a premature answer
- P8 swaps dependent tool-step pairs
- P9 corrupts tool-call JSON

So the repo's method is local edit first, not regenerate-the-rest-of-the-trace afterward.

### 3) What are the tradeoffs between perturb-and-complete and direct perturbation?
`Perturb-and-complete` is stronger on realism but more expensive and more operationally complex.

Benefits of TrajAD-style perturb-and-complete:
- downstream steps reflect the consequences of the mistake
- anomaly classification and localization are trained on more coherent bad trajectories
- labels are less likely to feel like mechanical text edits

Costs of perturb-and-complete:
- you need an extra generation stage after each corruption
- continuation quality becomes part of dataset quality risk
- reproducibility and cost control are harder than for deterministic local edits

Benefits of this repo's direct perturbation:
- simple, deterministic, and cheap
- easy to test rule by rule
- easier to inspect exactly what changed at the corrupted step

Costs of direct perturbation:
- later steps may still assume the clean world state
- some anomalies can feel too synthetic because only one local edit changed
- first-error localization may become easier for the wrong reason: the trace looks internally inconsistent immediately after the edit

### 4) When does the simpler direct-perturbation approach fail most obviously?
The biggest failure mode is internal contradiction between the corrupted step and the later clean steps.

Two especially important examples from the current rule set:
- P6 `contradicted_tool_result`: the final assistant answer is changed, but the rest of the trajectory still contains the original evidence path. The anomaly can be useful, but it is still a local edit rather than a naturally evolved bad run.
- P7 `premature_final_answer`: the rule truncates the trajectory before the real resolution and inserts a fake early conclusion. This creates a valid anomaly type, but it is not the same as watching an agent continue from a mistaken belief state through several later steps.

P3 and P8 also show the same pattern in a different form: removing or reordering step pairs creates a broken trajectory, but the later content was not regenerated to reflect the break.

So the honest lesson is that direct perturbation is acceptable for a first-generation builder, but it tends to create anomalies that are structurally clear before they are behaviorally realistic.

### 5) What are TrajAD's top-level anomaly classes?
TrajAD groups anomalies into three top-level classes:

1. Task Failure
2. Process Inefficiency
3. Unwarranted Continuation

The paper's framing is useful because it moves the project away from a bag of rule names and toward a process-level interpretation:
- Task Failure = the agent does not complete the task correctly
- Process Inefficiency = the task may complete, but the path is unnecessarily wasteful or redundant
- Unwarranted Continuation = the agent should stop, refuse, or declare completion, but keeps acting

### 6) How does this repo's taxonomy map onto those classes?
From `ANOMALY_TYPE_TO_CLASS` in `dataset_builder/perturbations.py`, the current mapping is:

| Repo anomaly subtype | TrajAD top-level class | Current rule coverage |
|---|---|---|
| `wrong_tool_choice` | `process_inefficiency` | implemented by P1 |
| `bad_tool_arguments` | `task_failure` | implemented by P2 |
| `skipped_required_step` | `task_failure` | implemented by P3 and P8 |
| `repeated_step` | `process_inefficiency` | implemented by P4 |
| `premature_final_answer` | `task_failure` | implemented by P7 |
| `continued_after_sufficient_evidence` | `unwarranted_continuation` | implemented by P5 |
| `contradicted_tool_result` | `task_failure` | implemented by P6 |
| `hallucinated_tool` | `task_failure` | stub only |
| `invalid_tool_json` | `task_failure` | implemented by P9 |
| `unnecessary_replanning` | `process_inefficiency` | stub only |

Two important observations:
- the repo currently has 10 anomaly subtypes
- it now has 9 implemented perturbation rules, not 8, because P9 `invalid_tool_json` has already been added

### 7) Which anomaly classes are well covered right now, and which are thin?
Task Failure is the most heavily covered class.

Task Failure currently includes implemented support for:
- `bad_tool_arguments`
- `skipped_required_step`
- `premature_final_answer`
- `contradicted_tool_result`
- `invalid_tool_json`

Process Inefficiency has partial but meaningful coverage:
- `wrong_tool_choice`
- `repeated_step`
- `unnecessary_replanning` is still a stub

Unwarranted Continuation is the thinnest implemented class:
- `continued_after_sufficient_evidence` exists via P5
- but there is no broader family of continuation/refusal variants yet

So the current builder is strongest on "the agent did something wrong" and weaker on richer variants of wasteful or should-have-stopped behavior.

### 8) Which subtypes are still stubs, and why do they matter?
The two remaining stub anomaly subtypes are:
- `hallucinated_tool`
- `unnecessary_replanning`

Why they matter:
- `hallucinated_tool` would capture a realistic task-failure mode where the agent invokes a tool that is unavailable, fabricated, or unsupported by the environment
- `unnecessary_replanning` would capture a process-inefficiency mode where the agent burns steps on needless replanning without changing the task state productively

These are exactly the kinds of failures that make agent traces feel realistic rather than toy-like. So leaving them stubbed does not break the current builder, but it does narrow the diversity of procedural failure modes.

### 9) What should the learner carry forward into Phase 3.2?
The most important mindset shift is this:

Phase 3 is not just about reading one rule after another. It is about judging whether each rule creates a believable failure mode hypothesis.

That means for each rule you now need to ask two separate questions:
1. Is the anomaly label/category correct?
2. Is the generated trajectory a realistic example of that category?

TrajAD gives the benchmark standard: realistic anomalous trajectories should look like the downstream world actually changed after the first mistake. This repo's direct perturbation rules are still useful, but they should be studied with an eye toward where realism breaks.

## Key takeaway for this project
The main lesson from Phase 3.1 is that taxonomy and generation strategy are inseparable.

A good anomaly dataset is not just a larger list of perturbation names. It needs:
- a clear mapping from rule to process-level failure class
- realistic downstream consequences after the first error
- enough subtype coverage that the verifier is not overtrained on one failure family
- honest awareness of where deterministic direct perturbation is good enough and where it becomes too synthetic

That sets up the next study slice cleanly: inspect each perturbation rule one by one and judge both correctness and realism.

## Sources
- TrajAD paper abstract and HTML summary: https://arxiv.org/abs/2602.06443 and https://arxiv.org/html/2602.06443
- Repo implementation: `dataset_builder/perturbations.py`
- Repo learning plan: `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
