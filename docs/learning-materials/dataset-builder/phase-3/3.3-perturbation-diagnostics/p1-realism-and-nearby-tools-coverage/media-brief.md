# Media brief — P1 realism and NEARBY_TOOLS coverage improvement

Objective:
- Explain why removing `_v2` fallback names improves anomaly realism even though P1 coverage drops.

Audience:
- The project owner learning how to turn Phase 0 realism lessons into disciplined perturbation-engine design.

Must-cover points:
- old problem: fake `_v2` tool names
- new policy: skip unmapped tools instead of fabricating names
- curated improvements: `terminal` and `search_files` now adapt arguments
- corpus result: success 3679 -> 3170, fake `_v2` count 509 -> 0
- interpretation: precision over recall, not an accidental regression

Tone:
- Practical, elegant, best-practice oriented
- Treat this as a dataset quality gate, not as a generic refactor

Visual guidance:
- Prefer a compact scoreboard with before/after metrics and 2 example transformations
- Keep labels short and typography large
