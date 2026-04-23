# Dataset Builder Phase-0 Single-Task Execution Guide

Date: 2026-04-23
Repo: `/home/hermes/gemma-trajad-eval`
Plan: `docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md`

## Purpose
Use this guide when implementing exactly one task from the Phase-0 dataset-builder improvement plan.

## Core rule
A task is only complete when all of these are done:
1. implementation finished
2. verification commands passed
3. infographic PNG created
4. plan file updated with status, date, verification, and infographic path
5. wiki updated
6. commit created
7. push completed

## Orientation checklist
Before touching code:
- read `AGENTS.md`
- read the target task section in `docs/plans/2026-04-22-dataset-builder-phase-0-improvements.md`
- read `wiki/SCHEMA.md`
- read `wiki/index.md`
- scan recent `wiki/log.md`
- run `git status --short --branch`

## Execution mode guidance
For this repo and these tasks, default to direct local execution on the VPS.

Use delegation only if the work naturally decomposes into a narrow independent subtask with clear inputs/outputs. Do not delegate small code/test loops on this VPS.

## Single-task loop
1. identify the exact task and objective
2. inspect only the files needed for that task
3. write or update focused tests first when practical
4. implement the smallest useful code change
5. run the task's targeted verification commands
6. run the broader build/validation command if the task requires it
7. create/update the infographic PNG artifact in `infographic/task-*/`
8. update the plan task block
9. update the wiki with a raw execution note and a durable query page when warranted
10. commit with a task-specific message
11. push

## Repo-specific expectations
- Prefer elegant, bounded changes over framework expansion.
- Preserve script-first Python + JSONL design.
- Keep Apple Silicon out of scope unless the user explicitly approves high-RAM work.
- If a task needs media artifacts, PNG is required; do not substitute SVG/manual fallbacks.

## Typical verification pattern
- targeted pytest for changed behavior
- dataset builder command if the task affects dataset generation
- strict label validation if labels or build output changed

## Suggested status update format in the plan
- `**Status:** Done (YYYY-MM-DD)`
- `**Verification:** <exact commands>`
- `**Implementation infographic:** <path>`

## Output expectations for the task report
Include:
- task completed
- execution mode chosen and why
- files changed
- verification commands run
- infographic path
- wiki files updated
- commit hash
- push result
