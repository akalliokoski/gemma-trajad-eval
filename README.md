# gemma-trajad-eval

Hermes-first applied LLM engineering on Gemma, Unsloth, and Apple Silicon.

This repository is a learn-by-doing project where Nous Research Hermes Agent does the hands-on work across development, data engineering, fine-tuning, evaluation, and documentation. The project keeps the original Gemma-based trajectory-anomaly direction as an important technical track, but the broader scope is now bigger: build with Hermes, and turn the build process itself into reusable course material.

---

## Project pivot

The repository started as a focused project for trajectory anomaly detection on Hermes-style agent traces.

That thread still matters, but the scope has changed:
- Hermes is now the primary executor for project work
- the repo should actively use Hermes skills, tools, and newly created skills
- the project should maintain a living wiki while work is happening
- every substantial implementation step should also produce study material for the human learner
- the same core stack should be preserved where practical: Gemma, Unsloth, and Apple Silicon

In short: this is now a Hermes-first build-and-learn lab.

---

## What this repo is for now

This repo serves four purposes at once:

1. Development workspace
   - Build real code, scripts, datasets, and experiments with Hermes doing the execution.

2. Data engineering lab
   - Ingest, inspect, normalize, label, mutate, and validate agent-trace data.

3. Fine-tuning and evaluation lab
   - Prepare training data, run Gemma experiments, and evaluate outputs with local-first constraints.

4. Course-material factory
   - Capture project knowledge as explainers, plans, runbooks, and wiki pages so the human can study both concepts and actual implementation steps.

---

## Core operating model

For meaningful work in this repository, Hermes should:
- load and use relevant skills first
- inspect existing code and docs before changing anything
- create plans for multi-step work in `docs/plans/`
- execute tasks with tools, scripts, and verification
- update documentation as part of implementation
- maintain a project knowledge base with the `llm-wiki` skill
- create or patch reusable skills when project-specific workflows emerge

The intent is not just to finish tasks, but to leave behind a high-signal record of what was learned and how the work was done.

---

## Current technical direction

The preferred technical direction remains:
- model family: Gemma
- tuning workflow: Unsloth where possible
- control/orchestration plane: VPS-hosted Hermes Agent
- local worker target: Apple Silicon MacBook Pro
- network coordination: Tailscale
- file synchronization: Syncthing
- implementation language: Python
- repo-native documentation: Markdown
- heavy GPU tier: Modal later, once the project is ready and account setup is done

When local constraints require alternatives, use the closest compatible path that still preserves the spirit of the stack.

### Execution topology and workload placement

The project now uses a three-tier execution model:

1. VPS
   - Hermes runs here by default.
   - Use it for orchestration, planning, docs, repo management, lightweight automation, and remote coordination.

2. Apple Silicon MacBook Pro (M3 Pro, 32 GB)
   - Use it for small and medium heavy-lifting, Apple-Silicon-specific validation, bounded local training runs, and local data processing.
   - Because this is also the user's daily workstation, high-RAM tasks require explicit user approval before dispatch.

3. Modal serverless GPU
   - Intended future home for truly heavy compute.
   - Account setup is intentionally deferred until the project reaches the right stage.

Hermes should actively use Tailscale and Syncthing-aware workflows to coordinate work between the VPS and the Mac instead of assuming all work happens on one machine.

---

## Active workstreams

### 1. Hermes-first project infrastructure
- project operating rules in `AGENTS.md`
- implementation plans in `docs/plans/`
- reusable Hermes skills
- project wiki and study materials

### 2. Agent-trace data engineering
- download and inspect source traces
- normalize trajectory formats
- define anomaly taxonomies and labels
- generate perturbations and validation checks
- build train/eval-ready datasets

### 3. Gemma fine-tuning and evaluation
- format SFT-ready examples
- run local-first experiments
- compare prompt and model variants
- choose the right execution tier for each experiment
- measure output quality, localization quality, and structured-output reliability

### 4. Integrations and demos
- connect outputs to observability or tracing workflows
- build demos around trace inspection and anomaly analysis
- create practical examples that can be studied and reproduced

---

## Repo layout

Current top-level areas:

```text
gemma-trajad-eval/
  AGENTS.md
  README.md
  LICENSE
  pyproject.toml

  dataset_builder/
  training/
  integrations/
  prompts/
  docs/

  wiki/                      # Project LLM Wiki (to be created and maintained by Hermes)
  outputs/                   # Generated adapters, reports, artifacts
```

Important docs:
- `AGENTS.md` — project operating instructions for Hermes and future agents
- `docs/execution-topology.md` — workload placement rules across VPS, Mac, and future Modal
- `docs/project-spec.md` — prior project specification and source context
- `docs/labeling-guidelines.md` — anomaly labeling rules and examples
- `docs/evaluation-plan.md` — metrics and evaluation protocol
- `docs/plans/` — implementation plans for ongoing work

---

## Project wiki

This project should maintain a repository-local wiki under `wiki/` using the `llm-wiki` skill.

The wiki should capture:
- important concepts and terminology
- models, datasets, tools, and libraries
- experiment decisions and tradeoffs
- durable answers to recurring project questions
- raw sources that informed implementation choices

The goal is a compounding project memory that survives beyond chat history and doubles as study material.

---

## Learn-by-doing output standard

Substantial work should leave behind material that a human can study later.

Good outputs include:
- short technical explainers
- implementation notes
- experiment summaries
- troubleshooting guides
- architecture notes
- example commands and verification steps
- wiki pages for concepts and decisions

A useful artifact should answer:
- what was done
- why it was done this way
- how it was implemented
- how it was validated
- what to study next

---

## Original trajectory-anomaly track

The original focus remains a valid and important execution track inside the broader project.

That track includes:
- converting Hermes-style traces into supervised trajectory-eval datasets
- generating anomaly labels and localized bad-step annotations
- fine-tuning Gemma to judge trajectory quality
- evaluating binary anomaly detection, anomaly typing, and step localization

Existing scripts under `dataset_builder/`, `training/`, `prompts/`, and `integrations/` remain relevant and should be evolved rather than discarded whenever possible.

---

## Suggested next steps

1. Initialize the project wiki in `wiki/`
2. Keep execution-topology docs aligned with reality
3. Pick the next concrete implementation slice
4. Decide whether it belongs on the VPS, the Mac, or later Modal
5. Execute it with Hermes while producing course material in parallel

---

## License

MIT — see `LICENSE`.
