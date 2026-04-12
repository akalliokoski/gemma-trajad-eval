"""Fine-tune Gemma 4 E4B-it with LoRA SFT on NVIDIA GPU via Unsloth.

Use this script for cloud GPU runs (A100/H100) after local E2B prototyping is stable.

References:
    Unsloth Gemma 4 guide:    https://unsloth.ai/docs/models/gemma-4/train
    Unsloth notebooks:        https://unsloth.ai/docs/get-started/unsloth-notebooks
    Google Gemma fine-tuning: https://ai.google.dev/gemma/docs/tune
    Google Gemma QLoRA:       https://ai.google.dev/gemma/docs/core/huggingface_text_finetune_qlora

Hardware target: A100 (40/80 GB) or H100

Usage:
    python training/train_e4b.py --task binary
    python training/train_e4b.py --task joint --qlora
"""

import argparse
import json
from pathlib import Path

try:
    from unsloth import FastLanguageModel
    BACKEND = "unsloth"
except ImportError:
    print("Unsloth not found. Install with: pip install unsloth")
    print("For local Mac, use train_e2b.py with mlx-tune.")
    raise

MODEL_ID = "google/gemma-4-E4B-it"

PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"
ADAPTERS_DIR = Path(__file__).parent.parent / "outputs" / "adapters"

# LoRA hyperparameters (Unsloth recommends conservative settings for Gemma 4)
LORA_R = 16
LORA_ALPHA = 16
LORA_DROPOUT = 0.0
TARGET_MODULES = [
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj",
]

# Training hyperparameters
MAX_SEQ_LENGTH = 8192
LEARNING_RATE = 2e-4
NUM_EPOCHS = 3
BATCH_SIZE = 4
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


def train(task: str, run_name: str, use_qlora: bool) -> None:
    adapter_path = ADAPTERS_DIR / run_name
    adapter_path.mkdir(parents=True, exist_ok=True)

    print(f"Loading model: {MODEL_ID}")
    print(f"Backend: {BACKEND}")
    print(f"Task: {task}")
    print(f"QLoRA: {use_qlora}")
    print(f"Run name: {run_name}")

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=MODEL_ID,
        max_seq_length=MAX_SEQ_LENGTH,
        load_in_4bit=use_qlora,
        # Unsloth's Gemma 4 guide notes quirks with PLE quantization;
        # start with LoRA (load_in_4bit=False) for a stable baseline.
    )

    model = FastLanguageModel.get_peft_model(
        model,
        r=LORA_R,
        target_modules=TARGET_MODULES,
        lora_alpha=LORA_ALPHA,
        lora_dropout=LORA_DROPOUT,
        bias="none",
        use_gradient_checkpointing="unsloth",
    )

    train_data = load_sft_data("train", task)
    dev_data = load_sft_data("dev", task)
    print(f"Train: {len(train_data):,}  Dev: {len(dev_data):,}")

    from trl import SFTConfig, SFTTrainer

    training_args = SFTConfig(
        output_dir=str(adapter_path),
        num_train_epochs=NUM_EPOCHS,
        per_device_train_batch_size=BATCH_SIZE,
        gradient_accumulation_steps=GRAD_ACCUM_STEPS,
        learning_rate=LEARNING_RATE,
        lr_scheduler_type="cosine",
        warmup_ratio=0.05,
        logging_steps=50,
        eval_strategy="steps",
        eval_steps=200,
        save_strategy="steps",
        save_steps=200,
        save_total_limit=2,
        load_best_model_at_end=True,
        bf16=True,
        report_to="none",
        max_seq_length=MAX_SEQ_LENGTH,
        dataset_text_field="messages",
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_data,
        eval_dataset=dev_data,
        args=training_args,
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
    )
    parser.add_argument(
        "--run-name",
        default=None,
    )
    parser.add_argument(
        "--qlora",
        action="store_true",
        help="Use QLoRA (4-bit quantized base). Default: LoRA (fp16/bf16 base).",
    )
    args = parser.parse_args()
    run_name = args.run_name or f"e4b-{'qlora' if args.qlora else 'lora'}-{args.task}-run1"
    train(args.task, run_name, args.qlora)


if __name__ == "__main__":
    main()
