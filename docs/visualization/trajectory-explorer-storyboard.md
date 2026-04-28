# Trajectory Explorer Storyboard

## Scene 1: Hero / framing

Purpose:
- Explain that this is a Hermes-first trajectory anomaly lab and point readers to the TurboQuant-inspired reference style.

Key content:
- project title
- short tagline
- top-level counts
- reference visualization link

## Scene 2: Project pipeline overview

Purpose:
- Show the repo as a pipeline from source traces to dataset artifacts, SFT formatting, fine-tuning, and evaluation.

Key content:
- sources
- dataset builder
- processed artifacts
- SFT prep
- training
- evaluation

## Scene 3: Trajectory explorer

Purpose:
- Let the reader switch between one normal and one anomalous sample and inspect where the anomaly occurs.

Key content:
- sample selector
- message timeline canvas
- `bad_step` highlight
- per-step detail panel
- source-pair comparison summary for anomalous sample when available

## Scene 4: Dataset summary

Purpose:
- Show that the interactive examples sit inside a larger processed dataset with explicit perturbation rules and label distributions.

Key content:
- raw trace count
- processed example count
- split counts
- anomaly class/type counts
- perturbation rule coverage

## Scene 5: Fine-tuning lifecycle

Purpose:
- Make the later project stage concrete even before heavy training runs are committed.

Key content:
- prepare_sft_data -> train_e2b -> evaluate flow
- task modes: binary, localize, joint
- artifact locations
- note that RL/GRPO is later

## Scene 6: Evaluation status

Purpose:
- Explain what can be visualized now versus what depends on future evaluation-report artifacts.

Key content:
- dataset-backed evaluation context
- perturbation diagnostics
- note about missing committed run reports
