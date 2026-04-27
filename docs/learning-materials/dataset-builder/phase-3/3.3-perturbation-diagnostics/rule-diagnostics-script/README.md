# Perturbation diagnostics script

This folder contains the first Phase 3.3 perturbation-diagnostics package for the task "Write a perturbation diagnostics script" in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`.

## Files
- `answers.md` — explains what the diagnostics script does, how it computes eligibility/success/failure, and what the real corpus results mean
- `analysis.md` — infographic content analysis and message framing
- `structured-content.md` — infographic-ready content structure
- `media-brief.md` — media brief for this learning slice
- `prompts/infographic.md` — prompt source for PNG generation
- `infographic.png` — current infographic artifact
- `podcast-transcript.json` — canonical transcript for the podcast pipeline
- `podcast-transcript.txt` — rendered transcript text
- `perturbation-diagnostics-snapshot.json` — copied snapshot of the generated diagnostics artifact

## Generated media outside the repo
- Podcast: [local MP3](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-3-perturbation-engine/3.3-perturbation-diagnostics/rule-diagnostics-script/phase-3_3.3-02_perturbation-diagnostics-script.mp3) · [Audiobookshelf UI](https://vps.taild96651.ts.net:13378/)

## Notes
- This slice introduced a reusable script at `dataset_builder/perturbation_diagnostics.py`.
- The generated dataset artifact lives at `data/processed/perturbation_diagnostics.json` and was snapshotted here for learning-material stability.
- The first run confirmed that P1 is now the only rule with meaningful failure volume after removing fake `_v2` fallbacks.
- The infographic is acceptable as a concept-level dashboard summary, but it still contains some AI text corruption and should not be treated as polished final typography.
