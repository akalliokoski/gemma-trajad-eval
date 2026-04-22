---
title: "Dataset construction and anomaly taxonomy in TrajAD"
topic: "educational/technical"
data_type: "taxonomy + comparison"
complexity: "moderate"
point_count: 7
source_language: "en"
user_language: "en"
---

## Main Topic
This topic explains how TrajAD defines anomalous trajectories and why dataset quality depends on both the anomaly taxonomy and the method used to generate anomalous traces. It also compares TrajBench's perturb-and-complete pipeline with this repo's simpler direct-perturbation approach.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. the three top-level anomaly classes in TrajAD and the six perturbation families that map onto them
2. how TrajBench's perturb-and-complete pipeline differs from this repo's current 8 perturbation rules and direct perturbation strategy
3. why coherent downstream behavior and high human agreement matter for later `dataset_builder/` manual review and first-error localization work

## Target Audience
- **Knowledge Level**: Beginner-to-intermediate technical learner
- **Context**: Working through the dataset-builder learning plan for the first time
- **Expectations**: Understand the anomaly taxonomy, the generation-method comparison, and the practical implications for this repo

## Content Type Analysis
- **Data Structure**: One taxonomy block, one mapping from classes to perturbation families, one method comparison, and one evidence/quality bar block
- **Key Relationships**: Three anomaly classes group six perturbation families; TrajBench's perturb-and-complete contrasts with this repo's direct perturbation; human agreement rates justify the quality bar for later manual review
- **Visual Opportunities**: Tree-style taxonomy module, class-to-family mapping module, side-by-side method comparison, callout panel for `96.2%` and `94.5%`, and a quick-reference takeaway module for `dataset_builder/`

## Key Data Points (Verbatim)
- "1. Task Failure"
- "2. Process Inefficiency"
- "3. Unwarranted Continuation"
- "TrajBench uses six perturbation families to synthesize anomalous trajectories."
- "- reasoning-error injection"
- "- execution-error injection"
- "- loop insertion"
- "- detour or redundant-subsequence insertion"
- "- failure-to-refuse setup"
- "- redundant-continuation setup"
- "Compared with this repo's current 8 perturbation rules, this project has a slightly broader rule count at the implementation level, but it uses a simpler generation strategy."
- "TrajBench starts from a successful trajectory, injects an anomaly at a chosen step, and then continues the rest of the trajectory from that corrupted state."
- "This repo's current dataset builder uses direct perturbation: it edits a step and leaves later steps unchanged."
- "The paper reports strong human agreement:"
- "- 96.2% agreement for anomaly classification"
- "- 94.5% agreement for first-error localization"
- "The main lesson from TrajAD section 3 is that anomaly quality depends on both taxonomy and generation method."
- "It needs:"
- "- a clear anomaly taxonomy"
- "- perturbations that map cleanly to that taxonomy"
- "- coherent downstream behavior after the first error"
- "- labels that humans can agree on reliably"

## Layout × Style Signals
- Content type: taxonomy + method comparison + evidence summary → suggests `dense-modules`
- Tone: technical, educational, no hype → suggests `pop-laboratory` or `technical-schematic`
- Audience: technically curious learner → suggests a precise but readable technical style
- Complexity: moderate with multiple evidence blocks → suggests a compact modular layout instead of a single tree or single comparison panel

## Design Instructions (from user input)
- Educational and technical for a technically curious learner
- Prefer a layout/style combination that fits taxonomy + generation-method comparison
- `infographic.png` should be the canonical infographic artifact
- The earlier Matplotlib infographic workflow should no longer be treated as the source of truth

## Recommended Combinations
1. **dense-modules + pop-laboratory** (Recommended): Best fit for one infographic that must combine taxonomy, class-to-rule mapping, method comparison, and quality metrics in coordinated technical modules.
2. **comparison-matrix + technical-schematic**: Strong for the TrajBench-versus-this-repo comparison, but weaker for showing the three-class taxonomy cleanly.
3. **tree-branching + pop-laboratory**: Strong for the taxonomy, but weaker for giving enough space to the generation-method and quality-bar comparison.