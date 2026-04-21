---
title: Execution Topology
created: 2026-04-17
updated: 2026-04-17
type: concept
tags: [workflow, decision, documentation, local-first, cloud]
sources: [raw/transcripts/execution-topology-update-2026-04-17.md]
---

# Execution Topology

## Definition
Execution topology is the project rule-set for deciding whether work runs on the VPS, the Apple Silicon MacBook Pro, or later Modal.

## Why it matters in this repo
The project is no longer a single-machine workflow. Hermes runs on the VPS, moderate local compute belongs on the Mac, and future heavy GPU work belongs on Modal.

## Practical implications
- Each substantial task should have an explicit workload-placement decision.
- High-RAM Mac work requires user approval first.
- Cross-machine workflows should account for both connectivity and file synchronization.

## Related pages
- [[tailscale]]
- [[syncthing]]
- [[modal]]
