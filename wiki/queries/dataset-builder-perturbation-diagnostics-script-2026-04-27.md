# Dataset-builder perturbation diagnostics script

Question: What did the new perturbation diagnostics script establish about current rule coverage in the normalized Hermes corpus?

Answer:
The new diagnostics script established that the perturbation engine is no longer operating on intuition alone. It now has a repeatable corpus-wide coverage artifact with separate counts for eligibility, success, failure, and ineligibility.

## Main result
On the 3,679 normalized records in `data/interim/hermes_normalized_phase2.jsonl`:
- `p1_replace_tool_choice` succeeded on `3170` and failed on `509` eligible records (`86.2%` success)
- `p2_mutate_argument_value` succeeded on `3646` and failed on `32` eligible records (`99.1%` success)
- all other current rules were `100%` on eligible records in this run

## Why this matters
This makes P1 the clear remaining bottleneck.

Before this script, that was a reasonable suspicion based on walkthroughs and cleanup work. After this script, it is a measured fact that can be rechecked after every mapping improvement.

## Design lesson
Separating `eligible` from `failed` matters.

A record that cannot structurally support a rule should not be mixed with a record that looks structurally suitable but still cannot be perturbed. The script keeps those categories separate, which makes the coverage signal much more trustworthy.

## Practical consequence
Future realism work should prioritize whichever rule row remains the outlier after each pass. Right now, that is P1 by a wide margin.

## Related pages
- [[dataset-builder-p1-replace-tool-choice-2026-04-27]]
- [[dataset-builder-p1-realism-coverage-2026-04-27]]
