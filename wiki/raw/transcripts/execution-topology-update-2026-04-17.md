# Execution topology update

Date: 2026-04-17
Source type: internal project notes

New operating constraints and preferences:
- Hermes is currently running on the VPS.
- The Apple Silicon MacBook Pro (M3 Pro, 32 GB RAM) should be used for small and medium heavy-lifting.
- The VPS and the Mac are connected via Tailscale, and Syncthing is used for file synchronization.
- Hermes should actively use these tools and related workflows to distribute work between the VPS and the Mac.
- The Mac is also a day-to-day human workstation, so any high-RAM task sent to the Mac requires explicit user approval first.
- The actual heavy-lifting tier should eventually use Modal serverless GPUs.
- Modal account setup is intentionally deferred until the project reaches the right stage.
