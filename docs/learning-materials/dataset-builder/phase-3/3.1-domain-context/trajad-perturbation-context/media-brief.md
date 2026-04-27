# Media brief: TrajAD perturbation context

Use this brief to generate an infographic and podcast for the combined Phase 3.1 domain-context slice in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`.

## Audience
A technically curious learner who now understands normalization and needs to understand what makes a perturbation dataset realistic before walking through rules one by one.

## Target understanding
By the end, the learner should understand:
1. that TrajAD's `perturb-and-complete` strategy is richer than this repo's direct perturbation because later steps evolve from the error
2. that this repo's direct perturbation approach is simpler and deterministic but can create internal contradictions
3. that the repo's anomaly taxonomy now maps 10 subtypes into the three TrajAD top-level classes
4. that the repo currently implements 9 rules and still leaves `hallucinated_tool` and `unnecessary_replanning` as stubs
5. that Phase 3.2 should judge each rule on both taxonomy fit and realism

## Core facts to preserve
- TrajAD evaluates trajectories for anomaly detection plus first-error localization
- TrajAD's top-level classes are `Task Failure`, `Process Inefficiency`, and `Unwarranted Continuation`
- TrajBench is summarized as a `63,484`-sample balanced dataset across `13` tasks and `5` domains
- this repo currently uses direct perturbation rather than perturb-and-complete
- implemented repo rules: P1 through P9, with `skipped_required_step` covered by both P3 and P8
- stub subtypes: `hallucinated_tool`, `unnecessary_replanning`
- realism risk examples: P6 `contradicted_tool_result`, P7 `premature_final_answer`

## Repo-specific framing
Hammer home these ideas:
- taxonomy quality and generation quality are inseparable
- deterministic local edits are great for inspection but weaker on downstream realism
- Task Failure currently dominates the implemented rule inventory
- the next practical goal is not more abstract theory; it is to inspect each existing perturbation rule with realism in mind

## Suggested podcast angle
Make the episode feel like the bridge between Phase 2 and hands-on rule inspection:
- why understanding the generation strategy matters before reading individual rules
- why a clean taxonomy is not enough if the trajectories still feel mechanically edited
- why the remaining stubs reveal where the current dataset is still thin

## Suggested tone
- technically grounded
- debrief style, not textbook style
- emphasize the most important distinctions repeatedly from slightly different angles

## Source files
- `answers.md`
- `analysis.md`
- `structured-content.md`
- `prompts/infographic.md`
- `podcast-transcript.json`
- `podcast-transcript.txt`
- `infographic.png`
