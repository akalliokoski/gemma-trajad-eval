# P1 replace_tool_choice walkthrough learning artifacts

This folder contains the Phase 3.2 walkthrough package for the first perturbation rule in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`.

## Files
- `answers.md` — debrief on how P1 works, what real samples show, and what implementation bug was fixed during the walkthrough
- `p1-sample-comparisons.json` — three real before/after sample comparisons from the normalized corpus
- `analysis.md` — infographic content analysis and layout/style recommendation
- `structured-content.md` — designer-ready content structure for the infographic
- `prompts/infographic.md` — prompt-assembled source of truth for the image-generation workflow
- `infographic.png` — current in-repo infographic artifact generated from the prompt-driven image workflow
- `media-brief.md` — shared brief used to shape media outputs
- `podcast-transcript.json` — canonical two-host transcript with per-turn emotion metadata
- `podcast-transcript.txt` — rendered two-host transcript for the podcast pipeline

## Generated media outside the repo
- Podcast: [local MP3](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-3-perturbation-engine/3.2-rule-walkthroughs/p1-replace-tool-choice-walkthrough/phase-3_3.2-01_p1-replace-tool-choice-walkthrough.mp3) · [Audiobookshelf UI](https://vps.taild96651.ts.net:13378/)

## Notes
- No video explainer was created for this topic.
- This package includes a real implementation fix discovered during the walkthrough: multi-tool assistant messages were being over-mutated because `replace_tool_call()` replaced every `<tool_call>` block instead of only the intended one.
- The infographic is usable as a concept-level visual summary, but text rendering is still not fully clean even after a retry with the newer Ideogram configuration.
