# Gemma-TrajAD

**Local trajectory anomaly detection for tool-using agents with Gemma 4 E2B**

A research/dev project that converts Hermes-style agent traces into a TrajAD-inspired supervised dataset and fine-tunes Gemma 4 E2B-it to detect trajectory anomalies, localize bad steps, and classify anomaly types — all runnable locally on Apple Silicon.

---

## Overview

This project consists of two tightly connected subprojects:

- **Subproject A — Dataset:** Hermes traces → TrajAD-style supervised dataset
- **Subproject B — Model:** Gemma 4 E2B trajectory anomaly detector + step localizer

The split is intentional: TrajAD's core setup requires labeled trajectories with anomaly types and localized bad steps, while Hermes-style traces already provide rich multi-turn reasoning, tool calls, and tool responses in a compatible conversational structure.

---

## Hardware target

- **Apple Silicon M3, 32 GB unified memory**
- Local prototyping: MLX / mlx-tune
- Cloud scaling: Unsloth on NVIDIA GPU (A100/H100)

---

## Subproject A — Dataset pipeline

### Input

| Source | Description |
|--------|-------------|
| [`DJLougen/hermes-agent-traces-filtered`](https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered) | ~3,679 rows, multi-turn, ShareGPT-compatible, filtered for reasoning depth |
| [`lambda/hermes-agent-reasoning-traces`](https://huggingface.co/datasets/lambda/hermes-agent-reasoning-traces) | Larger, noisier original source (optional) |

### Output tasks

1. **Binary anomaly detection** — `{"anomalous": true}`
2. **Step localization** — `{"bad_step": 5}`
3. **Typed anomaly classification** — `{"anomaly_type": "process_inefficiency"}`
4. **Joint output** — all of the above plus an explanation string

### Anomaly taxonomy

Top-level classes:

| Class | Description |
|-------|-------------|
| `normal` | Valid expert trajectory |
| `task_failure` | Agent failed to complete the task |
| `process_inefficiency` | Task completed but via a suboptimal path |
| `unwarranted_continuation` | Agent continued after task was effectively solved |

Operational subtypes:

`wrong_tool_choice`, `bad_tool_arguments`, `skipped_required_step`, `repeated_step`, `premature_final_answer`, `continued_after_sufficient_evidence`, `contradicted_tool_result`, `hallucinated_tool`, `invalid_tool_json`, `unnecessary_replanning`

### Dataset record format

```json
{
  "id": "trace_000123_var_02",
  "source_trace_id": "uuid",
  "split": "train",
  "trajectory": [
    {"role": "system",    "content": "..."},
    {"role": "user",      "content": "..."},
    {"role": "assistant", "content": "<think>...</think><tool_call>...</tool_call>"},
    {"role": "tool",      "content": "<tool_response>...</tool_response>"}
  ],
  "is_anomalous": true,
  "anomaly_type": "bad_tool_arguments",
  "bad_step": 4,
  "generation_rule": "mutate_argument_value",
  "metadata": {
    "category": "Terminal & Coding",
    "subcategory": "Terminal Tasks"
  }
}
```

### Generation pipeline stages

| Stage | Description |
|-------|-------------|
| A1 | Clean "normal" set from filtered Hermes traces |
| A2 | Synthetic perturbations (8 perturbation rules) |
| A3 | Automatic labeling with source/variant metadata |
| A4 | Manual review of 100–200 samples |

---

## Subproject B — Model

### Model

| Model | HF ID | Notes |
|-------|-------|-------|
| Primary | [`google/gemma-4-E2B-it`](https://huggingface.co/google/gemma-4-E2B-it) | Lower memory, fast local iteration |
| Optional | `google/gemma-4-E4B-it` | Comparison target |

### Training objective

SFT for structured judging output.

**Prompt:** system instruction (anomaly detector) + full trajectory + task description  
**Target:**
```json
{
  "anomalous": true,
  "bad_step": 5,
  "anomaly_type": "skipped_required_step",
  "confidence": 0.81,
  "explanation": "The agent answered before checking the required file contents."
}
```

### Training ladder

| Stage | Environment | Method | Objective |
|-------|-------------|--------|-----------|
| 1 | Mac / mlx-tune | LoRA SFT | Binary anomaly detection + localization |
| 2 | Mac / mlx-tune | DPO | Ranking between competing judgments |
| 3 | Cloud / Unsloth | LoRA SFT | E4B or 31B, larger batches |
| 4 | Cloud / Unsloth | GRPO | Reward-driven detection + localization |

### Metrics

- Binary anomaly classification accuracy
- Macro F1 for anomaly type
- Exact-match bad-step accuracy
- ±1 tolerance localization accuracy
- JSON validity rate
- Calibration / confidence sanity checks
- Inference latency on local Mac

### MVP success criteria

| Level | Criteria |
|-------|---------|
| Good MVP | Binary detection > base model; localization useful on obvious perturbations; JSON validity > 95% |
| Strong result | Useful classification on 5–8 subtypes; demo integration with observability stack |

---

## Repo layout

```
gemma-trajad-eval/
  README.md
  LICENSE
  pyproject.toml

  docs/
    project-spec.md          # Full project specification
    labeling-guidelines.md   # Anomaly labeling rules and examples
    evaluation-plan.md       # Metrics, splits, and evaluation protocol

  data/
    raw/                     # Downloaded source traces (gitignored)
    interim/                 # Normalized, pre-perturbation records
    processed/               # Final JSONL dataset
    eval/                    # Held-out evaluation set

  dataset_builder/
    download_hermes.py       # Download and cache Hermes traces
    inspect_traces.py        # EDA utilities
    normalize_trajectory.py  # Convert ShareGPT → internal format
    perturbations.py         # 8 perturbation rules
    build_trajad_dataset.py  # End-to-end pipeline
    validate_labels.py       # Schema and consistency checks

  training/
    prepare_sft_data.py      # Format dataset for SFT
    train_e2b.py             # mlx-tune training script (E2B)
    train_e4b.py             # Unsloth training script (E4B / cloud)
    inference.py             # Local inference and batch evaluation
    evaluate.py              # Metrics computation

  prompts/
    anomaly_binary.txt       # Binary detection prompt template
    anomaly_localize.txt     # Localization prompt template
    anomaly_joint.txt        # Joint detection + localization + type

  integrations/
    langfuse_demo.py         # Langfuse trajectory scorer demo
    phoenix_openinference_demo.py
    smolagents_demo.py       # Run agent → export trace → verify

  notebooks/
    01_trace_exploration.ipynb
    02_perturbation_analysis.ipynb
    03_eval_report.ipynb

  outputs/
    adapters/                # Saved LoRA adapters (gitignored)
    reports/                 # Evaluation reports
```

---

## Milestones

| Week | Goal |
|------|------|
| 1 | Load and inspect Hermes filtered traces; write trajectory normalizer; define anomaly taxonomy; review 30 traces manually |
| 2 | Implement first 4 perturbation rules; generate first synthetic dataset; hand-check 100 examples; publish dataset schema draft |
| 3 | Create SFT prompts for binary detection; fine-tune Gemma 4 E2B on small sample; evaluate on held-out synthetic set |
| 4 | Add localization; build local demo with one tracing tool; publish repo and write-up |
| 5+ | Compare E2B vs E4B; add harder anomaly types; release HF dataset and adapter |

---

## Community / integration targets

| Project | Repo | Potential contribution |
|---------|------|----------------------|
| Langfuse | [langfuse/langfuse](https://github.com/langfuse/langfuse) | Cookbook: trajectory anomaly detection for agent traces |
| Arize Phoenix | [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix) | Notebook / plugin for localized trajectory failure analysis |
| OpenInference | [spec](https://arize-ai.github.io/openinference/spec/) | Proposal for `trajectory.anomalous`, `trajectory.bad_step`, etc. |
| AgentOps | [AgentOps-AI/agentops](https://github.com/AgentOps-AI/agentops) | Offline/runtime trace-quality scorer integration |
| smolagents | [docs](https://huggingface.co/docs/smolagents/en/tutorials/inspect_runs) | End-to-end demo: run agent → export trace → flag step |

---

## Resource links

### Paper
- **TrajAD paper:** https://arxiv.org/abs/2602.06443

### Hermes resources
- Hermes Agent trajectory format: https://hermes-agent.nousresearch.com/docs/developer-guide/trajectory-format
- Hermes Agent batch processing: https://hermes-agent.nousresearch.com/docs/user-guide/features/batch-processing
- Hermes filtered traces dataset: https://huggingface.co/datasets/DJLougen/hermes-agent-traces-filtered
- Original Hermes reasoning traces: https://huggingface.co/datasets/lambda/hermes-agent-reasoning-traces

### Gemma resources
- Google Gemma 4 announcement: https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/
- Gemma 4 E2B-it model card: https://huggingface.co/google/gemma-4-E2B-it
- Unsloth Gemma 4 fine-tuning guide: https://unsloth.ai/docs/models/gemma-4/train
- Unsloth notebooks: https://unsloth.ai/docs/get-started/unsloth-notebooks
- Google Gemma fine-tuning docs: https://ai.google.dev/gemma/docs/tune
- Google Gemma QLoRA tutorial: https://ai.google.dev/gemma/docs/core/huggingface_text_finetune_qlora

### Local training resources
- mlx-tune (Unsloth-compatible MLX trainer): https://github.com/ARahim3/unsloth-mlx
- mlx-lm LoRA/QLoRA docs: https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md

### Community / integration resources
- Langfuse repo: https://github.com/langfuse/langfuse
- Phoenix repo: https://github.com/Arize-ai/phoenix
- OpenInference spec: https://arize-ai.github.io/openinference/spec/
- AgentOps repo: https://github.com/AgentOps-AI/agentops
- smolagents trace inspection docs: https://huggingface.co/docs/smolagents/en/tutorials/inspect_runs

### Related work
- AOI observer paper (GRPO cautionary evidence): https://arxiv.org/html/2603.03378v3

---

## Getting started

```bash
# 1. Clone and install
git clone <repo-url>
cd gemma-trajad-eval
pip install -e ".[dev]"

# 2. Download Hermes traces
python dataset_builder/download_hermes.py

# 3. Inspect traces
python dataset_builder/inspect_traces.py

# 4. Build dataset
python dataset_builder/build_trajad_dataset.py

# 5. Prepare SFT data
python training/prepare_sft_data.py

# 6. Train (local Mac)
python training/train_e2b.py

# 7. Evaluate
python training/evaluate.py
```

---

## License

MIT — see [LICENSE](LICENSE).
