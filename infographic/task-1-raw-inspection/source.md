Objective: Make the inspection path trustworthy on the real raw dataset before deeper changes.

Implementation facts:
- dataset_builder/inspect_traces.py supports both role/content and from/value message schemas.
- Added helpers get_role(msg) and get_content(msg).
- count_roles(), print_summary(), and print_sample() use the helpers.
- Summary now reports traces with >=1 tool call and traces with >=2 assistant/tool-call pairs.

Verification:
- PYTHONPATH=. uv run --with pytest --no-project pytest tests/test_inspect_traces.py -v
- python3 dataset_builder/inspect_traces.py data/raw/hermes_filtered.jsonl
- Tests passed: 5
- Real raw-file summary: Total records 3,679; Traces with >=1 tool call 100.0%; Traces with >=2 assistant/tool-call pairs 99.4%

Files involved:
- dataset_builder/inspect_traces.py
- tests/test_inspect_traces.py
