"""Fine-tune Gemma 4 E2B-it with LoRA SFT on Apple Silicon via mlx-tune.

This script uses the mlx-tune API (Unsloth-compatible) for local Mac prototyping.
The same training style can be moved to CUDA by swapping the import:
    from unsloth import FastLanguageModel

References:
    mlx-tune: https://github.com/ARahim3/unsloth-mlx
    mlx-lm LoRA docs: https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md
    Gemma 4 E2B-it: https://huggingface.co/google/gemma-4-E2B-it
    Unsloth Gemma 4 guide: https://unsloth.ai/docs/models/gemma-4/train

Hardware target: Apple M3, 32 GB unified memory

Usage:
    python training/train_e2b.py --task binary
    python training/train_e2b.py --task joint --run-name e2b-sft-joint-run1
"""

import argparse
import json
from pathlib import Path

# mlx-tune provides an Unsloth-compatible API for Apple Silicon
# Swap for `from unsloth import FastLanguageModel` on CUDA
try:
    from mlx_tune import FastLanguageModel
    BACKEND = "mlx"
except ImportError:
    print("mlx-tune not found. Install with: pip install mlx-tune")
    print("For CUDA, use: pip install unsloth")
    raise

MODEL_ID = "google/gemma-4-E2B-it"
# https://huggingface.co/google/gemma-4-E2B-it

PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
ADAPTERS_DIR = Path(__file__).parent.parent / "outputs" / "adapters"

# LoRA hyperparameters
LORA_R = 16
LORA_ALPHA = 32
LORA_DROPOUT = 0.05
TARGET_MODULES = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
]

# Training hyperparameters
MAX_SEQ_LENGTH = 4096
LEARNING_RATE = 2e-4
NUM_EPOCHS = 2
BATCH_SIZE = 2
GRAD_ACCUM_STEPS = 4


def load_sft_data(split: str, task: str) -> list[dict]:
    path = PROCESSED_DIR / f"{split}_sft_{task}.jsonl"
    if not path.exists():
        raise FileNotFoundError(
            f"SFT data not found: {path}\n"
            f"Run: python training/prepare_sft_data.py --task {task}"
        )
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def train(task: str, run_name: str) -> None:
    adapter_path = ADAPTERS_DIR / run_name
    adapter_path.mkdir(parents=True, exist_ok=True)

    print(f"Loading model: {MODEL_ID}")
    print(f"Backend: {BACKEND}")
    print(f"Task: {task}")
    print(f"Run name: {run_name}")

    # Load model with LoRA
    # mlx-tune / Unsloth-compatible API
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=MODEL_ID,
        max_seq_length=MAX_SEQ_LENGTH,
        load_in_4bit=False,  # Use LoRA (not QLoRA) for stability on M3
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r=LORA_R,
        target_modules=TARGET_MODULES,
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        bias="none",
        use_gradient_checkpointing=True,
    )

    # Load SFT data
    train_data = load_sft_data("train", task)
    dev_data = load_sft_data("dev", task)
    print(f"Train: {len(train_data):,}  Dev: {len(dev_data):,}")

    # Training arguments
    # mlx-tune exposes a TrainingArguments compatible with transformers/TRL
    from mlx_tune import SFTTrainer, TrainingArguments

    training_args = TrainingArguments(
        output_dir=str(adapter_path),
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM_STEPS,
        learning_rate=LEARNING_RATE,
        lr_scheduler_type="cosine",
        warmup_ratio=0.1,
        logging_steps=50,
        eval_strategy="steps",
        eval_steps=200,
        save_strategy="steps",
        save_steps=200,
        save_total_limit=2,
        load_best_model_at_end=True,
        bf16=True,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_data,
        eval_dataset=dev_data,
        args=training_args,
        dataset_text_field="messages",
        max_seq_length=MAX_SEQ_LENGTH,
    )

    print("Starting training ...")
    trainer.train()
    trainer.save_model(str(adapter_path / "final"))
    print(f"Adapter saved → {adapter_path / 'final'}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--task",
        choices=["binary", "localize", "joint"],
        default="binary",
        help="Training task (default: binary)",
    )
    parser.add_argument(
        "--run-name",
        default=None,
        help="Name for this run (default: e2b-sft-<task>-run1)",
    )
    args = parser.parse_args()
    run_name = args.run_name or f"e2b-sft-{args.task}-run1"
    train(args.task, run_name)


if __name__ == "__main__":
    main()
