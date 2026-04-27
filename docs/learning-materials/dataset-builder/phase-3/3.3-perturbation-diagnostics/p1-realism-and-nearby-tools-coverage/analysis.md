# Analysis for infographic generation

Core message:
- P1 became more honest. The system stopped inventing fake tool names and started surfacing coverage gaps explicitly.

Best visual angle:
- A "quality over quantity" scoreboard

Key quantitative anchors:
- records evaluated: 3,679
- P1 successes before: 3,679
- fake `_v2` outputs before: 509
- P1 successes after: 3,170
- fake `_v2` outputs after: 0

Best qualitative anchors:
- `terminal -> execute_code` now adapts arguments into Python code
- `search_files -> terminal` now adapts arguments into a shell command
- `patch -> patch_v2` is gone; unmapped tools now skip instead of faking realism

Suggested layout:
- top banner: title + one-line thesis
- left column: before vs after metric cards
- middle column: two example transformation cards
- right column: "what remains" list of top unmapped tools

Typography guidance:
- extremely short labels only
- do not attempt long prose paragraphs inside the image
- prefer exact numbers and terse captions
