"""Format the TrajAD dataset for SFT training.

Reads processed JSONL from data/processed/ and writes chat-formatted
examples to data/processed/{train,dev,test}_sft.jsonl.

Three task modes are supported:
    binary   - predict is_anomalous only
    localize - predict is_anomalous + bad_step
    joint    - predict is_anomalous + bad_step + anomaly_type + explanation

Usage:
    python training/prepare_sft_data.py --task binary
    python training/prepare_sft_data.py --task joint
"""

import argparse
import json
from pathlib import Path

PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


def load_prompt(name: str) -> str:
    path = PROMPTS_DIR / f"{name}.txt"
    return path.read_text().strip()


def trajectory_to_text(trajectory: list[dict]) -> str:
    lines = []
    for i, msg in enumerate(trajectory):
        role = msg["role"].upper()
        content = (msg.get("content") or "").strip()
        lines.append(f"[Step {i}] [{role}]\n{content}")
    return "\n\n".join(lines)


def build_target(record: dict, task: str) -> str:
    if task == "binary":
        return json.dumps({"anomalous": record["is_anomalous"]})

    if task == "localize":
        return json.dumps({
            "anomalous": record["is_anomalous"],
            "bad_step": record["bad_step"],
        })

    if task == "joint":
        return json.dumps({
            "anomalous": record["is_anomalous"],
            "bad_step": record["bad_step"],
            "anomaly_type": record["anomaly_type"],
            "confidence": 0.85 if record["is_anomalous"] else 0.90,
            "explanation": (
                f"Anomaly detected at step {record['bad_step']}: {record['anomaly_type']}."
                if record["is_anomalous"]
                else "No anomaly detected. The trajectory follows correct procedure."
            ),
        })

    raise ValueError(f"Unknown task: {task!r}")


def format_record(record: dict, task: str, system_prompt: str) -> dict:
    traj_text = trajectory_to_text(record["trajectory"])
    user_content = f"Trajectory:\n\n{traj_text}\n\nTask: {task}"
    target = build_target(record, task)

    return {
        "id": record["id"],
        "messages": [
            {"role": "system",    "content": system_prompt},
            {"role": "user",      "content": user_content},
            {"role": "assistant", "content": target},
        ],
    }


def process_split(
    input_path: Path,
    output_path: Path,
    task: str,
    system_prompt: str,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    written = 0
    with input_path.open() as fin, output_path.open("w") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            formatted = format_record(record, task, system_prompt)
            fout.write(json.dumps(formatted) + "\n")
            written += 1
    print(f"  {written:,} examples → {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--task",
        choices=["binary", "localize", "joint"],
        default="binary",
        help="Output task format",
    )
    args = parser.parse_args()

    prompt_map = {
        "binary":   "anomaly_binary",
        "localize": "anomaly_localize",
        "joint":    "anomaly_joint",
    }
    system_prompt = load_prompt(prompt_map[args.task])
    print(f"Preparing SFT data for task={args.task!r}")

    for split in ("train", "dev", "test"):
        src = PROCESSED_DIR / f"{split}.jsonl"
        dst = PROCESSED_DIR / f"{split}_sft_{args.task}.jsonl"
        if not src.exists():
            print(f"  Skipping {split} (not found)")
            continue
        process_split(src, dst, args.task, system_prompt)


if __name__ == "__main__":
    main()
