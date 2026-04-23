Create a professional infographic following these specifications:

## Image Specifications
- **Type**: Infographic
- **Layout**: bento-grid
- **Style**: technical-schematic
- **Aspect Ratio**: 16:9
- **Language**: en

## Core Principles
- Clean engineering blueprint look
- Strong panel-based information hierarchy
- Emphasize taxonomy mapping, validation logic, and verification evidence
- Keep text concise and highly readable

## Content
Title: Task 3 — Top-Level Anomaly Classes
Panels:
1. Motivation: leaf anomaly labels alone were not enough; add top-level anomaly_class.
2. Mapping table: wrong_tool_choice -> process_inefficiency, bad_tool_arguments -> task_failure, repeated_step -> process_inefficiency, continued_after_sufficient_evidence -> unwarranted_continuation, skipped_required_step -> task_failure.
3. Pipeline behavior: perturbations assign anomaly_class, build preserves anomaly_class=None for normals, validator enforces both anomalous and normal rules.
4. Verification: 6 tests passed; MVP rebuild wrote 36,712 records; strict validation reported all records valid.
5. Files: dataset_builder/perturbations.py, dataset_builder/validate_labels.py, dataset_builder/build_trajad_dataset.py, tests/test_validate_labels.py, tests/test_perturbations.py.
