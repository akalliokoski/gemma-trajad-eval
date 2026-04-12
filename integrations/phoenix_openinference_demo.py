"""Arize Phoenix + OpenInference integration demo.

Shows how to:
1. Export spans from Phoenix
2. Convert to internal trajectory format
3. Score with the Gemma anomaly detector
4. Annotate spans with anomaly scores using proposed OpenInference fields

References:
    Phoenix repo:          https://github.com/Arize-ai/phoenix
    OpenInference spec:    https://arize-ai.github.io/openinference/spec/
    Phoenix Python SDK:    https://docs.arize.com/phoenix

Proposed OpenInference fields (see docs/project-spec.md):
    trajectory.anomalous     bool
    trajectory.bad_step      int
    trajectory.anomaly_type  str
    trajectory.confidence    float

Setup:
    pip install arize-phoenix openinference-semantic-conventions
    # Start Phoenix locally:
    python -m phoenix.server.main

Usage:
    python integrations/phoenix_openinference_demo.py --session-id <id>
    python integrations/phoenix_openinference_demo.py --limit 20
"""

import argparse
import json
from pathlib import Path

ADAPTER_PATH = Path(__file__).parent.parent / "outputs" / "adapters" / "e2b-sft-joint-run1" / "final"
SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "anomaly_joint.txt").read_text().strip()

# Proposed OpenInference span attribute names for trajectory anomaly scoring
ATTR_ANOMALOUS = "trajectory.anomalous"
ATTR_BAD_STEP = "trajectory.bad_step"
ATTR_ANOMALY_TYPE = "trajectory.anomaly_type"
ATTR_CONFIDENCE = "trajectory.confidence"


def spans_to_trajectory(spans: list[dict]) -> list[dict]:
    """Convert a list of Phoenix spans (sorted by start time) to trajectory format."""
    trajectory = []
    for span in sorted(spans, key=lambda s: s.get("start_time", "")):
        span_kind = span.get("span_kind", "")
        attrs = span.get("attributes", {})

        if span_kind == "LLM":
            input_msgs = attrs.get("llm.input_messages", [])
            for msg in input_msgs:
                role = msg.get("message.role", "user")
                content = msg.get("message.content", "") or ""
                trajectory.append({"role": role, "content": content})
            output_msgs = attrs.get("llm.output_messages", [])
            for msg in output_msgs:
                content = msg.get("message.content", "") or ""
                trajectory.append({"role": "assistant", "content": content})

        elif span_kind == "TOOL":
            output = attrs.get("output.value", "")
            trajectory.append({
                "role": "tool",
                "content": output if isinstance(output, str) else json.dumps(output),
            })

    return trajectory


def score_trajectory(model, tokenizer, trajectory: list[dict]) -> dict:
    from training.inference import parse_output, predict

    traj_lines = []
    for i, msg in enumerate(trajectory):
        content = (msg.get("content") or "")[:1000]
        traj_lines.append(f"[Step {i}] [{msg['role'].upper()}]\n{content}")
    traj_text = "\n\n".join(traj_lines)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": f"Trajectory:\n\n{traj_text}\n\nTask: joint"},
    ]
    output_text, _ = predict(model, tokenizer, messages)
    return parse_output(output_text) or {}


def run(session_id: str | None = None, limit: int = 10, phoenix_host: str = "http://localhost:6006") -> None:
    import httpx

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

    # Fetch trace sessions from Phoenix REST API
    params = {"limit": limit}
    if session_id:
        params["session_id"] = session_id
    resp = httpx.get(f"{phoenix_host}/v1/traces", params=params)
    resp.raise_for_status()
    traces = resp.json().get("data", [])

    print(f"Scoring {len(traces)} trace(s) from Phoenix ...")

    annotations = []
    for trace in traces:
        trace_id = trace.get("trace_id") or trace.get("context", {}).get("trace_id")
        spans = trace.get("spans", [])
        if not spans:
            continue

        trajectory = spans_to_trajectory(spans)
        if not trajectory:
            print(f"  {trace_id}: empty trajectory, skipping")
            continue

        judgment = score_trajectory(model, tokenizer, trajectory)
        is_anomalous = judgment.get("anomalous", False)
        print(
            f"  {trace_id}: anomalous={is_anomalous}  "
            f"type={judgment.get('anomaly_type')}  "
            f"step={judgment.get('bad_step')}"
        )

        # Prepare annotation for Phoenix
        annotations.append({
            "trace_id": trace_id,
            "name": "gemma_trajad",
            "annotator_kind": "LLM",
            "result": {
                "label": "anomalous" if is_anomalous else "normal",
                "score": judgment.get("confidence", 0.5),
                "explanation": judgment.get("explanation", ""),
            },
            "metadata": {
                ATTR_ANOMALOUS:    is_anomalous,
                ATTR_BAD_STEP:     judgment.get("bad_step"),
                ATTR_ANOMALY_TYPE: judgment.get("anomaly_type"),
                ATTR_CONFIDENCE:   judgment.get("confidence"),
            },
        })

    # Post annotations back to Phoenix
    if annotations:
        post_resp = httpx.post(
            f"{phoenix_host}/v1/trace_annotations",
            json=annotations,
        )
        if post_resp.status_code == 200:
            print(f"Posted {len(annotations)} annotations to Phoenix.")
        else:
            print(f"WARNING: annotation POST returned {post_resp.status_code}: {post_resp.text}")

    print("Done.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-id", help="Score traces from a specific Phoenix session")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--phoenix-host", default="http://localhost:6006")
    args = parser.parse_args()
    run(session_id=args.session_id, limit=args.limit, phoenix_host=args.phoenix_host)


if __name__ == "__main__":
    main()
