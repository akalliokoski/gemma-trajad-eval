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
- Emphasize metadata enrichment and verification evidence
- Keep text concise and highly readable

## Content
Title: Task 2 — Derived Structural Metadata
Panels:
1. Motivation: keep trajectory shape unchanged while preserving more signal.
2. Helper: derive_trace_metadata computes trajectory_length, tool_call_count, tool_response_count, has_think.
3. Merge point: normalize_record updates existing metadata.
4. Verification: 2 tests passed; smoke test normalized 3,679 records with 0 errors.
5. Files: dataset_builder/normalize_trajectory.py, tests/test_normalize_trajectory.py
