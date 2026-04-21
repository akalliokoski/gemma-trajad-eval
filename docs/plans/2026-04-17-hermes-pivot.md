# Hermes-First Project Pivot Implementation Plan

> For Hermes: use project skills aggressively, keep the same core stack where possible, and treat every implementation task as both project work and course-material production.

**Goal:** Pivot the repository from a narrow trajectory-anomaly experiment into a Hermes-first learn-by-doing project where Hermes performs the engineering work and continuously produces study material.

**Architecture:** Keep the current Gemma/Unsloth/Apple Silicon stack and existing repo structure, but reframe the project around an autonomous Hermes workflow. The repo becomes both an implementation workspace and a living curriculum with AGENTS instructions, wiki maintenance, and generated learning artifacts.

**Tech Stack:** Hermes Agent, Hermes skills/tools, Gemma, Unsloth, Apple Silicon, Python, markdown docs.

---

### Task 1: Document the pivot

**Objective:** Capture the new scope before additional implementation work begins.

**Files:**
- Create: `AGENTS.md`
- Modify: `README.md`
- Create: `docs/plans/2026-04-17-hermes-pivot.md`

**Step 1: Read the current README and repo structure**
Run: inspect repo files and read `README.md`
Expected: clear view of the current anomaly-detection-focused scope.

**Step 2: Define the new scope in writing**
Include:
- Hermes as the primary executor for development, data engineering, and fine-tuning
- Course-material generation as a first-class output
- Active use of project-relevant Hermes skills and creation of new skills when missing
- LLM Wiki maintenance during execution
- Preservation of the existing Gemma/Unsloth/Apple Silicon direction where practical

**Step 3: Create `AGENTS.md`**
Document operational rules for future Hermes work:
- project mission
- non-goals
- default workflow for every task
- wiki maintenance expectations
- course-material artifact expectations
- stack constraints and preferred tools
- definition of done

**Step 4: Rewrite `README.md`**
Update the top-level project narrative so it matches the Hermes-first scope while preserving the important technical threads from the current project.

**Step 5: Verify consistency**
Read both edited files and confirm that scope, workflow, and stack references align.

**Step 6: Commit later when requested**
Do not commit automatically unless the user asks.
