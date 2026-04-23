# Dataset builder environment setup

Source topic: Phase 0 → Orientation → 0.3 Environment setup in `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`

## Questions and answers

### 1) What does the learning plan want the environment setup to accomplish?
The goal of Phase 0.3 is not “do clever DevOps.” It is to establish a boring, repeatable local environment that can run the dataset-builder scripts without ambiguity.

Concretely, the learner should leave this phase with:
- a project-local Python environment
- the repo dependencies installed
- optional Hugging Face CLI authentication ready for later upload work
- the expected `data/raw/`, `data/interim/`, and `data/processed/` directories present

This is the minimum foundation for Phase 1 onward.

### 2) What does `pyproject.toml` say about the required Python and dependency baseline?
The repo declares `requires-python = ">=3.11"`, so any environment used for the project should be Python 3.11 or newer.

The core dependencies are lightweight data-pipeline packages:
- `datasets`
- `huggingface_hub`
- `jsonlines`
- `tqdm`
- `pydantic`
- `transformers`
- `tokenizers`
- `scikit-learn`
- `numpy`

The `dev` extra adds:
- `pytest`
- `pytest-cov`
- `ruff`
- `mypy`

That means the learning-plan command `pip install -e ".[dev]"` is a sensible canonical setup because it installs both runtime and developer tooling in one step.

### 3) What is the canonical setup sequence from the learning plan?
The plan’s generic sequence is:

1. `python3 -m venv .venv`
2. `source .venv/bin/activate`
3. `pip install -e ".[dev]"`
4. `python -c "import datasets, tqdm, pydantic; print('ok')"`

That path is portable and easy to understand. It is a good default explanation for the learning materials because it matches the repo metadata directly.

### 4) Why does the repo’s practical VPS walkthrough recommend `uv` instead?
The VPS walkthrough documented a machine-specific reality: system `python3` existed, but the system `pip` module was not available under `/usr/bin/python3`. However, `uv` was available.

Because of that, the practical setup decision on the VPS was:

- `uv venv .venv`
- `. .venv/bin/activate`
- `uv pip install ...`

So the right mental model is:
- the learning plan gives the generic Python-venv recipe
- the walkthrough shows the more robust VPS-specific recipe that was actually used here

This is a good example of practical elegance: keep the conceptual setup simple, but adapt the implementation to the host.

### 5) What should a learner do on this repo specifically?
In this repo, the most practical recommendation is:

- if standard `python3 -m venv` and `pip install -e ".[dev]"` work on your machine, use them
- if the host behaves like the VPS described in `docs/data-pipeline-walkthrough.md`, use `uv` to create the venv and install the dependencies

In both cases, the outcome should be the same: a repo-local `.venv` that can import the core dataset-builder dependencies.

### 6) What is the real verification target after environment creation?
The real target is not “the command completed.” It is “the environment can import the libraries the pipeline needs.”

The plan’s import check is a good smoke test:

`python -c "import datasets, tqdm, pydantic; print('ok')"`

Why those imports?
- `datasets` proves Hugging Face dataset loading is available
- `tqdm` proves progress display dependency is available
- `pydantic` proves one of the schema/validation building blocks is available

A stronger practical extension would be to also verify `huggingface_hub`, `numpy`, and `sklearn`, because they appear in the core dependency list too.

### 7) Why is Hugging Face authentication described as optional for early phases?
The plan explicitly notes that the Hermes filtered dataset is public. That means you do not need authentication just to download and inspect it.

Authentication matters later for actions like:
- pushing processed artifacts to the Hugging Face Hub
- publishing the dataset
- updating a dataset card under your own account

So Phase 0.3 is mostly about being ready for later, not about unlocking the current public read path.

### 8) What commands does the learning plan expect for Hugging Face auth?
The plan describes a simple CLI flow:

- `pip install huggingface-hub`
- `huggingface-cli login`
- `huggingface-cli whoami`

Conceptually, this gives the learner a verified token-backed session before the publishing phase.

Even if the exact CLI entrypoint evolves over time, the important operational idea stays the same: install the Hub client, authenticate once, and verify the account context before trying to publish.

### 9) Why does Phase 0.3 also ask for directory creation?
It asks for:

`mkdir -p data/{raw,interim,processed}`

because the repo’s workflow is file-oriented. Later scripts assume these storage layers exist:
- `data/raw/` for downloaded source snapshots
- `data/interim/` for normalized records
- `data/processed/` for train/dev/test outputs and manifests

Creating those directories up front makes the pipeline’s storage contract explicit and removes avoidable friction later.

### 10) What did the documented repo walkthrough confirm about those directories?
The walkthrough used exactly this layered layout. It created `data/interim` and `data/processed`, then wrote:
- `data/raw/hermes_filtered.jsonl`
- `data/interim/hermes_filtered.normalized.jsonl`
- `data/processed/train.jsonl`, `dev.jsonl`, `test.jsonl`, `all.jsonl`

So the directory convention in the learning plan is not theoretical. It matches the actual pipeline outputs described elsewhere in the repo.

### 11) What is the main best-practice lesson of this setup phase?
The lesson is to separate “portable repo contract” from “machine-specific command details.”

The portable contract is:
- Python 3.11+
- local virtual environment
- project dependencies installed
- optional HF auth ready
- pipeline directories present

The machine-specific details are:
- `venv + pip` when the host is normal
- `uv` when the host’s system Python packaging is awkward

That is the elegant way to think about setup: preserve the contract, adapt the tool choice only when reality forces it.

### 12) What should the learner remember before moving into Phase 1?
Remember three things.

1. Setup is only done when imports and directory contracts are verified.
2. Hugging Face login is preparation for publishing, not a blocker for public dataset reading.
3. The environment should stay boring and local. Phase 0.3 is not the place to introduce unnecessary infrastructure.

## Key takeaway for this project
The right Phase 0.3 setup is a small, reproducible repo-local environment that satisfies `pyproject.toml`, can import the pipeline dependencies, and uses the expected `data/` directory layout. On most machines that can be standard `venv + pip`; on this VPS, the documented practical path used `uv` because it was more reliable than the system Python packaging path.

## Sources
- `docs/learning-materials/dataset-builder/dataset_builder_learning_plan.md`
- `pyproject.toml`
- `docs/data-pipeline-walkthrough.md`
- `docs/codebase-baseline.md`
