# P4 duplicate_tool_step walkthrough

Source topic: Phase 3 -> Perturbation Engine -> 3.2 Walk through each perturbation rule -> P4 `duplicate_tool_step` in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`

## What this artifact covers

This package studies the fourth perturbation rule on the real normalized corpus, using actual repeated-step examples and a small implementation refinement discovered during the walkthrough.

## Questions and answers

### 1) What is P4 supposed to do?
P4 is the `duplicate_tool_step` rule. It copies one consecutive `(assistant tool_call, tool response)` pair and inserts the duplicate immediately after the original pair.

That makes the anomaly different from P3:
- P3 removes a required step pair
- P4 repeats a completed step pair
- the repeated step is not paraphrased or regenerated
- it is intentionally duplicated byte-for-byte

In code, P4:
- scans the trajectory for assistant steps containing `<tool_call>` followed by a `tool` step
- chooses one eligible pair
- deep-copies both messages
- inserts the copies immediately after the original pair
- marks the record as:
  - `is_anomalous=true`
  - `anomaly_type="repeated_step"`
  - `generation_rule="P4"`
  - `bad_step=<index where the duplicate assistant step begins>`

### 2) Does the duplicated pair appear at the expected index?
Yes.

The duplicate is inserted immediately after the original assistant/tool pair, so:
- if the original pair starts at index `i`
- the duplicate assistant step begins at `i + 2`
- the duplicate tool response follows at `i + 3`

That is why `bad_step` points to the duplicate rather than to the original occurrence.

A focused regression test now locks this in:
- `test_p4_duplicates_pair_with_exact_content_and_marks_duplicate_step`

On the smallest valid base case in `BASE_RECORD`, the original pair starts at index `2`, and the duplicated assistant step begins at index `4`.

### 3) Is `bad_step` set to the first occurrence or the second occurrence?
It is set to the second occurrence: the duplicate.

That is the right semantic choice for this dataset because the first pair is still the clean behavior. The anomaly starts exactly where the repeated pair begins.

This lines up with the validator's rule-aware P4 semantics: `bad_step` must point to the duplicated assistant step and matching tool response, not to the original step that the model should have moved on from.

### 4) Is the duplicate really identical content, byte for byte?
Yes.

The walkthrough verified that both copied messages are exact deep copies of the original assistant and tool messages.

The new P4 regression test checks that:
- output trajectory length is original length plus `2`
- `trajectory[bad_step].content == original_assistant.content`
- `trajectory[bad_step + 1].content == original_tool.content`
- the original pair remains unchanged in place

So the learning-plan requirement is satisfied literally: the duplicate is not a paraphrase and not a regenerated tool call. It is the same bytes.

### 5) What is the minimum trajectory length for P4 to succeed?
On the real normalized corpus snapshot in `data/interim/hermes_normalized_phase2.jsonl`, the minimum valid source trajectory length for P4 was `5`.

That shortest valid shape is:
- system
- user
- assistant tool call
- tool response
- assistant final answer

Duplicating the only pair turns that into a `7`-step trajectory while preserving an assistant ending.

The walkthrough found:
- eligible records: `3679`
- minimum valid source trajectory length: `5`
- single-pair records: `21`
- multi-pair records: `3658`

### 6) What did a shortest real example look like?
A real shortest-case sample came from `trace_000092_var_00`.

That trace had one assistant step containing two tool calls (`session_search` and `skills_list`) plus the matching combined tool response message.

After P4:
- the whole assistant step was duplicated
- the whole tool response step was duplicated
- the trajectory still ended with the same final assistant reply
- `bad_step` pointed to the duplicated assistant step at index `4`

This is important because it shows that P4 duplicates a pair at the message level, not at the single-tool-call level.

### 7) Did the walkthrough uncover an implementation issue?
Yes. The issue was not with `bad_step` labeling. It was with step granularity realism.

The walkthrough found that many eligible assistant/tool pairs are compound pairs, not simple one-call/one-response pairs.

Real corpus counts:
- total eligible assistant/tool pairs: `53,191`
- simple pairs with exactly one `<tool_call>` and one `<tool_response>`: `43,912`
- compound pairs with multiple tool calls and/or multiple tool responses: `9,279`
- compound-pair share: `17.4%`

At the record level:
- `1,753` records had only simple pairs
- `76` records had only compound pairs
- `1,850` records had a mix of simple and compound pairs

That means the old uniform selection policy could choose a compound pair even when a simpler, cleaner repeated-step candidate existed in the same trace.

### 8) Why is that a realism problem?
Because `duplicate_tool_step` is supposed to teach a repeated-step anomaly, not a duplicated bundle of several tool actions packed into one assistant turn.

When the selected assistant message contains multiple tool calls, duplicating that message can repeat:
- several tool invocations at once
- several tool responses at once
- and a much bigger chunk of workflow than the rule name suggests

That is still structurally valid, but it is less focused. The anomaly drifts from:
- "the model unnecessarily repeated one step"

toward:
- "the model repeated an entire compound mini-workflow"

### 9) How was P4 improved?
The fix in `dataset_builder/perturbations.py` is intentionally small.

P4 now:
- still scans all eligible assistant/tool pairs
- counts how many `<tool_call>` blocks appear in the assistant message
- counts how many `<tool_response>` blocks appear in the tool message
- prefers pairs with exactly one tool call and one tool response when such pairs exist
- falls back to any eligible pair only when the record has no simple pair

So the new selection policy is:
- prefer a focused repeated step when possible
- preserve full applicability for the `76` records that only contain compound pairs

### 10) How was the implementation change verified?
Two focused regression tests were added to `tests/test_perturbations.py`.

The new tests verify that:
- P4 duplicates a pair with exact content and marks `bad_step` at the duplicate assistant step
- P4 prefers a simple single-call pair when a record mixes compound and simple candidates

Verification commands:
- `uv run --with pytest --no-project pytest tests/test_perturbations.py::test_p4_duplicates_pair_with_exact_content_and_marks_duplicate_step tests/test_perturbations.py::test_p4_prefers_single_call_pair_when_mixed_with_compound_pairs -v`
- `uv run --with pytest --no-project pytest tests/test_perturbations.py -v`
- `uv run --with pytest --no-project pytest tests/test_coherence.py::test_accepts_repeated_step_perturbation_as_plausible tests/test_validate_labels.py::test_validate_record_rejects_repeated_step_when_bad_step_is_not_duplicate_start -v`

Results:
- both focused P4 tests passed
- the full perturbations test file passed with `16 passed`
- the relevant coherence and validator checks passed with `2 passed`

Real-sample validation also stayed clean: the sampled P4 outputs in `p4-sample-comparisons.json` all show `validation_errors: []` and `plausibility: [true, null]` after assigning the anomaly class.

### 11) What is the main judgment on P4 right now?
P4 is now clearer than before.

What is good:
- `bad_step` semantics are crisp and now explicitly regression-tested
- the duplicate is exact, which makes the anomaly easy to localize
- minimum valid length is simple and well characterized
- the new selection policy keeps the anomaly focused on one repeated step when the trace gives that option

What is still intentionally rough:
- the duplicate remains immediately adjacent to the original pair
- the tool response is repeated exactly, not re-executed with slight variation
- compound assistant messages still exist in the corpus, so some repeated-step examples still duplicate a bundle when there is no simpler candidate

### 12) What should happen next?
For the learning path, the right next moves are:
1. mark the P4 walkthrough complete
2. carry forward the lesson that message-level perturbations should prefer the narrowest plausible unit
3. use the same realism lens on P5 through P8

A good future refinement would be to consider whether adjacent exact-repeat behavior should eventually evolve into a more natural "redundant re-check" pattern. But for the current deterministic dataset-builder stage, the simple-pair preference is the right bounded improvement.

## Key takeaway for this project
P4 taught a different realism lesson from P2 and P3: the important question is not only whether a repeated step exists, but what counts as one step.

If the generator duplicates a simple one-call/one-response pair, the anomaly teaches clean repeated-step behavior.
If it duplicates a compound assistant turn containing several tool calls, the anomaly becomes broader and less precise than the rule name implies.

The walkthrough therefore tightened P4 in a small but meaningful way: keep the anomaly deterministic, keep the duplicate exact, but prefer the narrowest plausible repeated step when the trace allows it.

## Sources
- `dataset_builder/perturbations.py`
- `tests/test_perturbations.py`
- `tests/test_coherence.py`
- `tests/test_validate_labels.py`
- `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
- `p4-sample-comparisons.json`
