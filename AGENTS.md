# AGENTS.md

Project: gemma-trajad-eval
Status: Hermes-first learn-by-doing lab

## Mission

Use Nous Research Hermes Agent as the primary operator for this project.

Hermes should do the actual work across:
- software development
- data engineering
- experiment design
- fine-tuning and evaluation
- documentation and project operations

At the same time, Hermes should turn the work into study material so the human can learn by reading what was built, why it was built, and how it was verified.

## Core project idea

This repo is no longer only a narrow trajectory-anomaly-detection experiment.
It is now a Hermes-first applied LLM engineering project that still keeps the same core technical direction where possible:
- Gemma models
- Unsloth-based fine-tuning where appropriate
- Apple Silicon as the main local development environment

The current trajectory-anomaly work remains a valid initial track, but it should now be developed as one module inside the broader Hermes-driven workflow.

## Primary operating principles

1. Hermes does the doing.
   - Prefer real tool use, scripts, experiments, and code changes over speculative planning.
   - Use Hermes tools and skills aggressively before falling back to generic reasoning.

2. Every task teaches.
   - Each substantial task should leave behind human-readable learning artifacts.
   - Favor docs that explain both concepts and concrete hands-on actions.

3. Preserve the stack when reasonable.
   - Keep Gemma, Unsloth, and Apple Silicon compatibility as defaults.
   - Only introduce new infrastructure when it materially improves execution.

4. Respect the execution topology.
   - Hermes runs on the VPS by default and should treat the VPS as the orchestration/control plane.
   - The Apple Silicon MacBook Pro is the preferred worker for small and medium heavy-lifting.
   - Use Tailscale for secure host-to-host access and Syncthing for file synchronization when coordinating work between the VPS and the Mac.
   - Do not send high-RAM jobs to the Mac without explicit user approval first.
   - Reserve true heavy GPU lifting for Modal once account setup is intentionally done later.

5. Build reusable Hermes workflows.
   - Reuse existing skills whenever relevant.
   - Create or patch skills when project-specific procedures become repeatable.

6. Maintain a project wiki as work happens.
   - Use the `llm-wiki` skill to keep a living knowledge base for the project.
   - The wiki should accumulate project concepts, decisions, references, experiments, and lessons learned.

## Default workflow for any meaningful task

For any task that is more than a tiny edit, Hermes should:

1. Read current context before acting.
   - inspect relevant files
   - inspect existing docs or plans
   - load relevant Hermes skills first

2. Make the smallest useful plan.
   - create or update a task plan in `docs/plans/` when the work is multi-step
   - prefer bite-sized tasks with explicit verification

3. Execute with tools.
   - write code, run scripts, inspect outputs, and verify results
   - avoid describing actions without taking them
   - decide deliberately whether execution belongs on the VPS, the Mac, or later Modal

4. Produce learning artifacts alongside implementation.
   - update docs in `docs/`
   - create short explainers, runbooks, or tutorials when useful
   - make the work understandable to a human studying the repo afterward

5. Update the project wiki.
   - use the `llm-wiki` skill to record notable concepts, workflows, sources, experiments, and decisions
   - avoid letting knowledge live only in chat history

6. Capture reusable procedure knowledge.
   - if a non-trivial workflow worked, save or update a Hermes skill

7. Respect approval gates.
   - ask for explicit approval before starting any high-RAM task on the MacBook Pro
   - low-impact inspection, sync, and setup tasks on the Mac are fine without a special approval step

## Expected learning outputs

When Hermes completes substantial work, it should try to leave behind one or more of:
- implementation notes
- mini tutorials
- architecture notes
- experiment logs
- glossary or concept pages
- troubleshooting notes
- reproducible command examples

Good course material explains:
- what problem was solved
- why this approach was chosen
- what files changed
- what commands were run
- how success was verified
- what to study next

## Wiki policy

Preferred project wiki location: `wiki/` at the repository root.

The wiki should be used for:
- concepts: fine-tuning, evals, data pipelines, Gemma, Unsloth, Apple Silicon constraints
- entities: models, datasets, tools, libraries, services
- comparisons: training approaches, local vs cloud tradeoffs, model variants
- queries: durable answers worth keeping
- raw sources: copied or extracted source material used during the project

When starting a wiki session, Hermes should orient itself first:
- read `wiki/SCHEMA.md`
- read `wiki/index.md`
- scan recent entries in `wiki/log.md`

If the wiki does not yet exist and the current task benefits from it, initialize it with the `llm-wiki` skill.

## Preferred stack

Keep these as defaults unless there is a strong reason to deviate:
- language: Python
- model family: Gemma
- control plane: VPS-hosted Hermes Agent
- local worker: Apple Silicon MacBook Pro (M3 Pro, 32 GB RAM)
- secure connectivity: Tailscale
- file sync: Syncthing
- fine-tuning path: Unsloth where feasible, with Apple-Silicon-compatible local alternatives when needed
- heavy GPU path: Modal serverless GPU later, after explicit setup
- data work: local Python scripts, notebooks only when they add clear value
- docs: markdown in-repo

## Execution topology

- VPS: orchestration, documentation, lightweight automation, planning, repo management, and remote coordination
- MacBook Pro: small/medium training runs, data processing, local model experimentation, Apple-Silicon-specific validation
- Modal: future heavy GPU tier for jobs that are too large or disruptive for the Mac

When choosing where a task runs, prefer:
1. VPS for light coordination and documentation work
2. Mac for bounded small/medium compute that fits normal workstation use
3. Modal for real heavy lifting once the project is ready and account setup is complete

Never assume the Mac is freely available for disruptive workloads; obtain user approval for high-RAM use first.

## Current strategic tracks

1. Hermes-first project infrastructure
   - AGENTS rules
   - planning docs
   - reusable skills
   - project wiki
   - learning materials

2. Data engineering
   - source trace ingestion
   - normalization
   - labeling and perturbation pipelines
   - eval dataset curation

3. Fine-tuning and evaluation
   - prompt formatting
   - SFT datasets
   - Gemma experiments
   - Unsloth training workflows
   - local and cloud evaluation
   - Mac-vs-Modal workload placement

4. Integrations and demos
   - observability integrations
   - agent trace inspection
   - practical demos of model outputs

## Definition of done for a task

A task is not done until:
- the requested implementation or document exists
- the result was verified with the appropriate tool, test, or inspection step
- the README or docs were updated if the behavior or scope changed
- relevant project knowledge was captured in the wiki or docs
- a reusable workflow was turned into a skill if warranted

## Non-goals

Unless explicitly requested, do not:
- optimize prematurely for large-scale cloud infrastructure
- introduce unnecessary frameworks
- replace the Gemma/Unsloth/Apple Silicon direction without a strong reason
- treat documentation as optional
- leave important reasoning only in transient chat messages

## Immediate next-step guidance

When continuing from this point, prioritize:
1. update docs and wiki whenever execution-topology assumptions change
2. choose the next concrete implementation slice
3. decide whether it belongs on the VPS, the Mac, or later Modal
4. execute it with Hermes while generating course material in parallel
