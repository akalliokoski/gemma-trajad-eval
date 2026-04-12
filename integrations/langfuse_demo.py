"""Langfuse integration demo: score agent traces with the Gemma anomaly detector.

This demo shows how to:
1. Fetch stored traces from Langfuse
2. Convert them to the internal trajectory format
3. Run the Gemma anomaly detector
4. Write anomaly scores back to Langfuse as evaluations

References:
    Langfuse repo: https://github.com/langfuse/langfuse
    Langfuse Python SDK: https://python.langfuse.com/

Setup:
    pip install langfuse
    export LANGFUSE_PUBLIC_KEY=pk-...
    export LANGFUSE_SECRET_KEY=sk-...
    export LANGFUSE_HOST=https://cloud.langfuse.com  # or your self-hosted URL

Usage:
    python integrations/langfuse_demo.py --trace-id <trace_id>
    python integrations/langfuse_demo.py --limit 20   # score last 20 traces
"""

import argparse
import json
import os
from pathlib import Path

ADAPTER_PATH = Path(__file__).parent.parent / "outputs" / "adapters" / "e2b-sft-joint-run1" / "final"
SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "anomaly_joint.txt").read_text().strip()


def lf_message_to_internal(msg: dict) -> dict:
    """Convert a Langfuse message to internal trajectory format."""
    role = msg.get("role", "user")
    content = msg.get("content", "") or ""
    return {"role": role, "content": content}


def trace_to_trajectory(trace) -> list[dict]:
    """Extract the message trajectory from a Langfuse trace object."""
    messages = []
    for obs in sorted(trace.observations, key=lambda o: o.start_time):
        if obs.type == "GENERATION":
            if obs.input:
                for msg in (obs.input if isinstance(obs.input, list) else [obs.input]):
                    if isinstance(msg, dict):
                        messages.append(lf_message_to_internal(msg))
            if obs.output:
                output = obs.output
                if isinstance(output, str):
                    messages.append({"role": "assistant", "content": output})
                elif isinstance(output, dict):
                    messages.append({"role": "assistant", "content": json.dumps(output)})
        elif obs.type == "TOOL":
            if obs.output:
                messages.append({
                    "role": "tool",
                    "content": json.dumps(obs.output) if not isinstance(obs.output, str) else obs.output,
                })
    return messages


def score_trace(model, tokenizer, trajectory: list[dict]) -> dict:
    """Run anomaly detection on a trajectory. Returns parsed judgment dict."""
    from training.inference import predict, parse_output

    traj_lines = []
    for i, msg in enumerate(trajectory):
        content = (msg.get("content") or "")[:1000]
        traj_lines.append(f"[Step {i}] [{msg['role'].upper()}]\n{content}")
    traj_text = "\n\n".join(traj_lines)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": f"Trajectory:\n\n{traj_text}\n\nTask: joint"},
    ]
    output_text, latency_ms = predict(model, tokenizer, messages)
    parsed = parse_output(output_text) or {}
    parsed["latency_ms"] = round(latency_ms, 1)
    return parsed


def run(trace_id: str | None = None, limit: int = 10) -> None:
    from langfuse import Langfuse

    lf = Langfuse(
        public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
        secret_key=os.environ["LANGFUSE_SECRET_KEY"],
        host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
    )

    # Load model
    try:
        from mlx_tune import FastLanguageModel
    except ImportError:
        from unsloth import FastLanguageModel

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=str(ADAPTER_PATH) if ADAPTER_PATH.exists() else "google/gemma-4-E2B-it",
        max_seq_length=4096,
        load_in_4bit=False,
    )
    FastLanguageModel.for_inference(model)

    # Fetch traces
    if trace_id:
        traces = [lf.get_trace(trace_id)]
    else:
        traces = lf.get_traces(limit=limit).data

    print(f"Scoring {len(traces)} trace(s) ...")

    for trace in traces:
        trajectory = trace_to_trajectory(trace)
        if not trajectory:
            print(f"  {trace.id}: no trajectory extracted, skipping")
            continue

        judgment = score_trace(model, tokenizer, trajectory)
        is_anomalous = judgment.get("anomalous", False)
        anomaly_type = judgment.get("anomaly_type", "none")
        confidence = judgment.get("confidence", 0.5)
        bad_step = judgment.get("bad_step")

        print(f"  {trace.id}: anomalous={is_anomalous}  type={anomaly_type}  step={bad_step}  conf={confidence:.2f}")

        # Write scores back to Langfuse
        lf.score(
            trace_id=trace.id,
            name="anomaly_detected",
            value=1.0 if is_anomalous else 0.0,
            comment=judgment.get("explanation", ""),
        )
        if is_anomalous:
            lf.score(
                trace_id=trace.id,
                name="anomaly_type",
                value=0.0,
                comment=anomaly_type,
            )
            if bad_step is not None:
                lf.score(
                    trace_id=trace.id,
                    name="bad_step",
                    value=float(bad_step),
                )

    print("Done.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--trace-id", help="Score a single trace by ID")
    group.add_argument("--limit", type=int, default=10, help="Score last N traces")
    args = parser.parse_args()
    run(trace_id=args.trace_id, limit=args.limit)


if __name__ == "__main__":
    main()
