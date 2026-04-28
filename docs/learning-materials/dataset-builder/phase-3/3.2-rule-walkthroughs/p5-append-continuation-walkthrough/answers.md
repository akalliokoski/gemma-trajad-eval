# P5 append_continuation walkthrough

Source topic: Phase 3 -> Perturbation Engine -> 3.2 Walk through each perturbation rule -> P5 `append_continuation` in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`

## What this artifact covers

This package studies the fifth perturbation rule on the real normalized corpus, using actual continued-after-answer examples and one bounded realism improvement discovered during the walkthrough.

## Questions and answers

### 1) What is P5 supposed to do?
P5 is the `append_continuation` rule. It takes a trajectory that already ends with an assistant answer and appends an extra assistant -> tool -> assistant tail after that answer.

The intended anomaly is `continued_after_sufficient_evidence`:
- the task was already complete
- but the agent keeps going anyway
- the extra work is structurally valid, just unnecessary

In code, P5 now:
- requires the source trajectory to end on an assistant message
- finds existing `(assistant tool_call, tool response)` pairs in the trace
- prefers a lightweight inspection/search pair when one exists
- copies that real pair to the end of the trajectory
- adds a short wrap-up assistant message saying the prior answer still stands
- marks the record as:
  - `is_anomalous=true`
  - `anomaly_type="continued_after_sufficient_evidence"`
  - `generation_rule="P5"`
  - `bad_step=<index of the first appended assistant step>`

### 2) What fake tool call gets appended?
After the walkthrough improvement, P5 no longer invents a hard-coded `search_web` call.

Instead, it appends a copied tool-call pair taken from the trajectory itself. In practice that means the fake continuation usually replays one already-established inspection step such as:
- `terminal`
- `read_file`
- `browser_snapshot`
- `search_files`

On the current normalized corpus snapshot in `data/interim/hermes_normalized_phase2.jsonl`, the top appended tool names were:
- `terminal`: `2146`
- `read_file`: `546`
- `browser_snapshot`: `314`
- `search_files`: `113`

### 3) Is the appended step realistic?
Yes, much more than the prior version.

The old P5 always appended a generic `search_web` call with a canned query string, even though none of the real corpus traces used `search_web` at all. On the current snapshot:
- eligible P5 source records: `3182`
- traces whose established tool set did not include `search_web`: `3182`
- so the old rule injected an out-of-distribution tool name in effectively every case

The improved rule is more realistic because:
- the appended tool name already exists in the trace's established tool set
- the appended tool response is copied from a real earlier response in the same trajectory
- the failure now looks like one more unnecessary verification pass, not like a synthetic tool suddenly appearing from nowhere

### 4) Does the tool name exist in the trace's established tool set?
Yes, by construction in the improved rule.

P5 now copies an existing assistant/tool pair from the source trajectory, so the appended tool name is already present in that trajectory. That directly answers the learning-plan question: the continuation uses an established tool rather than inventing a new one.

### 5) What is `bad_step` set to?
`bad_step` is the index of the first appended assistant step.

That means it points to the exact moment where the already-complete task turns into an unwarranted continuation. It does not point to the final wrap-up and it does not point back to the original earlier pair that was copied.

### 6) What implementation issue did the walkthrough uncover?
The issue was realism, not structure.

Task 5 had already fixed the most obvious structural bug by making P5 append a complete assistant -> tool -> assistant continuation instead of a dangling tool call. But the rule still used a hard-coded `search_web` continuation that did not match the Hermes corpus.

The walkthrough made that mismatch concrete:
- `3182 / 3182` eligible records lacked prior `search_web` usage
- common real tool ecosystems in these traces were things like `terminal`, `read_file`, `search_files`, and browser tools instead

So the structural contract was fine, but the content of the continuation was still too synthetic.

### 7) How was P5 improved?
The fix in `dataset_builder/perturbations.py` is intentionally bounded.

P5 now:
- collects all existing assistant/tool pairs in the trajectory
- prefers a lightweight verification-style pair when available:
  - `search_web`
  - `search_files`
  - `read_file`
  - `terminal`
  - `browser_snapshot`
  - `browser_console`
  - `browser_get_images`
  - `session_search`
- otherwise falls back to the last available pair
- copies the chosen assistant and tool steps exactly, then appends the wrap-up assistant reply

This keeps the anomaly deterministic while pushing it toward a much better failure shape.

### 8) How often does the preferred lightweight heuristic apply?
Almost always on the current corpus snapshot.

From `p5-sample-comparisons.json`:
- eligible records: `3182`
- preferred lightweight choice used: `3150` (`98.99%`)
- fallback to a non-preferred pair: `32` (`1.01%`)

That matters because the original last pair is often a side-effect-heavy action like `write_file`, `patch`, or `process`, which reads less like "one more gratuitous check" and more like a strange extra task execution after the answer.

### 9) What did real examples show?
The most useful examples were mixed traces where the last pair was not the best continuation candidate.

Examples from `p5-sample-comparisons.json` showed patterns like:
- original final pair = `write_file`, but a better earlier `read_file` pair existed
- original final pair = `process`, but a better earlier `terminal` health-check pair existed
- original final pair = `todo`, but a better earlier `read_file` inspection pair existed

Those are exactly the cases where the heuristic matters. The continued-after-answer anomaly becomes more believable when the agent pointlessly re-checks something rather than launching one more mutation after the work is already done.

### 10) What is the minimum trajectory length for P5 to succeed?
On the current normalized corpus snapshot, the minimum valid source trajectory length for P5 was `5`.

That shortest valid case is:
- system
- user
- assistant tool call
- tool response
- assistant final answer

P5 then appends:
- copied assistant tool call
- copied tool response
- assistant wrap-up saying the original answer still stands

So the minimum successful P5 case becomes a trajectory of length `8`.

### 11) How was the implementation change verified?
Two focused regression tests were added or updated in `tests/test_perturbations.py`.

The new tests verify that:
- P5 appends an existing assistant/tool pair plus a wrap-up, and `bad_step` points at the first appended step
- when a trace mixes a lightweight verification pair with a later side-effect-heavy pair, P5 prefers the lightweight established pair

Verification commands:
- `uv run --with pytest --no-project pytest tests/test_perturbations.py::test_p5_appends_existing_final_tool_pair_as_unnecessary_continuation tests/test_perturbations.py::test_p5_prefers_established_lightweight_verification_pair_when_mixed -v`
- `uv run --with pytest --no-project pytest tests/test_perturbations.py -v`
- `uv run --with pytest --no-project pytest tests/test_validate_labels.py::test_validate_record_rejects_continuation_when_bad_step_skips_first_extra_step -v`

Results:
- both focused P5 tests passed
- the full perturbations test file passed with `17 passed`
- the P5 label-validation check passed

### 12) What is the main judgment on P5 right now?
P5 is now in a much better place.

What is good now:
- it remains deterministic and structurally simple
- the continuation uses an established tool name from the trace
- the appended tool response is internally consistent because it is copied from the trace
- the preferred-pair heuristic makes the anomaly feel like one more needless verification pass instead of a random synthetic action

What is still intentionally rough:
- the continuation is still copied, not newly generated
- a few fallback cases still use non-preferred tools because no better option exists
- the wrap-up sentence is generic across traces

Those remaining simplifications are acceptable for this project because the main realism bug was the invented out-of-distribution tool call, and that bug is now removed.

## Key takeaway for this project
P5 taught a different realism lesson from P3 and P4: even when an anomaly is structurally correct, it can still be distributionally wrong.

The old P5 already had the right shape, but it used the wrong content. The walkthrough showed that believable unwarranted continuation depends on staying inside the trace's established tool ecosystem. Once P5 copies a real verification-style pair instead of inventing `search_web`, the anomaly reads much more like a bad but plausible agent decision.

## Sources
- `dataset_builder/perturbations.py`
- `tests/test_perturbations.py`
- `tests/test_validate_labels.py`
- `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
- `p5-sample-comparisons.json`
