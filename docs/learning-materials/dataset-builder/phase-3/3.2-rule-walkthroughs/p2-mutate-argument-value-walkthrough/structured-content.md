# P2 mutate_argument_value walkthrough infographic content

## Title
P2 mutate_argument_value

## Subtitle
Type-aware argument corruption for `bad_tool_arguments`

## Learning objectives
- Same tool, wrong argument
- Realistic corruption depends on value type
- Tiny implementation details can make anomalies much more synthetic

## Module 1 — Rule contract
Headline: Keep the tool, corrupt one value
Points:
- Select an assistant `<tool_call>`
- Choose one argument key
- Mutate only that value
- Label as `anomaly_type = bad_tool_arguments`
- Mark `generation_rule = P2`

## Module 2 — Real string sample
Headline: String corruption should look plausible
Before:
- `terminal.command = "ls -la"`
After:
- `terminal.command = "sl -la"`
Caption:
- Better than `_CORRUPTED`
- Still shell-like, but now wrong

## Module 3 — Real integer sample
Headline: Numbers stay numeric but go bad
Before:
- `read_file.offset = 501`
After:
- `read_file.offset = -498`
Caption:
- Same tool
- Same key
- Wrong retrieval behavior

## Module 4 — Real boolean bug
Headline: Python bool is a subclass of int
Before bug fix:
- `background = true -> -998`
After fix:
- `background = true -> false`
Caption:
- Branch order mattered
- Realistic control-flag corruption is logical, not numeric

## Module 5 — Implementation fix
Headline: Two bounded changes
Points:
- Check `bool` before `int`
- Replace `_CORRUPTED` suffixes with typo/path-like mutations
- Keep the rest of the rule contract unchanged

## Module 6 — Verification
Headline: Tight regression proof
Points:
- Focused tests for path-like string mutation
- Focused tests for boolean toggling
- `uv run pytest tests/test_perturbations.py -v`
- Result: `12 passed`

## Module 7 — Takeaway
Headline: Corrupt values in the way the field itself fails
Points:
- booleans flip
- file paths become nearby wrong paths
- commands become plausible typos
- integers remain numbers but become bad values

## Visual notes
- Technical chips for before/after values
- Arrow notation for mutations
- Highlight the bool/int bug in a caution panel
- Keep body text minimal and highly legible
