# Wiki Schema

## Domain
Hermes-first applied LLM engineering in this repository: autonomous development workflows, data engineering, Gemma fine-tuning, evaluation, Apple Silicon constraints, and project-generated study material.

## Conventions
- File names: lowercase, hyphens, no spaces.
- Every wiki page starts with YAML frontmatter.
- Use `[[wikilinks]]` between pages; every wiki page should include at least 2 outbound links where practical.
- When updating a page, always bump the `updated` date.
- Every new wiki page must be added to `index.md`.
- Every create, ingest, query, lint, archive, or major update action must be appended to `log.md`.
- Raw sources in `raw/` are immutable snapshots; corrections belong in wiki pages, not the raw files.
- Prefer concise, scannable pages. Split any page that grows beyond ~200 lines.

## Frontmatter
```yaml
---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/transcripts/example.md]
---
```

## Tag Taxonomy
Models and systems:
- model
- agent
- training
- evaluation
- inference
- data

Project operations:
- workflow
- roadmap
- documentation
- course-material
- decision
- experiment

Hardware and tooling:
- apple-silicon
- local-first
- cloud
- python
- open-source

Domain themes:
- fine-tuning
- trajectory-analysis
- observability
- integration
- dataset

Rule: every tag used on a page must appear in this taxonomy first.

## Page Thresholds
- Create a page when a concept or entity is central to the project or appears repeatedly.
- Add to an existing page when new work extends something already covered.
- Do not create pages for passing mentions or temporary execution details.
- Split a page when it becomes too large to scan quickly.
- Archive a page only when it is clearly superseded by a better structured replacement.

## Entity Pages
One page per notable tool, model, dataset, or system. Include:
- What it is
- Why it matters here
- Key constraints or affordances
- Links to related concepts and entities

## Concept Pages
One page per reusable project concept. Include:
- Definition
- Why it matters in this repo
- Practical implications
- Related concepts and entities

## Comparison Pages
Use comparison pages for tradeoffs such as local vs cloud training, Gemma variants, or tooling choices. Prefer tables for dimensions and a short verdict section.

## Query Pages
Use query pages only for durable answers that would be annoying to re-derive, such as a recurring setup decision or a frequently referenced technical conclusion.

## Update Policy
When new information conflicts with existing content:
1. Check which source is newer.
2. Note both claims with dates and source paths when the conflict is real.
3. Add a `contradictions:` frontmatter field if the disagreement needs later review.
4. Flag unresolved conflicts in the next lint report.
