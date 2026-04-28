# P2 mutate_argument_value walkthrough

Source topic: Phase 3 -> Perturbation Engine -> 3.2 Walk through each perturbation rule -> P2 `mutate_argument_value` in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`

## What this artifact covers

This package studies the second perturbation rule on the real normalized corpus, using actual mutated tool calls and a small implementation cleanup discovered during the walkthrough.

## Questions and answers

### 1) What is P2 supposed to do?
P2 is the `mutate_argument_value` rule. It keeps the same tool name but corrupts one argument value inside the selected tool call.

That means the anomaly is narrower than P1:
- the assistant still chose the same tool
- the tool-call JSON still parses
- but one argument is now wrong enough to make the action fail or become misleading

In code, P2:
- finds assistant steps that contain `<tool_call>` blocks
- parses the selected tool call
- chooses one argument key
- mutates that one value according to its Python type
- marks the record as:
  - `is_anomalous=true`
  - `anomaly_type="bad_tool_arguments"`
  - `generation_rule="P2"`
  - `bad_step=<selected assistant step>`

### 2) What happened on a real string-argument example?
A real seed-0 sample came from `trace_000000_var_00`.

The clean call was:
- tool: `terminal`
- argument: `command="ls -la"`

After P2, the call became:
- `command="sl -la"`

This is materially better than the older `_CORRUPTED` suffix strategy.

Why it is better:
- it still looks like something an operator or model could plausibly emit
- it is syntactically valid shell text
- it changes behavior in a sharp way, because `sl` is no longer the intended command

So the answer to the learning-plan question is yes: the literal `_CORRUPTED` suffix was too obvious. A typo-style mutation is a more believable wrong-argument anomaly.

### 3) What happened on a real integer-argument example?
A real seed-0 integer sample came from `trace_000001_var_00`.

The clean call included:
- tool: `read_file`
- argument: `offset=501`

After P2, that became:
- `offset=-498`

This mutation is strong in a different way:
- it stays valid JSON
- it keeps the same tool and the same argument key
- but it makes the read offset obviously wrong for the assistant's stated goal of continuing further down the file

This is a good example of a localized, schema-valid failure.

### 4) Did the walkthrough uncover an implementation issue?
Yes. The walkthrough exposed a type-ordering bug in the original P2 logic.

In Python, `bool` is a subclass of `int`.

The previous branch order checked `int` before `bool`, so a boolean argument like:
- `background=true`

was being mutated numerically instead of logically. On a real sample, the old code turned:
- `background=true`
into:
- `background=-998`

That is bad for two reasons:
- it is much more synthetic than intended
- it stops being a believable wrong-argument mutation for a boolean field

### 5) How was the bug fixed?
The fix was intentionally small and bounded.

Two improvements were made in `dataset_builder/perturbations.py`:

1. Boolean handling now runs before integer handling.
   - `true` now mutates to `false`
   - `false` would mutate to `true`

2. String mutation no longer appends the literal `_CORRUPTED` marker.
   - path-like strings now become nearby wrong filenames such as `settings.py -> settings-old.py`
   - generic strings now get typo-style corruption instead of an explicit corruption tag

These changes preserve the core P2 contract while producing more believable argument-level anomalies.

### 6) What did the real boolean sample look like after the fix?
A real seed-0 boolean sample came from `trace_000060_var_00`.

The clean tool call included:
- tool: `terminal`
- argument: `background=true`

After the fix, it became:
- `background=false`

That is exactly the kind of mutation P2 should make for a boolean control flag:
- same tool
- same JSON schema
- same argument key
- different runtime behavior

This is much more realistic than the old integer-like corruption.

### 7) How was the implementation change verified?
First, two focused regression tests were added to `tests/test_perturbations.py`.

The new tests verify that:
- path-like string arguments mutate without the `_CORRUPTED` suffix
- boolean arguments toggle to `False` instead of being treated as integers

Verification commands:
- `uv run pytest tests/test_perturbations.py::test_p2_mutates_path_like_strings_without_corrupted_suffix tests/test_perturbations.py::test_p2_toggles_boolean_arguments_instead_of_treating_them_as_ints -v`
- `uv run pytest tests/test_perturbations.py -v`

Results:
- the two focused tests passed
- the full perturbations test file passed with `12 passed`

Real-sample validation also stayed clean: the sampled P2 outputs in `p2-sample-comparisons.json` all produced `validation_errors: []` after assigning the anomaly class.

### 8) What is the main judgment on P2 right now?
P2 looks stronger than before, but still mixed in an honest way.

What is good:
- the anomaly stays tightly localized to one argument value
- the tool name remains unchanged, which isolates the failure mode cleanly
- integer and boolean mutations now look more semantically grounded
- string corruption is less cartoonish than a `_CORRUPTED` suffix

What is still weak:
- some mutations are still generic rather than tool-aware
- list mutation currently collapses to `[]`, which is useful but often blunt
- the rule still operates at the argument-value level, not at a richer task-semantic level

### 9) What should happen next?
For the learning path, the right next moves are:
1. mark the P2 walkthrough complete
2. carry forward the rule-design lesson that type-aware mutation matters
3. keep improving P2 toward tool-aware value corruption where that can be done without over-engineering

A good next refinement would be to specialize by argument role:
- file paths
- shell commands
- search queries
- pagination offsets
- structured todo payloads

## Key takeaway for this project
P2 taught an important realism lesson: argument corruption should be wrong in the way the field itself is wrong.

That means:
- booleans should flip
- file paths should become nearby bad paths
- commands should look like plausible typos or wrong invocations
- numbers should stay numbers but become bad values

The walkthrough therefore did more than answer the study questions. It tightened the perturbation engine so `bad_tool_arguments` examples are less synthetic and easier to trust later during training and evaluation.

## Sources
- `dataset_builder/perturbations.py`
- `tests/test_perturbations.py`
- `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
- `p2-sample-comparisons.json`
