# Evaluation plan

Metrics, data splits, and evaluation protocol for the Gemma-TrajAD anomaly detector.

---

## Overview

Evaluation covers three tasks:

| Task | Description |
|------|-------------|
| T1: Binary detection | Predict `is_anomalous` (true/false) |
| T2: Localization | Predict `bad_step` (step index or null) |
| T3: Classification | Predict `anomaly_type` (10-class taxonomy or null) |

Each model run is evaluated independently on T1 first, then T1+T2, then T1+T2+T3.

---

## Data splits

### Split rationale

| Split | Size | Source | Purpose |
|-------|------|--------|---------|
| Train | ~2,400 | Synthetic perturbations + normal | SFT training |
| Dev | ~400 | Synthetic perturbations + normal | Hyperparameter tuning, early stopping |
| Test (synthetic) | ~400 | Synthetic perturbations + normal | Final automated evaluation |
| Test (manual) | 150 | Hand-reviewed subset | High-quality held-out set |

### Construction rules

- Normal examples: 50% of each split
- Anomalous examples: 50% of each split, balanced across perturbation rules where possible
- No source trace appears in both train and eval splits (split by `source_trace_id`)
- Manual review set is drawn from the synthetic test split; it does not add new examples

### Class balance

Target distribution in train/dev/test (anomalous examples only):

| Subtype | Target % |
|---------|---------|
| `wrong_tool_choice` | 12% |
| `bad_tool_arguments` | 12% |
| `skipped_required_step` | 14% |
| `repeated_step` | 12% |
| `premature_final_answer` | 12% |
| `continued_after_sufficient_evidence` | 10% |
| `contradicted_tool_result` | 12% |
| `hallucinated_tool` | 8% |
| `invalid_tool_json` | 4% |
| `unnecessary_replanning` | 4% |

---

## Metrics

### T1: Binary anomaly detection

| Metric | Description | Target (MVP) |
|--------|-------------|-------------|
| Accuracy | Overall correct predictions | > 70% |
| Precision | TP / (TP + FP) | > 0.65 |
| Recall | TP / (TP + FN) | > 0.65 |
| F1 | Harmonic mean of precision and recall | > 0.65 |
| AUROC | Area under ROC curve | > 0.75 |

Baseline: majority-class classifier = 50% accuracy (balanced split).

### T2: Step localization

Evaluated only on anomalous examples where `is_anomalous` is correctly predicted.

| Metric | Description | Target (MVP) |
|--------|-------------|-------------|
| Exact-match accuracy | Predicted step == true step | > 40% |
| ±1 tolerance accuracy | |predicted - true| ≤ 1 | > 55% |
| Mean absolute error | Average step index distance | < 2.0 |

### T3: Anomaly type classification

Evaluated only on anomalous examples where `is_anomalous` is correctly predicted.

| Metric | Description | Target (MVP) |
|--------|-------------|-------------|
| Macro F1 | Unweighted F1 across all 10 subtypes | > 0.40 |
| Accuracy | Correct subtype prediction | > 45% |
| Top-3 accuracy | True label in top-3 predictions | > 65% |

### Output quality

| Metric | Description | Target |
|--------|-------------|--------|
| JSON validity rate | % of outputs that parse as valid JSON | > 95% |
| Schema compliance | % of valid JSON outputs that match the response schema | > 90% |
| Confidence calibration | Expected calibration error (ECE) | < 0.15 |

### Inference

| Metric | Description |
|--------|-------------|
| Latency (p50) | Median time per trajectory on M3 |
| Latency (p95) | 95th percentile time per trajectory |
| Throughput | Trajectories per minute |

---

## Evaluation protocol

### Automated evaluation

Run `training/evaluate.py` against the test split after each training run.

```bash
python training/evaluate.py \
  --model outputs/adapters/<run-name> \
  --data data/eval/test.jsonl \
  --tasks binary localize classify \
  --output outputs/reports/<run-name>.json
```

Output format:

```json
{
  "run": "e2b-sft-lora-run1",
  "timestamp": "2025-04-12T10:00:00Z",
  "t1_accuracy": 0.74,
  "t1_f1": 0.71,
  "t1_auroc": 0.79,
  "t2_exact": 0.45,
  "t2_pm1": 0.58,
  "t2_mae": 1.8,
  "t3_macro_f1": 0.44,
  "t3_accuracy": 0.48,
  "json_validity": 0.97,
  "schema_compliance": 0.94,
  "latency_p50_ms": 1200,
  "latency_p95_ms": 3400
}
```

### Manual review evaluation

For the 150-sample manual review set, additionally check:

1. Does the explanation cite the actual failing step?
2. Is the stated anomaly type coherent with the explanation?
3. Is the confidence score plausible given the difficulty?

Rate each on a 1–3 scale and report mean rating.

### Regression checks

After each model update, compare against the previous run's metrics. Flag regressions of > 5% absolute on any primary metric.

---

## Baselines

### Zero-shot baseline

Prompt the base Gemma 4 E2B-it (no fine-tuning) with the same prompt template and evaluate. This establishes the floor.

### Majority-class baseline

Predict `is_anomalous: false` for all examples. This gives 50% accuracy on a balanced test set.

### Rule-based baseline

Use simple heuristics (e.g., detect invalid JSON in tool calls, detect duplicate tool calls) to flag anomalies. Report precision/recall/F1.

---

## Ablation study plan

After the full joint model (Run 3) is trained:

| Ablation | What changes | Question |
|----------|-------------|---------|
| A1 | No explanation in output | Does generating an explanation improve label accuracy? |
| A2 | No confidence score in output | Does predicting confidence affect classification? |
| A3 | Random bad_step baseline | How much does step localization contribute to type accuracy? |
| A4 | Train on only 2 perturbation rules | How sensitive is generalization to data diversity? |
| A5 | E2B vs E4B | Does the larger model improve localization? |

---

## Reporting

Results are saved to `outputs/reports/` in JSON format and summarized in `notebooks/03_eval_report.ipynb`.

Report structure:

1. Dataset statistics (size, class balance, split details)
2. Baseline results
3. Run 1 results (binary detection)
4. Run 2 results (binary + localization)
5. Run 3 results (full joint)
6. DPO results (if applicable)
7. Ablation results
8. Error analysis: 20 randomly sampled false positives, 20 false negatives
9. Localization failure analysis: cases where exact match fails but ±1 succeeds

---

## Known limitations

- Synthetic perturbations may not capture all real-world anomaly patterns
- Label noise in synthetically generated examples may suppress localization accuracy
- Manual review set (150 samples) is small; results should be interpreted as indicative
- GRPO localization may regress even as binary detection improves (see AOI observer paper: https://arxiv.org/html/2603.03378v3)
