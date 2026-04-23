Create a professional infographic following these specifications:

## Image Specifications
- **Type**: Infographic
- **Layout**: bento-grid
- **Style**: technical-schematic
- **Aspect Ratio**: 16:9
- **Language**: en

## Core Principles
- Clean engineering blueprint look
- Strong panel-based hierarchy
- Show the coherence gate clearly as a keep/drop decision point
- Keep text concise and readable
- Preserve the exact verification numbers below

## Content
Title: Task 4 — Lightweight Coherence Screen
Panels:
1. Motivation: direct perturbation can create structurally broken traces; add a lightweight post-perturbation quality gate without introducing a full perturb-and-complete system.
2. Three deterministic checks: dangling assistant tool calls with no immediate tool response; orphan tool responses with no matching preceding assistant tool call; exact adjacent duplicate fragments of the same message type.
3. Pipeline integration: apply_perturbation(...) creates a candidate anomaly; coherence.py returns (plausible, reason); plausible anomalies are kept; implausible anomalies are dropped and counted by rejection reason.
4. Reproducibility and coverage: build_trajad_dataset.py now uses unique_source_ids_in_order(records); same-seed builds had no diff output; repeated_step anomalies remain plausible with repeated_step train count 5,518 and repeated_step test count 1,104.
5. Verification: 13 passed; Generated 29,354 anomalous records; Coherence screen: kept=29,354 rejected=0; All records valid.
6. Files: dataset_builder/coherence.py, dataset_builder/build_trajad_dataset.py, tests/test_coherence.py, tests/test_build_trajad_dataset.py.

Text labels (in en):
- Catch Broken Traces Early
- Three Deterministic Checks
- Screen Right After Perturbation
- Deterministic and Non-Destructive
- Verified End-to-End
- dangling_tool_call
- orphan_tool_response
- duplicate_adjacent_fragment
- unique_source_ids_in_order
- 13 passed
- 29,354 kept
- 0 rejected
- All valid
