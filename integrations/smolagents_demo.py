"""smolagents end-to-end demo: run agent → export trace → verify with Gemma.

This demo shows the full pipeline:
1. Run a small smolagents agent on a task
2. Export the resulting trace
3. Convert the trace to internal trajectory format
4. Score with the Gemma anomaly detector
5. Print the flagged step and anomaly type

References:
    smolagents trace inspection: https://huggingface.co/docs/smolagents/en/tutorials/inspect_runs

Setup:
    pip install smolagents

Usage:
    python integrations/smolagents_demo.py
    python integrations/smolagents_demo.py --task "What is the capital of France?"
"""

import argparse
import json
from pathlib import Path

ADAPTER_PATH = Path(__file__).parent.parent / "outputs" / "adapters" / "e2b-sft-joint-run1" / "final"
SYSTEM_PROMPT = (Path(__file__).parent.parent / "prompts" / "anomaly_joint.txt").read_text().strip()


def run_agent(task: str) -> list[dict]:
    """Run a smolagents CodeAgent and return the collected trajectory."""
    from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

    model = HfApiModel()
    agent = CodeAgent(
        tools=[DuckDuckGoSearchTool()],
        model=model,
        max_steps=6,
    )

    # Run the agent and collect step logs
    result = agent.run(task)
    print(f"\nAgent result: {result}\n")

    # Convert smolagents step logs to internal trajectory format
    trajectory = []

    # System message
    trajectory.append({
        "role": "system",
        "content": "You are a helpful agent with access to web search.",
    })

    # User task
    trajectory.append({"role": "user", "content": task})

    # Agent steps
    for step in agent.logs:
        if hasattr(step, "llm_output") and step.llm_output:
            trajectory.append({"role": "assistant", "content": str(step.llm_output)})
        if hasattr(step, "tool_call") and step.tool_call:
            tc = step.tool_call
            tool_json = json.dumps({"name": tc.name, "arguments": tc.arguments})
            trajectory[-1]["content"] += f"\n<tool_call>{tool_json}</tool_call>"
        if hasattr(step, "observations") and step.observations:
            trajectory.append({
                "role": "tool",
                "content": f"<tool_response>{step.observations}</tool_response>",
            })

    return trajectory


def score(trajectory: list[dict]) -> dict:
    """Score a trajectory with the Gemma anomaly detector."""
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
    output_text, latency_ms = predict(model, tokenizer, messages)
    judgment = parse_output(output_text) or {}
    judgment["latency_ms"] = round(latency_ms, 1)
    return judgment


def print_report(trajectory: list[dict], judgment: dict) -> None:
    is_anomalous = judgment.get("anomalous", False)
    bad_step = judgment.get("bad_step")
    anomaly_type = judgment.get("anomaly_type")
    confidence = judgment.get("confidence", 0.0)
    explanation = judgment.get("explanation", "")

    print("=" * 60)
    print("TRAJECTORY ANOMALY REPORT")
    print("=" * 60)
    print(f"Anomalous:    {is_anomalous}")
    print(f"Anomaly type: {anomaly_type}")
    print(f"Bad step:     {bad_step}")
    print(f"Confidence:   {confidence:.2f}")
    print(f"Explanation:  {explanation}")
    print(f"Latency:      {judgment.get('latency_ms', 0):.0f} ms")

    if is_anomalous and bad_step is not None and bad_step < len(trajectory):
        print(f"\nFlagged step [{bad_step}]:")
        flagged = trajectory[bad_step]
        print(f"  Role: {flagged['role']}")
        print(f"  Content: {(flagged.get('content') or '')[:300]}")
    print("=" * 60)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--task",
        default="What is the population of Tokyo as of the latest available data?",
        help="Task to run with the agent",
    )
    args = parser.parse_args()

    print(f"Running agent on task: {args.task!r}")
    trajectory = run_agent(args.task)

    print(f"\nCollected {len(trajectory)} trajectory steps. Scoring with Gemma ...")
    judgment = score(trajectory)
    print_report(trajectory, judgment)


if __name__ == "__main__":
    main()
