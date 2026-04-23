Objective: Improve the realism of perturbation rules P5 and P6 without adding model-generated continuation or a heavier perturb-and-complete system.

Implementation facts:
- Updated dataset_builder/perturbations.py.
- Added extract_tool_response_text(content) so P6 can reason from the last tool response body instead of using a hard-coded contradiction marker.
- Added tool_response_looks_empty(content) to distinguish empty-like tool outputs from concrete result-bearing tool outputs.
- P5 no longer appends a dangling assistant tool call.
- P5 now appends a structurally complete unnecessary continuation: assistant tool call -> tool response -> assistant wrap-up.
- P5 marks bad_step at the first unnecessary extra step, not at the final appended message.
- P6 no longer prepends an explicit bracketed marker like [CONTRADICTION].
- P6 now replaces the final assistant answer with a subtle but wrong natural-language conclusion that contradicts whether the last tool response contained a concrete result.
- Updated tests/test_perturbations.py with focused tests for P5 structural completeness and P6 natural-language contradiction behavior.

Verification:
- PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_perturbations.py -v
- 4 passed
- python3 dataset_builder/build_trajad_dataset.py --seed 42
- Generated 56,724 anomalous records
- Coherence screen: kept=56,724 rejected=0
- Split sizes: train=47,973  dev=6,413  test=9,696
- continued_after_sufficient_evidence train count: 4,730
- contradicted_tool_result train count: 4,730
- continued_after_sufficient_evidence test count: 992
- contradicted_tool_result test count: 992
- python3 dataset_builder/validate_labels.py data/processed/all.jsonl --strict
- Validated 64,082 records from data/processed/all.jsonl
- All records valid.

Files involved:
- dataset_builder/perturbations.py
- tests/test_perturbations.py
- data/processed/train.jsonl
- data/processed/dev.jsonl
- data/processed/test.jsonl
- data/processed/all.jsonl
