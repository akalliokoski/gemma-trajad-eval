# P1 realism and NEARBY_TOOLS coverage improvement

This folder contains the Phase 3.3 follow-up package for improving the realism of P1 `replace_tool_choice` after the earlier walkthrough exposed the `_v2` fallback weakness.

## Files
- `answers.md` — explanation of the design change, why `_v2` was removed, and what the corpus-level comparison showed
- `p1-realism-coverage-comparison.json` — before/after diagnostics summary on `data/interim/hermes_normalized_phase2.jsonl`
- `analysis.md` — infographic content analysis and recommendation
- `structured-content.md` — structured infographic source material
- `prompts/infographic.md` — prompt source of truth for PNG generation
- `infographic.png` — current infographic artifact for this improvement slice
- `media-brief.md` — media brief for the package
- `podcast-transcript.json` — canonical two-host transcript for the podcast pipeline
- `podcast-transcript.txt` — rendered transcript text

## Generated media outside the repo
- Podcast: [local MP3](file:///data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-3-perturbation-engine/3.3-perturbation-diagnostics/p1-realism-and-nearby-tools-coverage/phase-3_3.3-01_p1-realism-and-nearby-tools-coverage.mp3) · [Audiobookshelf UI](https://vps.taild96651.ts.net:13378/)

## Notes
- This slice chooses realism over raw perturbation yield: unmapped tools are skipped instead of being mutated into fake `_v2` names.
- `search_files` and `terminal` now use curated replacements with argument adaptation, so the resulting wrong calls look more like believable tool confusion and less like broken API names.
- Remaining unmapped tools are now visible as explicit coverage gaps rather than hidden behind synthetic suffixes.
- The infographic is acceptable as a concept-level summary, but the second-pass PNG still contains some text corruption and should not be treated as polished final typography.
