# Execution Topology

This project uses a three-tier execution model.

## 1. VPS = control plane

Hermes is running on the VPS.

Use the VPS for:
- planning
- documentation
- repository management
- wiki maintenance
- lightweight automation
- remote coordination
- preparing work that will later run elsewhere

Current observed Tailscale details from the VPS:
- VPS hostname: `vps`
- VPS tailnet DNS: `vps.taild96651.ts.net`
- VPS Tailscale IPv4: `100.121.250.82`
- Mac hostname on tailnet: `Codeo’s MacBook Pro`
- Mac tailnet DNS: `codeos-macbook-pro.taild96651.ts.net`
- Mac Tailscale IPv4: `100.92.96.112`

## 2. MacBook Pro = small/medium worker

Primary local worker:
- Apple Silicon MacBook Pro
- M3 Pro
- 32 GB RAM

Use the Mac for:
- small and medium data-processing tasks
- Apple-Silicon-specific validation
- local Gemma experiments that fit workstation constraints
- bounded fine-tuning or inference work that should not require dedicated GPUs

Constraint:
- this is also the user's daily workstation
- high-RAM jobs must be explicitly approved by the user before dispatch

Default rule:
- if a task might noticeably disrupt normal workstation use, pause and ask first

## 3. Modal = future heavy-compute tier

Use Modal later for:
- large training runs
- GPU-heavy batch inference
- jobs that would be too slow or too disruptive on the Mac
- elastic or serverless GPU workloads

Current status:
- Modal is the intended heavy-lifting tier
- account setup is intentionally deferred for now
- do not start Modal setup until the project actually needs it

## Coordination tools

### Tailscale
Use Tailscale for:
- secure access from VPS to Mac
- remote command and service access
- host discovery and connectivity checks
- future remote orchestration workflows

Status observed from the VPS on 2026-04-17:
- `tailscale` CLI present on VPS: yes
- Tailscale backend state: `Running`
- Mac peer visible and online: yes

Note:
- Tailscale SSH is enabled on the VPS, but current access controls do not yet allow anyone to access this device via Tailscale SSH according to `tailscale status --json`

### Syncthing
Use Syncthing for:
- keeping project files synchronized between VPS and Mac
- reducing manual copy steps for artifacts and data slices
- supporting distributed execution without assuming the same filesystem

Current status from this VPS session:
- `syncthing` CLI was not found in the VPS PATH
- this does not prove Syncthing is unavailable overall; it only means the CLI is not currently available in this shell environment

## Workload placement rules

Prefer this order when deciding where work should run:

1. VPS
   - if the task is documentation-heavy, planning-heavy, lightweight, or coordination-heavy

2. MacBook Pro
   - if the task needs Apple Silicon, moderate local compute, or local model validation
   - only if it is unlikely to cause disruptive RAM pressure

3. Modal
   - if the task is truly heavy and the project is ready for cloud GPU setup

## Approval gate for Mac dispatch

Ask the user before dispatching any task to the Mac when it is likely to involve:
- high RAM use
- long-running CPU/GPU pressure
- large local downloads
- persistent resource contention during normal work hours

No special approval is required for:
- light inspection tasks
- connectivity checks
- sync checks
- modest setup steps
- other obviously low-impact actions

## Practical implications for Hermes

Before meaningful execution work, Hermes should decide:
- does this stay on the VPS?
- should this go to the Mac?
- is this actually a future Modal task instead?

For each substantial implementation slice, the resulting docs should record:
- chosen execution tier
- why that tier was chosen
- any approval gate involved
- any sync or coordination assumptions
