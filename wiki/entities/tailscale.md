---
title: Tailscale
created: 2026-04-17
updated: 2026-04-17
type: entity
tags: [workflow, integration, local-first, open-source, documentation]
sources: [raw/transcripts/execution-topology-update-2026-04-17.md]
---

# Tailscale

## Overview
Tailscale is the secure connectivity layer between the VPS and the MacBook Pro for this project.

## Why it matters here
Hermes runs on the VPS, while some small/medium compute should run on the Apple Silicon Mac. Tailscale makes that cross-machine coordination practical without assuming public exposure or manual networking work.

## Practical implications
- Hermes should use Tailscale-aware workflows when coordinating remote work.
- Connectivity checks and remote host discovery should happen before trying to use the Mac as a worker.
- Tailscale status is part of the project's execution-topology health.

## Related pages
- [[execution-topology]]
- [[syncthing]]
- [[hermes-agent]]
