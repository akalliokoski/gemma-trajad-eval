# Dataset Builder Phase 0 Improvements podcast playlist

This playlist turns the implemented plan `docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md` into a nine-episode sequence:
- one introduction
- one episode per implemented task
- one finale about how the completed tasks change the following steps

## Why this structure

The plan is easier to learn as a dependency chain than as a flat checklist. The introduction frames the seven tasks as a quality staircase, each task episode explains one implemented improvement and its downstream effect, and the finale connects the completed work to later evaluation, training-readiness, and future model-assisted extensions.

## Execution recommendation

Recommended approach: coordinator-local artifact creation plus a bounded VPS batch render for audio.

Why:
- playlist creation is mostly deterministic file work
- the VPS is the control plane and these episodes do not require GPU
- stateless worker fanout would add overhead without adding insight
- this playlist rendered cleanly through the normal podcast pipeline without needing an overnight tmux mission

## Audiobookshelf delivery
- Playlist created: `gemma-trajad-eval — Dataset Builder — Phase 0 Improvements task-by-task` (id `65414a96-7e7d-45fd-b9fe-e04599c13ded`)
- Playlist show folder: `file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.4-implementation-synthesis/dataset-builder-phase-0-improvements-playlist`
- Audiobookshelf UI: https://vps.taild96651.ts.net:13378/

## Episodes
- 1. `phase-0-playlist-01_intro_quality-staircase` — Phase 0 improvements playlist intro: why these seven tasks are a quality staircase (6 minutes)
  - Introduces the seven-task sequence as a compact quality staircase that unlocks safer later training, evaluation, and future model-assisted steps.
  - MP3: [local file](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.4-implementation-synthesis/dataset-builder-phase-0-improvements-playlist/phase-0-playlist-01_intro_quality-staircase.mp3)
- 2. `phase-0-playlist-02_task-1_repair-raw-data-inspection-for-sharegpt-style-he` — Task 1: Repair raw-data inspection for ShareGPT-style Hermes traces (5 minutes)
  - Explains the implemented Task 1 improvement, why it matters, and what later steps it unlocks.
  - MP3: [local file](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.4-implementation-synthesis/dataset-builder-phase-0-improvements-playlist/phase-0-playlist-02_task-1_repair-raw-data-inspection-for-sharegpt-style-he.mp3)
- 3. `phase-0-playlist-03_task-2_add-derived-structural-metadata-during-normaliza` — Task 2: Add derived structural metadata during normalization (5 minutes)
  - Explains the implemented Task 2 improvement, why it matters, and what later steps it unlocks.
  - MP3: [local file](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.4-implementation-synthesis/dataset-builder-phase-0-improvements-playlist/phase-0-playlist-03_task-2_add-derived-structural-metadata-during-normaliza.mp3)
- 4. `phase-0-playlist-04_task-3_add-explicit-top-level-anomaly-classes` — Task 3: Add explicit top-level anomaly classes (5 minutes)
  - Explains the implemented Task 3 improvement, why it matters, and what later steps it unlocks.
  - MP3: [local file](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.4-implementation-synthesis/dataset-builder-phase-0-improvements-playlist/phase-0-playlist-04_task-3_add-explicit-top-level-anomaly-classes.mp3)
- 5. `phase-0-playlist-05_task-4_add-a-lightweight-coherence-screen-after-perturb` — Task 4: Add a lightweight coherence screen after perturbation (5 minutes)
  - Explains the implemented Task 4 improvement, why it matters, and what later steps it unlocks.
  - MP3: [local file](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.4-implementation-synthesis/dataset-builder-phase-0-improvements-playlist/phase-0-playlist-05_task-4_add-a-lightweight-coherence-screen-after-perturb.mp3)
- 6. `phase-0-playlist-06_task-5_make-p5-and-p6-more-realistic` — Task 5: Make P5 and P6 more realistic (5 minutes)
  - Explains the implemented Task 5 improvement, why it matters, and what later steps it unlocks.
  - MP3: [local file](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.4-implementation-synthesis/dataset-builder-phase-0-improvements-playlist/phase-0-playlist-06_task-5_make-p5-and-p6-more-realistic.mp3)
- 7. `phase-0-playlist-07_task-6_deepen-validation-for-first-error-localization` — Task 6: Deepen validation for first-error localization (5 minutes)
  - Explains the implemented Task 6 improvement, why it matters, and what later steps it unlocks.
  - MP3: [local file](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.4-implementation-synthesis/dataset-builder-phase-0-improvements-playlist/phase-0-playlist-07_task-6_deepen-validation-for-first-error-localization.mp3)
- 8. `phase-0-playlist-08_task-7_add-build-manifests-and-perturbation-diagnostics` — Task 7: Add build manifests and perturbation diagnostics (5 minutes)
  - Explains the implemented Task 7 improvement, why it matters, and what later steps it unlocks.
  - MP3: [local file](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.4-implementation-synthesis/dataset-builder-phase-0-improvements-playlist/phase-0-playlist-08_task-7_add-build-manifests-and-perturbation-diagnostics.mp3)
- 9. `phase-0-playlist-09_finale_how-phase-0-changes-next-steps` — Finale: how the implemented Phase 0 tasks reshape the next steps (7 minutes)
  - Synthesizes how the seven completed tasks change the project’s readiness for later evaluation, training, and future GPU-backed extensions.
  - MP3: [local file](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.4-implementation-synthesis/dataset-builder-phase-0-improvements-playlist/phase-0-playlist-09_finale_how-phase-0-changes-next-steps.mp3)

## Files
- `playlist.json` — machine-readable playlist manifest and execution recommendation
- `generate_playlist.sh` — batch command to render any missing episode MP3s through the Hermes podcast helper
- `episodes/<episode-slug>/podcast-transcript.json` — canonical transcript JSON
- `episodes/<episode-slug>/podcast-transcript.txt` — rendered transcript text
- `episodes/<episode-slug>/notes.md` — concise production notes

## Generated media outside the repo
- Published show root: [local folder](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-0-orientation/0.4-implementation-synthesis/dataset-builder-phase-0-improvements-playlist)
- Audiobookshelf playlist: `gemma-trajad-eval — Dataset Builder — Phase 0 Improvements task-by-task` · Audiobookshelf UI: https://vps.taild96651.ts.net:13378/

## Notes
- The plan tasks are already implemented and marked done; this playlist is documentation and learning media based on that completed work.
- The intro and finale explicitly concentrate on how these implemented tasks affect the next steps.
