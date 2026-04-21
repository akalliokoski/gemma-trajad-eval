---
title: Syncthing
created: 2026-04-17
updated: 2026-04-17
type: entity
tags: [workflow, integration, local-first, open-source, documentation]
sources: [raw/transcripts/execution-topology-update-2026-04-17.md]
---

# Syncthing

## Overview
Syncthing is the intended file-synchronization layer between the VPS and the MacBook Pro.

## Why it matters here
Distributed execution becomes much easier when code, small artifacts, and project materials can move between machines without manual copy steps.

## Practical implications
- Hermes should assume that synchronized project state may matter when work moves from the VPS to the Mac.
- Sync health should be checked before relying on cross-machine artifacts.
- Procedure details for Syncthing-backed workflows should be documented once they stabilize.

## Related pages
- [[execution-topology]]
- [[tailscale]]
- [[hermes-first-development]]
