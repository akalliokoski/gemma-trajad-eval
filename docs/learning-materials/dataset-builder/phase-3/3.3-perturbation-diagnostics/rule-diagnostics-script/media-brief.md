# Media brief — perturbation diagnostics script

Objective:
- Explain how the new diagnostics script turns perturbation coverage from intuition into measured rule-by-rule evidence.

Audience:
- The project owner learning how to reason about synthetic anomaly coverage with engineering discipline.

Must-cover points:
- new script path: `dataset_builder/perturbation_diagnostics.py`
- output path: `data/processed/perturbation_diagnostics.json`
- key table columns: eligible, succeeded, failed, success rate
- main finding: P1 has 509 failures and 86.2% success after realism cleanup
- comparison signal: most other rules are effectively 100%
- interpretation: the script turns next-step prioritization into a measurable question

Tone:
- practical
- exact
- best-practice oriented
- more engineering dashboard than tutorial fluff

Visual guidance:
- emphasize the scoreboard and the standout P1 row
- keep labels short and numerical
