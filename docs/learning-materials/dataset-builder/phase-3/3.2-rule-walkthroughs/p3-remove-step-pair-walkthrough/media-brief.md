# Media brief — P3 remove_step_pair walkthrough

## Audience
- Primary: the repo owner learning dataset construction, anomaly design, and later fine-tuning/evaluation implications
- Secondary: a future reader trying to understand why `skipped_required_step` needs careful localization and realism

## Goal
Explain what P3 removes, why `bad_step` points to a missing location, what the minimum valid case is, and why preferring non-terminal pair removal improves realism.

## Core ideas to emphasize
1. P3 removes an `(assistant tool_call, tool response)` pair rather than mutating content.
2. The minimum real successful source length is 5 steps.
3. `bad_step` marks where the missing pair used to begin.
4. Interior-pair removal is better than terminal-pair removal when multiple candidates exist.
5. The anomaly should feel like a skipped workflow dependency, not a random truncation artifact.

## Evidence to preserve exactly
- Source corpus snapshot: `data/interim/hermes_normalized_phase2.jsonl`
- Applicable record count: `3679`
- Minimum valid trajectory length: `5`
- Focused verification: two new P3 tests passed
- Broader verification: `uv run pytest tests/test_perturbations.py -v` -> `14 passed`

## Tone
- Technical but teachable
- Emphasize the one key design insight: “missing-step realism depends on which pair you delete”
- Avoid generic boilerplate about anomaly detection

## Artifacts this brief supports
- `analysis.md`
- `structured-content.md`
- `prompts/infographic.md`
- `podcast-transcript.json`
- `podcast-transcript.txt`
- `infographic.png`
