---
title: "TrajAD perturbation context"
topic: "educational/technical"
data_type: "taxonomy comparison + generation-strategy tradeoff + implementation coverage audit"
complexity: "moderate"
point_count: 7
source_language: "en"
user_language: "en"
---

## Main Topic
This topic explains why Phase 3 starts with generation strategy rather than individual rules: TrajAD's perturb-and-complete approach creates downstream-realistic anomalous traces, while this repo's direct perturbation approach is simpler and easier to inspect but more prone to internal contradictions.

## Learning Objectives
After viewing this infographic, the viewer should understand:
1. that `perturb-and-complete` and `direct perturbation` are different dataset-quality philosophies, not just different implementation details
2. that this repo's 10 anomaly subtypes map into TrajAD's three top-level anomaly classes with uneven coverage
3. that the main Phase 3 risk is realism, especially for rules like P6 and P7 where later steps are not regenerated from the error

## Target Audience
- **Knowledge Level**: Beginner-to-intermediate technical learner
- **Context**: Continuing from normalization into the anomaly-generation stage
- **Expectations**: Understand what to look for before reading perturbation rules one by one

## Content Type Analysis
- **Data Structure**: one framing module, one direct-vs-perturb-and-complete comparison module, one failure-mode module, one taxonomy module, one implementation coverage module, one stub-gap module, and one next-step takeaway module
- **Key Relationships**: generation strategy shapes realism; taxonomy shapes labeling; implementation coverage reveals what failure families the current builder can and cannot represent well
- **Visual Opportunities**: side-by-side pipeline comparison, three-class taxonomy tree, coverage chips by subtype, warning panel for realism risks, and a forward arrow into Phase 3.2

## Key Data Points (Verbatim)
- "63,484"
- "13"
- "5"
- "Task Failure"
- "Process Inefficiency"
- "Unwarranted Continuation"
- "10 anomaly subtypes"
- "9 implemented rules"
- "hallucinated_tool"
- "unnecessary_replanning"
- "P6 contradicted_tool_result"
- "P7 premature_final_answer"
- "perturb-and-complete"
- "direct perturbation"

## Layout × Style Signals
- Content type: comparison plus taxonomy plus coverage audit -> suggests `dense-modules`
- Tone: technical and code-adjacent -> suggests `pop-laboratory`
- Audience: learner entering implementation-level anomaly work -> suggests readable modular diagrams rather than decorative visuals
- Complexity: moderate with multiple connected ideas -> suggests a portrait modular layout

## Design Instructions (from user input)
- Keep the artifact meaningful and emphasize the most important ideas over boilerplate
- Treat `infographic.png` as the canonical generated output
- Make the infographic feel like a debrief about anomaly realism, not a generic paper-summary poster

## Recommended Combinations
1. **dense-modules + pop-laboratory** (Recommended): Best fit for side-by-side generation-strategy comparison, taxonomy tree, coverage chips, and realism warnings.
2. **comparison-matrix + technical-schematic**: Good for strategy tradeoffs, but weaker than `dense-modules` for mixed taxonomy-plus-coverage content.
3. **bento-grid + pop-laboratory**: Usable fallback, but less strong than `dense-modules` for a coherent technical story.
