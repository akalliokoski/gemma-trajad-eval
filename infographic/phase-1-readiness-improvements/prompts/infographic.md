Create a clean landscape infographic titled "Dataset-builder Phase-1 Readiness Improvements".

Style: technical poster, clean white background, crisp dark text, minimal clutter, strong spacing, simple icons, highly readable labels.

Critical requirement: no garbled text, perfect spelling, large readable headings, short labels only.

Use these exact visible text elements only:

Title:
Dataset-builder Phase-1 Readiness Improvements

Top row cards:
1. UV standard
- .python-version 3.12
- uv.lock
- uv sync --extra dev

2. Bootstrap
- bootstrap_dataset_builder.sh
- sync deps
- create data dirs

3. Inspection
- schema report
- tool stats
- eligibility report

Middle row cards:
4. Perturbations
- new P9 invalid_tool_json
- class: task_failure
- ALL_RULES only

5. Audit
- audit_dataset.py
- streaming JSONL
- split counts
- anomaly counts

6. Data contract
- raw
- interim
- processed
- bronze/silver/gold is doc-only

Bottom row:
Verification
- bootstrap OK
- tests: 32 passed
- strict validation OK
- audit command OK

Key numbers
- raw records: 3,679
- avg length: 32.1
- tool-call traces: 100.0%
- >=2 pairs: 99.4%
- processed: 71,429
- train 53,557
- dev 7,154
- test 10,718

Decision
- keep raw -> interim -> processed
- no bronze/silver/gold rename

Use big typography, short chip labels, and clear section boxes. No paragraphs. No tiny text. No corrupted spelling.
