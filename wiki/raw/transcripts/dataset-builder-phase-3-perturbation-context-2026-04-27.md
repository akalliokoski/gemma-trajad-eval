# Raw transcript notes — dataset-builder Phase 3 perturbation context

Date: 2026-04-27
Source type: learning-path debrief / paper-to-implementation comparison

## What was done
- read the Phase 3.1 domain-context tasks from the dataset-builder learning plan
- reviewed the TrajAD paper summary for `perturb-and-complete`, anomaly taxonomy, and process-supervision framing
- inspected `dataset_builder/perturbations.py` to map implemented anomaly subtypes to top-level classes
- created a combined Phase 3.1 learning package with answers, infographic prompt materials, generated PNG, and podcast transcript
- generated a podcast episode and verified Audiobookshelf ingestion
- updated the learning plan to mark both Phase 3.1 checklist items complete

## Main findings
- TrajAD's core generation advantage is `perturb-and-complete`: after an error is injected, later steps are regenerated as if the error were real
- this repo still uses direct perturbation: edit one step locally and usually keep later steps unchanged
- direct perturbation is deterministic, cheap, and easy to inspect, but weaker on downstream realism
- the clearest realism-risk examples in the current rule set are:
  - P6 `contradicted_tool_result`
  - P7 `premature_final_answer`
- the repo currently maps `10` anomaly subtypes into the three TrajAD top-level classes:
  - `Task Failure`
  - `Process Inefficiency`
  - `Unwarranted Continuation`
- the repo now has `9` implemented perturbation rules because P9 `invalid_tool_json` exists
- the remaining stub anomaly subtypes are:
  - `hallucinated_tool`
  - `unnecessary_replanning`
- Task Failure currently has the strongest implementation coverage; continuation and replanning remain thinner

## Important interpretation
Taxonomy and generation strategy are inseparable. A good anomaly dataset is not just a list of perturbation labels; it also needs believable downstream consequences after the first error.

## Artifact package
- `docs/learning-materials/dataset-builder/phase-3/3.1-domain-context/trajad-perturbation-context/README.md`
- `docs/learning-materials/dataset-builder/phase-3/3.1-domain-context/trajad-perturbation-context/answers.md`
- `docs/learning-materials/dataset-builder/phase-3/3.1-domain-context/trajad-perturbation-context/infographic.png`
- `/data/audiobookshelf/podcasts/profiles/gemma/projects/gemma-trajad-eval/dataset-builder/phase-3-perturbation-engine/3.1-domain-context/trajad-perturbation-context/phase-3_3.1-01_trajad-perturbation-context.mp3`
