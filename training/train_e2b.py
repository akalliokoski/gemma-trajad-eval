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


def load_training_backend():
    # mlx-tune provides an Unsloth-compatible API for Apple Silicon.
    # Import lazily so argument parsing and lightweight inspection still work on the VPS.
    try:
        from mlx_tune import FastLanguageModel, SFTTrainer, TrainingArguments
    except ImportError as exc:
        print("mlx-tune not found. Install with: pip install mlx-tune")
        print("For CUDA, use: pip install unsloth")
        raise exc
    return FastLanguageModel, SFTTrainer, TrainingArguments, "mlx"


def load_sft_data(split: str, task: str, max_examples: int | None = None) -> list[dict]:
    path = PROCESSED_DIR / f"{split}_sft_{task}.jsonl"
    if not path.exists():
        raise FileNotFoundError(
            f"SFT data not found: {path}\n"
            f"Run: python training/prepare_sft_data.py --task {task}"
        )
    rows = []
    with path.open() as f:
        for line in f:
            if not line.strip():
                continue
            rows.append(json.loads(line))
            if max_examples is not None and len(rows) >= max_examples:
                break
    return rows


def train(
    task: str,
    run_name: str,
    max_seq_length: int,
    max_train_examples: int | None,
    max_eval_examples: int | None,
) -> None:
    adapter_path = ADAPTERS_DIR / run_name
    adapter_path.mkdir(parents=True, exist_ok=True)

    FastLanguageModel, SFTTrainer, TrainingArguments, backend = load_training_backend()

    print(f"Loading model: {MODEL_ID}")
    print(f"Backend: {backend}")
    print(f"Task: {task}")
    print(f"Run name: {run_name}")
    print(f"Max sequence length: {max_seq_length}")
    if max_train_examples is not None:
        print(f"Train subset: first {max_train_examples:,} examples")
    if max_eval_examples is not None:
        print(f"Eval subset: first {max_eval_examples:,} examples")

    # Load model with LoRA
    # mlx-tune / Unsloth-compatible API
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=MODEL_ID,
        max_seq_length=max_seq_length,
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
    train_data = load_sft_data("train", task, max_examples=max_train_examples)
    dev_data = load_sft_data("dev", task, max_examples=max_eval_examples)
    print(f"Train: {len(train_data):,}  Dev: {len(dev_data):,}")

    # Training arguments
    # mlx-tune exposes a TrainingArguments compatible with transformers/TRL
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
        max_seq_length=max_seq_length,
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
    parser.add_argument(
        "--max-seq-length",
        type=int,
        default=MAX_SEQ_LENGTH,
        help=f"Training context length cap (default: {MAX_SEQ_LENGTH})",
    )
    parser.add_argument(
        "--max-train-examples",
        type=int,
        default=None,
        help="Optional cap for a small smoke-test subset of training rows",
    )
    parser.add_argument(
        "--max-eval-examples",
        type=int,
        default=None,
        help="Optional cap for a small smoke-test subset of eval rows",
    )
    args = parser.parse_args()
    run_name = args.run_name or f"e2b-sft-{args.task}-run1"
    train(
        args.task,
        run_name,
        max_seq_length=args.max_seq_length,
        max_train_examples=args.max_train_examples,
        max_eval_examples=args.max_eval_examples,
    )


if __name__ == "__main__":
    main()
