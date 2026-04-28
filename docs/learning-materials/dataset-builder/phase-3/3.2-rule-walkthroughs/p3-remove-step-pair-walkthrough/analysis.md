# Infographic analysis — P3 remove_step_pair walkthrough

## Content type
This is a technical walkthrough of one perturbation rule plus one bounded implementation refinement discovered during corpus inspection.

## Audience need
The reader needs to quickly grasp:
- what P3 deletes
- what `bad_step` means after deletion
- why the shortest valid case is length 5
- why non-terminal removal is a better realism policy than terminal removal

## Information density
Medium-high. There are a few exact numbers and one important before/after structural concept.

## Recommended layout
- Layout: `dense-modules`
- Style: `pop-laboratory`
- Aspect: `portrait`

Why:
- the topic has multiple tightly related concepts rather than a pure timeline
- we need one module for rule mechanics, one for real-corpus evidence, one for the implementation fix, and one for verification
- the pop-laboratory style fits technical explanation while still making the structural before/after concept visually distinct

## Visual strategy
Use 4 main panels:
1. Rule contract: remove assistant+tool pair
2. Real-corpus evidence: 3679 applicable records, minimum length 5
3. Realism fix: prefer non-terminal pair removal
4. Verification: two focused tests + 14 passed overall

## Readability constraints
- Keep body text short
- Prefer step chips and labeled arrows over paragraphs
- Explicitly request very high text legibility and perfect spelling
- Use tiny snippets sparingly; focus on role sequences like `tool -> assistant/tool removed -> assistant`

## Must-preserve facts
- `anomaly_type = skipped_required_step`
- `generation_rule = P3`
- `bad_step = removed assistant step index`
- `applicable_record_count = 3679`
- `minimum_valid_trajectory_length = 5`
- `full perturbation test file = 14 passed`
