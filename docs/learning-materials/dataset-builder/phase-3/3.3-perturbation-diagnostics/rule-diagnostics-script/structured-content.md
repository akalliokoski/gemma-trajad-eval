# Structured infographic content

Title:
- Perturbation diagnostics

Subtitle:
- Measure every rule, surface the real bottleneck

Artifact cards:
- Script: dataset_builder/perturbation_diagnostics.py
- Output: data/processed/perturbation_diagnostics.json

Scoreboard cards:
- Records checked: 3679
- P1 success: 86.2%
- P1 failures: 509
- P2 success: 99.1%
- P3 to P9 on eligible records: ~100%

Method card:
- Columns: eligible, succeeded, failed, success rate
- Keep ineligible separate from failed

Why P1 stands out:
- realism cleanup removed fake v2 fallbacks
- unmapped tools now fail visibly
- next mapping work can be targeted

Next-step card:
- expand curated replacements
- use diagnostics after each cleanup pass

Footer takeaway:
- the project now has a repeatable rule-by-rule coverage meter
