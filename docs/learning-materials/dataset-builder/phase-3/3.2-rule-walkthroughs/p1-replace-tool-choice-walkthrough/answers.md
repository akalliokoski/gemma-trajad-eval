# P1 replace_tool_choice walkthrough

Source topic: Phase 3 -> Perturbation Engine -> 3.2 Walk through each perturbation rule -> P1 `replace_tool_choice` in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`

## What this artifact covers

This package studies the first perturbation rule on the real normalized corpus, using actual sample trajectories and a small regression fix discovered during inspection.

## Questions and answers

### 1) What is P1 supposed to do?
P1 is the `replace_tool_choice` rule. Its job is to take an assistant step that contains a tool call and change the tool name to a semantically nearby wrong tool.

That makes the trajectory anomalous without corrupting the argument schema. The rule keeps the call structurally valid while making the chosen action procedurally wrong.

In code, P1:
- finds assistant steps that contain `<tool_call>` blocks
- parses the first tool call in the selected step
- looks up the original tool in `NEARBY_TOOLS`
- if a mapping exists, swaps to one of those nearby tools
- otherwise falls back to appending `_v2`
- marks the record as:
  - `is_anomalous=true`
  - `anomaly_type="wrong_tool_choice"`
  - `generation_rule="P1"`
  - `bad_step=<selected assistant step>`

### 2) What happened on a real mapped example?
The cleanest mapped sample came from `trace_000001_var_00`.

In that trace, a multi-tool assistant message originally started with:
- `read_file` on `gateway/graphql_endpoint.py`

After P1, that first tool call became:
- `list_directory` on the same path

That is a good example of what the rule is trying to achieve:
- the call is still structurally valid
- the arguments are preserved
- but the tool choice is procedurally wrong for the assistant's stated intention

This is the strongest version of P1 because `read_file -> list_directory` is at least a plausible nearby mistake rather than a random nonsense tool.

### 3) What happened on unmapped tools?
The real corpus also showed the fallback path very clearly.

Two sampled unmapped tools produced:
- `search_files -> search_files_v2`
- `terminal -> terminal_v2`

These records still passed structural validation, but they reveal the main realism weakness in the current P1 design:
- `_v2` suffixes are mechanically convenient
- but they often do not look like real tool confusion
- they look like made-up tool names rather than believable operator mistakes

So the learning-plan question was exactly right: `search_web_v2`-style fallbacks are usually not realistic enough. A better long-term approach is probably either:
- expand `NEARBY_TOOLS` based on tools that actually appear in the Hermes trace corpus, or
- make P1 skip unmapped tools instead of fabricating `_v2` variants

### 4) What implementation bug did the walkthrough uncover?
The walkthrough exposed a real bug in `replace_tool_call()`.

Before the fix, the helper used a regex substitution that replaced every `<tool_call>...</tool_call>` block in the selected assistant message. That meant if an assistant message contained multiple tool calls, P1 would overwrite all of them with the same wrong replacement.

In the real sample from `trace_000001_var_00`, one assistant message contained three `read_file` calls. The buggy behavior rewrote all three calls to the same replacement tool and same first-call arguments, even though the rule was supposed to perturb only one selected call.

That was not just ugly output. It changed the semantics of unrelated tool calls in the same message and made the anomaly much more synthetic than intended.

### 5) How was the bug fixed?
The fix was intentionally small.

In `dataset_builder/perturbations.py`, both helpers were changed from replacing every match to replacing only the first match:
- `replace_tool_call(...)`
- `replace_tool_call_raw(...)`

The regex substitution now uses `count=1`.

This keeps P1 aligned with the rest of its logic, because the rule already parses only the first tool-call block it chooses to mutate.

### 6) How was the fix verified?
First, a new regression test was added to `tests/test_perturbations.py`.

The new test proves that `replace_tool_call()` only replaces the first tool call inside a multi-tool assistant message and leaves later tool calls intact.

Then verification was run with:
- `uv run pytest tests/test_perturbations.py::test_replace_tool_call_only_replaces_first_tool_call_in_message -v`
- `uv run pytest tests/test_perturbations.py -v`

Results:
- the new focused regression test failed before the fix
- it passed after the fix
- the full perturbations test file passed with `7 passed`

A longer rebuild-and-validate command was also started, but it did not complete within the interactive timeout window during this session, so the strongest completed verification evidence for the implementation fix is the targeted regression test plus the full perturbations test file.

### 7) Does the fixed rule look better on the real sample?
Yes.

After the fix, the mapped `read_file -> list_directory` sample still has three `<tool_call>` blocks in the message, but only the first one is mutated. The later tool calls remain intact.

That is much closer to the intended semantics of a single wrong-tool choice.

So the rule is still not perfect from a realism perspective, but it is now behaving in a more bounded and interpretable way.

### 8) What is the main judgment on P1 right now?
P1 is useful, but mixed.

What is good:
- structurally valid outputs
- clear `bad_step` labeling
- nearby-mapped replacements can create believable wrong actions
- the multi-tool overwrite bug is now fixed

What is weak:
- `_v2` fallback names are often unrealistic
- `NEARBY_TOOLS` coverage is still sparse relative to the real Hermes tool inventory
- some assistant messages bundle multiple tool calls, so even the fixed rule is still working at message level, not at a finer-grained individual-call selection model

### 9) What should happen next?
For the learning path, the right next moves are:
1. mark the P1 walkthrough complete
2. carry the realism warning forward into later rule walkthroughs
3. eventually use the corpus to improve `NEARBY_TOOLS` or skip unmapped tools instead of fabricating `_v2` names

That keeps the project honest: P1 now behaves better technically, but its fallback strategy is still the main realism debt.

## Key takeaway for this project
P1 taught two important lessons at once:
- the conceptual lesson: wrong-tool-choice anomalies are only as good as the realism of the replacement map
- the implementation lesson: even a small regex helper can silently make anomalies much more synthetic than intended if it mutates more of the trajectory than you think

So this first Phase 3.2 walkthrough was not just a reading exercise. It directly improved the perturbation engine.

## Sources
- `dataset_builder/perturbations.py`
- `tests/test_perturbations.py`
- `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
- `p1-sample-comparisons.json`
