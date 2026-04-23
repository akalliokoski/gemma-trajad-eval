Create a clean, highly legible technical infographic PNG in English.

Layout: dense-modules
Style: technical-schematic
Aspect ratio: 16:9 landscape

Topic: Dataset builder codebase orientation

Goal:
Teach a learner how the six main `dataset_builder/` scripts fit together, how data moves through the pipeline, and why stable source IDs plus leakage-safe splits are the most important architectural guardrails.

Hard constraints:
- very high text legibility
- large typography only
- no paragraphs
- no tiny code blocks
- no garbled filler text
- perfect spelling
- use only short labels and short phrases
- dark-on-light blueprint/technical poster feel
- visually crisp boxes, arrows, chips, and folder/file icons

Required content blocks:
1. Title block: "Dataset Builder Codebase Orientation"
2. Six-file backbone panel with these exact filenames:
   - download_hermes.py
   - inspect_traces.py
   - normalize_trajectory.py
   - perturbations.py
   - build_trajad_dataset.py
   - validate_labels.py
3. Dataflow ribbon:
   HF dataset -> data/raw/hermes_filtered.jsonl -> normalized trajectory -> anomaly variants -> train/dev/test + build_manifest.json
4. Inspection panel with short labels:
   list[dict], conversations, trajectory, messages, role/content, from/value
5. Normalization panel with short labels:
   human->user, gpt->assistant, metadata, trajectory_length, tool_call_count
6. Identity guardrail panel with exact terms:
   source_trace_id, var_00, var_01+, same-family split, prevent leakage
7. Perturbation/build panel with exact terms:
   MVP_RULES, ALL_RULES, <tool_call>, coherence screen, build_manifest.json
8. Validation boundary panel with exact terms:
   schema yes, realism no, hallucinated_tool, invalid_tool_json, unnecessary_replanning

Visual guidance:
- use 6 or 7 large modules only
- emphasize arrows and flow more than prose
- make the source_trace_id / prevent leakage panel especially prominent
- show a clear distinction between "structure checks" and "semantic realism"
- overall feel: elegant engineering map, not marketing art
