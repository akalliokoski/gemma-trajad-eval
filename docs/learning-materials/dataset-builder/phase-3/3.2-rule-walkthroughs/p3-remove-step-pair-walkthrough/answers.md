# P3 remove_step_pair walkthrough

Source topic: Phase 3 -> Perturbation Engine -> 3.2 Walk through each perturbation rule -> P3 `remove_step_pair` in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`

## What this artifact covers

This package studies the third perturbation rule on the real normalized corpus, using actual skipped-step examples and a small implementation refinement discovered during the walkthrough.

## Questions and answers

### 1) What is P3 supposed to do?
P3 is the `remove_step_pair` rule. It removes one consecutive `(assistant tool_call, tool response)` pair from an otherwise normal trajectory.

That makes the anomaly different from P1 and P2:
- the tool choice is not changed
- the tool-call JSON is not corrupted
- instead, one required action-and-observation pair simply disappears

In code, P3:
- scans the trajectory for consecutive assistant `<tool_call>` messages followed by a `tool` message
- removes one such pair
- marks the record as:
  - `is_anomalous=true`
  - `anomaly_type="skipped_required_step"`
  - `generation_rule="P3"`
  - `bad_step=<index where the removed assistant step used to begin>`

### 2) What happened on a real corpus example with multiple tool-call pairs?
A real seed-0 sample came from `trace_000000_var_00`.

Before P3, the local window around `bad_step=8` looked like:
- previous tool response
- assistant step calling `terminal`
- tool response for that call
- next assistant step calling `terminal` again

After P3, that middle `(assistant, tool)` pair is gone, so the trajectory jumps directly from the previous tool response into the later assistant step.

This is exactly the kind of narrative damage P3 is meant to create:
- the later reasoning now presupposes a missing check
- the trajectory still looks structurally plausible enough to parse
- but one required evidence-gathering step has vanished

### 3) What is the minimum trajectory length for P3 to succeed?
On the real normalized corpus snapshot in `data/interim/hermes_normalized_phase2.jsonl`, the minimum valid source trajectory length for P3 was `5`.

That shortest case is the simple pattern:
- system
- user
- assistant tool call
- tool response
- assistant final answer

If P3 removes the only tool-call pair from that shape, the result becomes:
- system
- user
- assistant final answer

So the minimum successful P3 case is not a multi-step workflow. It is a single-tool-call trace with one missing required step pair.

### 4) What is `bad_step` set to?
`bad_step` is set to the index where the removed assistant tool-call step used to start.

That matters because the anomalous step no longer exists in the mutated trajectory. So `bad_step` is not pointing at a surviving assistant or tool message. It is pointing at the missing position.

This matches the validator convention already used for `skipped_required_step`: the missing location can legally point at the insertion/removal boundary rather than a still-present message.

### 5) Does the resulting trajectory still “make sense” narratively?
Not fully — and that is the point.

But there is an important difference between:
- a useful skipped-step anomaly, and
- a trajectory that looks gratuitously broken at the ending.

The walkthrough found that the old P3 implementation could remove the last available assistant+tool pair even when earlier pairs existed. In multi-step traces, that sometimes left the mutated trajectory ending on a raw tool response. That made the sample look more like an obviously truncated conversation than a focused missing-step anomaly.

### 6) What implementation issue did the walkthrough uncover?
The issue was not labeling or applicability. It was pair selection realism.

The old rule chose uniformly from all eligible pairs. That meant it could remove a terminal pair in a long trajectory even when a better non-terminal candidate was available.

The practical downside was:
- the anomaly became less about a skipped required step inside the workflow
- and more about the conversation ending in an unnatural place

### 7) How was P3 improved?
The fix in `dataset_builder/perturbations.py` is intentionally small.

P3 now:
- prefers removing a non-terminal `(assistant, tool)` pair when one exists
- falls back to the only available pair when the trace has just one pair

So the new selection policy is:
- preserve an assistant ending when possible
- still allow the shortest valid single-pair case

This keeps the anomaly focused on a missing workflow step rather than on a visibly broken conversation ending.

### 8) What did the shortest real fallback case look like?
A real single-pair fallback example came from `trace_000092_var_00`.

Before P3:
- user asks for coding-standards memory
- assistant calls `session_search`
- tool returns a failure payload
- assistant continues with a follow-up reply

After P3:
- the `(assistant call, tool response)` pair disappears
- the trajectory jumps from the user directly to the later assistant reply

That still ends with an assistant message, and it shows why the minimum valid length is `5`.

### 9) How was the implementation change verified?
Two focused regression tests were added to `tests/test_perturbations.py`.

The new tests verify that:
- P3 prefers removing a non-terminal pair when multiple pairs exist
- P3 still works for the shortest valid single-pair trace and leaves the final assistant answer in place

Verification commands:
- `uv run pytest tests/test_perturbations.py::test_p3_prefers_removing_non_terminal_pair_when_available tests/test_perturbations.py::test_p3_returns_shortest_valid_skip_when_only_one_pair_exists -v`
- `uv run pytest tests/test_perturbations.py -v`

Results:
- both focused tests passed
- the full perturbations test file passed with `14 passed`

Real-sample validation also stayed clean: the sampled P3 outputs in `p3-sample-comparisons.json` all show `validation_errors: []`.

### 10) What is the main judgment on P3 right now?
P3 is strong when it removes an interior dependency step.

What is good now:
- the anomaly is easy to understand conceptually
- `bad_step` has a clear meaning as the missing location
- the minimum valid case is simple and well characterized
- the new selection policy produces cleaner narrative failures in multi-step traces

What is still intentionally rough:
- the resulting trajectory is not supposed to fully “make sense”
- later reasoning may reference evidence that was never gathered
- that narrative mismatch is the signal the model should learn to spot

## Key takeaway for this project
P3 taught a realism lesson that is different from P1 and P2: when you create a missing-step anomaly, the important choice is not just whether a pair can be removed, but which pair should be removed.

If the rule removes an interior dependency step, the trajectory becomes a believable workflow failure.
If it removes a late terminal pair unnecessarily, the trajectory risks looking like a generic truncation artifact instead.

So the walkthrough tightened P3 toward a better failure shape: still broken, but broken for the right reason.

## Sources
- `dataset_builder/perturbations.py`
- `tests/test_perturbations.py`
- `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
- `p3-sample-comparisons.json`
