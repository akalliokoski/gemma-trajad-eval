# Dataset construction and anomaly taxonomy in TrajAD

Source topic: Phase 0 → Orientation → 0.1 Domain background → second topic in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`

## Questions and answers

### 1) What are the three top-level anomaly classes?
TrajAD organizes anomalous agent trajectories into three top-level classes:

1. Task Failure
2. Process Inefficiency
3. Unwarranted Continuation

These classes are meant to cover not only obvious failed runs, but also trajectories that still finish the task while using a wasteful or unsafe process, and trajectories that should have stopped but keep going.

A useful mental model:
- Task Failure = the agent does not successfully complete the task because its reasoning or execution goes wrong.
- Process Inefficiency = the agent reaches the goal, but the path is unnecessarily long or redundant.
- Unwarranted Continuation = the agent should stop, refuse, or declare completion, but instead keeps acting.

### 2) How many perturbation rules does TrajBench use? How does that compare to this project's 8 rules?
TrajBench uses six perturbation families to synthesize anomalous trajectories. They align with the paper's anomaly taxonomy:

- Task Failure:
  - reasoning-error injection
  - execution-error injection
- Process Inefficiency:
  - loop insertion
  - detour or redundant-subsequence insertion
- Unwarranted Continuation:
  - failure-to-refuse setup
  - redundant-continuation setup

Compared with this repo's current 8 perturbation rules, this project has a slightly broader rule count at the implementation level, but it uses a simpler generation strategy. So the difference is not just 6 versus 8. TrajBench has fewer perturbation families, yet the paper's pipeline is richer because it models what happens after the injected mistake.

### 3) What does perturb-and-complete add that this project does not do?
Perturb-and-complete adds realistic downstream consequences.

TrajBench starts from a successful trajectory, injects an anomaly at a chosen step, and then continues the rest of the trajectory from that corrupted state. That continuation matters because later reasoning, actions, and observations now reflect the consequences of the mistake.

This repo's current dataset builder uses direct perturbation: it edits a step and leaves later steps unchanged. That is simpler and cheaper, but it can create internally inconsistent samples. For example, a later tool response or reasoning step may assume the original state still holds even though an earlier action was corrupted.

So the real advantage of perturb-and-complete is not only realism in a vague sense. It creates coherent bad trajectories whose later steps evolve naturally from the first error. That gives better supervision for both anomaly classification and first-error localization.

### 4) Why do the human agreement rates matter here?
The paper reports strong human agreement:
- 96.2% agreement for anomaly classification
- 94.5% agreement for first-error localization

These numbers matter because they set a quality bar for this repo's later manual-review work.

If this project's synthetic anomalies are confusing, unrealistic, or hard to localize consistently, then downstream supervision quality will suffer. The paper's agreement numbers therefore act as a benchmark for what good anomaly definitions and good trajectory construction should feel like in practice.

## Key takeaway for this project
The main lesson from TrajAD section 3 is that anomaly quality depends on both taxonomy and generation method. A useful dataset is not just a pile of corrupted traces. It needs:
- a clear anomaly taxonomy
- perturbations that map cleanly to that taxonomy
- coherent downstream behavior after the first error
- labels that humans can agree on reliably

That is directly relevant to `dataset_builder/`, because later phases in this repo depend on realistic perturbation rules, stable step labels, and high-confidence manual review.

## Sources
- TrajAD paper: https://arxiv.org/abs/2602.06443
- TrajAD HTML/PDF summary source used for extraction: https://arxiv.org/html/2602.06443
