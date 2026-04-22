# Trajectory anomaly detection in the agent context

Source topic: Phase 0 → Orientation → 0.1 Domain background → first topic in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`

## Questions and answers

### 1) What is "trajectory anomaly detection" in the agent context?
In TrajAD, a trajectory is not a GPS route. It is the agent's full execution trace for one task: the instruction plus the sequence of reasoning, actions, and observations across time.

Trajectory anomaly detection means auditing that execution process to answer two questions:
1. Is this trajectory anomalous or normal?
2. If it is anomalous, where is the first erroneous step?

That second part matters because the paper is explicitly about runtime auditing. If the verifier can localize the first bad step, the system can roll back to the previous good state and retry instead of restarting the whole task.

Examples of agent-trajectory anomalies discussed by TrajAD include:
- wrong reasoning that leads to a bad action
- wrong tool choice or wrong tool arguments
- loops, detours, and redundant actions
- continuing to act when the task is already complete or should stop

### 2) What distinguishes it from GPS trajectory anomaly detection?
The key difference is what the word trajectory means.

In GPS trajectory anomaly detection, the trajectory is a path through physical space. The data is usually a sequence of locations, staypoints, durations, or activities. An anomaly is an unusual movement pattern, route, or location behavior.

In agent trajectory anomaly detection, the trajectory is a path through task execution. The data is a process trace made of reasoning, tool use, and observations. An anomaly is therefore a procedural failure, not a geographic outlier.

A concise comparison:

| Dimension | GPS trajectory anomaly detection | Agent trajectory anomaly detection |
|---|---|---|
| Object being modeled | Movement in physical space | Multi-step task execution |
| Typical sequence elements | GPS points, staypoints, durations, activities | Reasoning, actions, tool calls, observations |
| What counts as an anomaly | Unusual route or movement pattern | Wrong reasoning, bad tool use, inefficient process, unwarranted continuation |
| Main supervision target | Trajectory-level or point-level anomaly scoring | Binary detection plus first-error-step localization |
| Why it matters | Detect abnormal mobility behavior | Enable runtime monitoring, rollback, and retry for LLM agents |

LM-TAD is a useful contrast case: it treats trajectories as token sequences of locations and uses language-model style scoring to detect anomalous locations or user-specific movement outliers. That is still a spatial trajectory problem. TrajAD instead audits semantic and procedural correctness in agent execution traces.

### 3) How was TrajBench constructed, and what does perturb-and-complete add?
TrajBench is built from successful agent trajectories using a perturb-and-complete pipeline.

The high-level process is:
1. Start from a clean, successful trajectory.
2. Inject an anomaly at a chosen step.
3. Continue the trajectory from that corrupted state so the downstream steps reflect the consequences of the mistake.

This is stronger than plain perturbation.

If you only perturb one step and leave the rest untouched, the result can look artificial because later steps may no longer make sense. Perturb-and-complete produces a more realistic post-error continuation, so the anomaly is embedded in a coherent but flawed trajectory rather than being an isolated broken token or one-step glitch.

For this repo, that matters because the current dataset builder uses direct perturbation only: it edits one step and leaves later steps unchanged. That is simpler and cheaper, but it can create internal contradictions that would not appear in a naturally unfolding bad trajectory.

## Key takeaway for this project
TrajAD frames the problem as process supervision for LLM agents. The verifier is not just checking whether the final answer looks okay; it is checking whether the execution process stays coherent, efficient, and properly bounded. That is exactly why this dataset-builder project cares about anomaly taxonomy, step labels, and leakage-safe splits.

## Sources
- TrajAD paper: https://arxiv.org/abs/2602.06443
- TrajAD HTML/PDF summary source used for extraction: https://arxiv.org/html/2602.06443
- LM-TAD paper: https://arxiv.org/abs/2409.15366
- LM-TAD HTML source used for extraction: https://arxiv.org/html/2409.15366
