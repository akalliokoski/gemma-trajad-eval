Create a professional infographic following these specifications:

## Image Specifications
- Type: Infographic
- Layout: dense-modules
- Style: pop-laboratory
- Aspect Ratio: 9:16
- Language: en

## Core Principles
- Follow a dense modular information architecture with 6-7 clearly separated technical modules
- Use the pop-laboratory palette consistently: grayish-white blueprint-grid background, muted teal blocks, fluorescent pink only for warnings/highlights, lemon-yellow marker emphasis, charcoal technical lines
- Keep all text short, large, and highly legible; prefer chips, labels, and short callouts over paragraphs
- No garbled text, no misspellings, no invented statistics
- Make the title and major headings extremely readable
- Treat this like a technical debrief about anomaly realism in an LLM-agent dataset pipeline

## Layout Guidelines
- Use 7 distinct modules with coordinate labels like SEC-01, SEC-02
- Keep the central comparison between perturb-and-complete and direct perturbation visually dominant
- Include a warning module for realism cracks and a coverage grid for taxonomy mapping
- Dense but organized; every module should carry useful information

## Style Guidelines
- Blueprint/lab-manual precision with bold headers and technical annotations
- Fine coordinate lines, arrows, crosshair markers, and small metadata corners
- Strong contrast between large headlines and small technical labels
- Avoid cartoon aesthetics, decorative clutter, or prose-heavy blocks

## Content
Title: TrajAD perturbation context
Subtitle: Why Phase 3 starts with realism, taxonomy, and generation strategy

Module SEC-01 — Why this stage starts here
- anomaly detection
- first-error localization
- rollback-and-retry
- realism gate before P1-P9 walkthrough

Module SEC-02 — Two dataset philosophies
Left side: perturb-and-complete
- inject error at step K
- generate steps K+1..N as if the error were real
- coherent downstream behavior
Right side: direct perturbation
- modify step K
- later steps mostly unchanged
- deterministic local edit

Module SEC-03 — Realism vs simplicity
- 63,484 samples
- 13 tasks
- 5 domains
- perturb-and-complete: stronger downstream realism
- direct perturbation: cheaper, deterministic, easy to test

Module SEC-04 — Where realism cracks show
- P6 contradicted_tool_result
- final answer changes, earlier evidence path stays clean
- P7 premature_final_answer
- fake early conclusion, later behavior not regenerated
- warning label: later steps not regenerated

Module SEC-05 — TrajAD top-level taxonomy
- Task Failure
- Process Inefficiency
- Unwarranted Continuation

Module SEC-06 — Repo coverage by class
Task Failure:
- bad_tool_arguments -> P2
- skipped_required_step -> P3 + P8
- premature_final_answer -> P7
- contradicted_tool_result -> P6
- invalid_tool_json -> P9
- hallucinated_tool -> stub
Process Inefficiency:
- wrong_tool_choice -> P1
- repeated_step -> P4
- unnecessary_replanning -> stub
Unwarranted Continuation:
- continued_after_sufficient_evidence -> P5
Badge stats:
- 10 anomaly subtypes
- 9 implemented rules

Module SEC-07 — What to carry into Phase 3.2
Two questions:
- Is the label right?
- Is the trajectory realistic?
Next arrow:
- next: P1-P9 walkthrough

## Text labels (exact)
- TrajAD perturbation context
- Two dataset philosophies
- perturb-and-complete
- direct perturbation
- Realism vs simplicity
- Where realism cracks show
- Task Failure
- Process Inefficiency
- Unwarranted Continuation
- 63,484 samples
- 13 tasks
- 5 domains
- 10 anomaly subtypes
- 9 implemented rules
- P6 contradicted_tool_result
- P7 premature_final_answer
- hallucinated_tool stub
- unnecessary_replanning stub
- Is the label right?
- Is the trajectory realistic?
- next: P1-P9 walkthrough
