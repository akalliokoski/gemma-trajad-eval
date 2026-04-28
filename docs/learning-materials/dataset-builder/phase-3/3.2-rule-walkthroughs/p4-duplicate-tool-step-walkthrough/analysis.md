# Analysis — P4 duplicate_tool_step infographic

## Audience
The learner already understands the dataset-builder pipeline at a high level and wants to understand one perturbation rule deeply enough to trust or improve it.

## Communication goal
Show three things clearly:
1. what P4 does structurally
2. what the real corpus revealed about pair granularity
3. what small implementation change improved realism without adding complexity

## Best layout choice
Use a landscape bento/dashboard layout with 5 large panels.

Why:
- we need one structural rule panel
- one `bad_step` semantics panel
- one corpus evidence panel with the key counts
- one implementation-fix panel
- one verification panel

## Visual style
- dark technical dashboard
- large typography
- subtle terminal/data-engineering vibe
- cards, arrows, and chips instead of paragraphs
- no code blocks
- exact numbers only where they matter

## Key facts to visualize
- P4 = duplicate `(assistant tool_call, tool response)` pair
- duplicate inserted immediately after original
- `bad_step = duplicate assistant step`
- exact byte-for-byte copy
- minimum valid source trajectory length = `5`
- eligible records = `3679`
- eligible pairs = `53191`
- simple pairs = `43912`
- compound pairs = `9279` (`17.4%`)
- mixed simple+compound records = `1850`
- only-compound fallback records = `76`
- implementation fix = prefer simple one-call/one-response pairs when available
- verification = focused P4 tests passed, full perturbations suite `16 passed`, coherence+validator checks `2 passed`

## What to avoid
- dense prose inside the image
- long filenames or long commands
- tiny labels trying to explain every edge case
- any suggestion that the rule now rewrites or paraphrases the duplicate

## Recommended panel plan
1. Title + one-line lesson
2. Before/after structure with arrow and `bad_step`
3. Real corpus evidence numbers
4. Problem: compound pair duplication vs fix: simple-pair preference
5. Verification badges and takeaway

## Readability guardrails
- keep every label short
- use 4 to 8 word labels
- keep commands out of the main image body
- emphasize `17.4%`, `1850`, and `76` as the key realism numbers
