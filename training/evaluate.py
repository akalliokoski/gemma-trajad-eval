"""Compute evaluation metrics for the anomaly detector.

Reads predictions JSONL (from inference.py) and the ground-truth test JSONL,
computes all metrics defined in docs/evaluation-plan.md, and writes a report.

Usage:
    python training/evaluate.py \
        --predictions outputs/reports/predictions.jsonl \
        --ground-truth data/processed/test.jsonl \
        --output outputs/reports/eval_run1.json
"""

import argparse
import json
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    roc_auc_score,
)


def load_jsonl(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def compute_metrics(preds: list[dict], gt_map: dict[str, dict]) -> dict:
    # Align predictions with ground truth by id
    aligned = []
    for pred in preds:
        pid = pred.get("id")
        gt = gt_map.get(pid)
        if gt is None:
            continue
        parsed = pred.get("parsed") or {}
        aligned.append({
            "id": pid,
            "gt_anomalous": gt["is_anomalous"],
            "gt_bad_step": gt.get("bad_step"),
            "gt_anomaly_type": gt.get("anomaly_type"),
            "pred_anomalous": parsed.get("anomalous"),
            "pred_bad_step": parsed.get("bad_step"),
            "pred_anomaly_type": parsed.get("anomaly_type"),
            "json_valid": pred.get("parsed") is not None,
            "latency_ms": pred.get("latency_ms", 0),
        })

    if not aligned:
        return {"error": "No aligned predictions found"}

    n = len(aligned)

    # JSON validity
    json_validity = sum(a["json_valid"] for a in aligned) / n

    # T1: Binary detection
    y_true = [a["gt_anomalous"] for a in aligned]
    y_pred_raw = [a["pred_anomalous"] for a in aligned]
    # Handle None predictions as False
    y_pred = [bool(p) if p is not None else False for p in y_pred_raw]

    t1_accuracy = accuracy_score(y_true, y_pred)
    t1_f1 = f1_score(y_true, y_pred, zero_division=0)
    try:
        t1_auroc = float(roc_auc_score(y_true, [1 if p else 0 for p in y_pred]))
    except ValueError:
        t1_auroc = None

    # T2: Localization (on anomalous examples with correct binary prediction)
    loc_examples = [
        a for a in aligned
        if a["gt_anomalous"] and a["pred_anomalous"] and a["gt_bad_step"] is not None
    ]
    if loc_examples:
        exact = [
            a["pred_bad_step"] == a["gt_bad_step"]
            for a in loc_examples
            if a["pred_bad_step"] is not None
        ]
        pm1 = [
            abs((a["pred_bad_step"] or -999) - a["gt_bad_step"]) <= 1
            for a in loc_examples
        ]
        mae_vals = [
            abs((a["pred_bad_step"] or 0) - a["gt_bad_step"])
            for a in loc_examples
        ]
        t2_exact = sum(exact) / len(loc_examples) if loc_examples else None
        t2_pm1 = sum(pm1) / len(loc_examples) if loc_examples else None
        t2_mae = sum(mae_vals) / len(mae_vals) if mae_vals else None
    else:
        t2_exact = t2_pm1 = t2_mae = None

    # T3: Anomaly type classification (on anomalous examples with correct binary)
    type_examples = [
        a for a in loc_examples
        if a["gt_anomaly_type"] is not None and a["pred_anomaly_type"] is not None
    ]
    if type_examples:
        yt3 = [a["gt_anomaly_type"] for a in type_examples]
        yp3 = [a["pred_anomaly_type"] for a in type_examples]
        t3_accuracy = accuracy_score(yt3, yp3)
        t3_macro_f1 = float(f1_score(yt3, yp3, average="macro", zero_division=0))
    else:
        t3_accuracy = t3_macro_f1 = None

    # Latency
    latencies = sorted(a["latency_ms"] for a in aligned)
    lat_p50 = latencies[len(latencies) // 2]
    lat_p95 = latencies[int(len(latencies) * 0.95)]

    return {
        "n_examples": n,
        "json_validity": round(json_validity, 4),
        "t1_accuracy": round(t1_accuracy, 4),
        "t1_f1": round(t1_f1, 4),
        "t1_auroc": round(t1_auroc, 4) if t1_auroc is not None else None,
        "t2_exact": round(t2_exact, 4) if t2_exact is not None else None,
        "t2_pm1": round(t2_pm1, 4) if t2_pm1 is not None else None,
        "t2_mae": round(t2_mae, 4) if t2_mae is not None else None,
        "t3_accuracy": round(t3_accuracy, 4) if t3_accuracy is not None else None,
        "t3_macro_f1": round(t3_macro_f1, 4) if t3_macro_f1 is not None else None,
        "latency_p50_ms": round(lat_p50, 1),
        "latency_p95_ms": round(lat_p95, 1),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--ground-truth", type=Path, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("outputs/reports/eval_results.json"),
    )
    args = parser.parse_args()

    preds = load_jsonl(args.predictions)
    gt_records = load_jsonl(args.ground_truth)
    gt_map = {r["id"]: r for r in gt_records}

    metrics = compute_metrics(preds, gt_map)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(metrics, indent=2))

    print("\n=== Evaluation results ===")
    for k, v in metrics.items():
        print(f"  {k:30s}: {v}")
    print(f"\nReport → {args.output}")


if __name__ == "__main__":
    main()
