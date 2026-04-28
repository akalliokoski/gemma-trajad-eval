Create a portrait technical infographic with a dense-modules layout and pop-laboratory visual style.

Title: P3 remove_step_pair
Subtitle: How skipped_required_step works, why bad_step points to a missing location, and why interior pair removal is more believable than terminal truncation.

Use a clean, high-legibility educational design. Very large readable headings. Perfect spelling. No garbled text. Minimal prose blocks. Prefer chips, arrows, cards, small diagrams, and short labels.

Panel 1: What P3 removes
- Show a before/after role sequence.
- Before: system -> user -> assistant tool_call -> tool -> assistant
- Highlight that P3 removes one consecutive assistant tool_call plus tool response pair.
- Labels: skipped_required_step, generation_rule = P3, bad_step = removed assistant index

Panel 2: Real corpus evidence
- Source snapshot: data/interim/hermes_normalized_phase2.jsonl
- Applicable records: 3679
- Minimum valid source length: 5
- Shortest valid shape: system -> user -> assistant tool_call -> tool -> assistant

Panel 3: Why pair selection matters
- Compare two cases:
  - terminal pair removal: can feel like generic truncation
  - non-terminal pair removal: cleaner skipped workflow dependency
- Emphasize the implementation improvement:
  Prefer removing a non-terminal assistant+tool pair when available; fall back to the only available pair otherwise.
- Include a label: preserve assistant ending when possible

Panel 4: What bad_step means
- Show bad_step pointing to a gap where the removed assistant step used to begin.
- State clearly: bad_step marks a missing location, not a surviving corrupted message.

Panel 5: Verification
- Focused tests passed:
  - test_p3_prefers_removing_non_terminal_pair_when_available
  - test_p3_returns_shortest_valid_skip_when_only_one_pair_exists
- Full perturbation test file: 14 passed

Visual tone:
- technical, educational, crisp
- dark-on-light or blueprint-lab palette
- clean arrows and indexing markers
- no screenshots, no code paragraphs, no dense body text

The infographic must read like a polished lab note about one anomaly rule improvement.