---
title: "Dataset-builder implementation improvements after Phase 0"
topic: "technical implementation synthesis"
data_type: "prioritized roadmap + design principles + code-change map"
complexity: "high"
point_count: 8
source_language: "en"
user_language: "en"
---

## Main Topic
This topic distills the Phase 0 learning materials into a practical implementation roadmap for `dataset_builder/`. It explains what should stay simple, what should improve first, and why the right next step is higher data-quality discipline rather than more infrastructure.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. which parts of the current `dataset_builder/` architecture are already good enough to keep
2. why the main quality gap is coherence and validation rather than missing infrastructure
3. which concrete improvements should come first and how they map to specific files
4. why Modal serverless GPU is now the default future GPU path while Apple Silicon becomes secondary

## Target Audience
- **Knowledge Level**: Beginner-to-intermediate technical learner
- **Context**: Building a first home AI lab project and studying the dataset-builder codebase
- **Expectations**: Wants a clean implementation roadmap with reasons, not just a list of tweaks

## Content Type Analysis
- **Data Structure**: one design-position block, one keep-vs-change block, one priority roadmap, one compute-policy block, and one best-practices block
- **Key Relationships**: Phase 0 findings -> implementation gaps -> concrete tasks -> safer future evolution
- **Visual Opportunities**: architecture-stays/simple panel, top-priority improvements ladder, code-file map, compute policy module, and best-practice principles strip

## Key Data Points (Verbatim)
- "keep the current script-first pipeline"
- "data quality discipline"
- "raw-schema-safe inspection"
- "lightweight coherence screening"
- "explicit anomaly classes"
- "rule-aware localization validation"
- "build manifests and perturbation diagnostics"
- "Modal serverless GPU is now the default future GPU tier"
- "Apple Silicon is secondary"
- "practical, elegant, and understandable"

## Layout × Style Signals
- Content type: roadmap + implementation guidance + priorities -> suggests `dense-modules`
- Tone: technical, practical, best-practice oriented -> suggests `pop-laboratory`
- Audience: technically curious learner -> precise but approachable technical style
- Complexity: high but modular -> favors information-dense visual blocks over a linear process illustration

## Design Instructions (from user input)
- Create a detailed plan with background information about the choices and changes
- Explain best practices and the why behind the roadmap
- Treat Modal serverless GPU as the default GPU usage option
- Treat Apple Silicon as the secondary option
- Generate an infographic and podcast from the plan and analysis
- Keep the output practical, elegant, and simple rather than over-engineered

## Recommended Combinations
1. **dense-modules + pop-laboratory** (Recommended): Best fit for a technical synthesis with priority blocks, file-level changes, principles, and compute-policy callouts.
2. **dashboard + technical-schematic**: Good for metrics-like priorities, but weaker for the explanatory tradeoff framing.
3. **bridge + pop-laboratory**: Good for current-state vs improved-state storytelling, but weaker for showing the full implementation roadmap.
