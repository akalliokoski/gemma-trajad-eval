"""Local inference and batch evaluation for the anomaly detector.

Usage:
    # Single trajectory from a JSON file
    python training/inference.py --adapter outputs/adapters/e2b-sft-binary-run1/final \
        --trajectory path/to/trace.json

    # Batch evaluation against a JSONL file
    python training/inference.py --adapter outputs/adapters/e2b-sft-binary-run1/final \
        --batch data/processed/test_sft_binary.jsonl \
        --output outputs/reports/predictions.jsonl
"""

import argparse
import json
import time
from pathlib import Path

MODEL_ID = "google/gemma-4-E2B-it"
MAX_NEW_TOKENS = 256
TEMPERATURE = 0.1  # Near-greedy for structured output


def load_model(adapter_path: str | None = None):
    """Load model with optional LoRA adapter."""
    try:
        from mlx_tune import FastLanguageModel
        backend = "mlx"
    except ImportError:
        from unsloth import FastLanguageModel
        backend = "unsloth"

    print(f"Loading model ({backend}) ...")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=adapter_path or MODEL_ID,
        max_seq_length=4096,
        load_in_4bit=False,
    )
    FastLanguageModel.for_inference(model)
    return model, tokenizer, backend


def predict(model, tokenizer, messages: list[dict]) -> tuple[str, float]:
    """Run inference on a single set of messages. Returns (output_text, latency_ms)."""
    input_ids = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    )

    t0 = time.perf_counter()
    output_ids = model.generate(
        input_ids,
        max_new_tokens=MAX_NEW_TOKENS,
        temperature=TEMPERATURE,
        do_sample=TEMPERATURE > 0,
    )
    latency_ms = (time.perf_counter() - t0) * 1000

    new_tokens = output_ids[0][input_ids.shape[1]:]
    output_text = tokenizer.decode(new_tokens, skip_special_tokens=True)
    return output_text, latency_ms


def parse_output(text: str) -> dict | None:
    """Try to parse the model output as JSON."""
    text = text.strip()
    # Strip markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:-1]) if len(lines) > 2 else text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def run_single(adapter_path: str | None, trajectory_path: Path) -> None:
    model, tokenizer, _ = load_model(adapter_path)
    trajectory = json.loads(trajectory_path.read_text())

    from training.prepare_sft_data import trajectory_to_text
    traj_text = trajectory_to_text(trajectory)

    messages = [
        {"role": "user", "content": f"Trajectory:\n\n{traj_text}\n\nTask: joint"},
    ]
    output, latency_ms = predict(model, tokenizer, messages)
    parsed = parse_output(output)

    print(f"\nRaw output:\n{output}")
    print(f"\nParsed:\n{json.dumps(parsed, indent=2) if parsed else 'PARSE FAILED'}")
    print(f"\nLatency: {latency_ms:.0f} ms")


def run_batch(adapter_path: str | None, batch_path: Path, output_path: Path) -> None:
    model, tokenizer, _ = load_model(adapter_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    latencies = []
    json_valid = 0
    total = 0

    with batch_path.open() as fin, output_path.open("w") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            messages = record["messages"][:-1]  # exclude assistant target

            output_text, latency_ms = predict(model, tokenizer, messages)
            parsed = parse_output(output_text)

            latencies.append(latency_ms)
            if parsed is not None:
                json_valid += 1
            total += 1

            result = {
                "id": record.get("id"),
                "raw_output": output_text,
                "parsed": parsed,
                "latency_ms": round(latency_ms, 1),
            }
            fout.write(json.dumps(result) + "\n")

            if total % 50 == 0:
                print(f"  {total} predictions ...")

    latencies.sort()
    p50 = latencies[len(latencies) // 2]
    p95 = latencies[int(len(latencies) * 0.95)]
    print(f"\nBatch complete: {total} predictions")
    print(f"JSON validity: {json_valid}/{total} ({100*json_valid/total:.1f}%)")
    print(f"Latency p50={p50:.0f}ms  p95={p95:.0f}ms")
    print(f"Output → {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--adapter", default=None, help="Path to LoRA adapter directory")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--trajectory", type=Path, help="Single trajectory JSON file")
    group.add_argument("--batch", type=Path, help="JSONL file with SFT-formatted examples")
    parser.add_argument("--output", type=Path, default=Path("outputs/reports/predictions.jsonl"))
    args = parser.parse_args()

    if args.trajectory:
        run_single(args.adapter, args.trajectory)
    else:
        run_batch(args.adapter, args.batch, args.output)


if __name__ == "__main__":
    main()
