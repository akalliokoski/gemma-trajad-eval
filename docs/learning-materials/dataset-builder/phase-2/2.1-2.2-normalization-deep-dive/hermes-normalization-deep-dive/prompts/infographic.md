Create a professional infographic poster in a dense-modules layout and pop-laboratory style. Use a portrait 9:16 aspect ratio. Make the poster highly legible, technical, and diagrammatic. No garbled text. No long paragraphs. Use only short headings, chips, arrows, and compact labels.

Title:
Hermes normalization deep dive
Subtitle:
Phase 2 understanding

Main message:
Normalization is the schema bridge from raw ShareGPT-style Hermes traces to the repo's internal trajectory format. The most important hidden guarantee is stable source_trace_id, because later split assignment depends on trace-family identity being deterministic.

Use these modules with exact short headings:
1. Normalization succeeded
Labels: 3,679 records; 0 errors; hermes_normalized_phase2.jsonl
2. Raw vs normalized
Labels: {from, value}; {role, content}; source_trace_id; metadata
3. Role mapping
Labels: human -> user; gpt -> assistant; system; tool
4. Simple trajectory, richer metadata
Labels: is_anomalous=false; anomaly_type=null; bad_step=null; generation_rule=null; trajectory_length; tool_call_count; has_think
5. Stable trace identity
Labels: source_trace_id; stable_on_repeat: true; trace family; leakage-safe splitting
6. Edge-case audit
Labels: 0 missing category; 0 missing subcategory; 0 empty metadata; no unknown roles
7. Why this script matters
Labels: schema bridge; simple trajectory; stable source IDs; next: perturbation engine

Visual instructions:
- central side-by-side comparison card for raw vs normalized record shape
- arrow diagram for role mapping
- badge or shield feel for stability guarantee
- audit badges with zero counts
- very readable typography
- blueprint/lab technical aesthetic
- exact spelling, no gibberish, no invented labels
