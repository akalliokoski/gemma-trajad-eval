# Structured content — P4 duplicate_tool_step infographic

Title:
- P4 duplicate_tool_step walkthrough

Subtitle:
- Repeated-step anomalies are strongest when one repeated step really means one step

Panel 1 — Rule shape
- Header: What P4 does
- Chips:
  - Duplicate assistant+tool pair
  - Insert immediately after original
  - Exact byte copy
- Mini flow:
  - original pair at i
  - duplicate starts at i+2
  - `bad_step = i+2`

Panel 2 — Why bad_step points to the duplicate
- Header: First wrong step
- Short points:
  - original pair is still correct
  - anomaly begins at repeated copy
  - validator expects duplicate start
- Badge:
  - `bad_step -> duplicate assistant`

Panel 3 — Real corpus evidence
- Header: What the corpus showed
- Big metrics:
  - `3679` eligible records
  - `5` min source length
  - `53191` eligible pairs
  - `17.4%` compound pairs
- Secondary chips:
  - `1753` only simple
  - `1850` mixed
  - `76` only compound

Panel 4 — Walkthrough finding and fix
- Header: Realism issue
- Left card:
  - old policy: random eligible pair
  - risk: duplicate a compound multi-call bundle
- Right card:
  - new policy: prefer 1 call + 1 response
  - fallback: any pair if no simple option
- Footer chip:
  - narrower anomaly, same determinism

Panel 5 — Verification
- Header: How it was checked
- Badges:
  - exact-content test passed
  - simple-pair preference test passed
  - perturbations suite `16 passed`
  - coherence + validator `2 passed`
- Closing takeaway:
  - Prefer the narrowest plausible repeated step

Design notes:
- dark background
- large clean type
- cyan/lime/orange accent chips
- arrows between before and after cards
- no paragraphs
- perfect spelling
