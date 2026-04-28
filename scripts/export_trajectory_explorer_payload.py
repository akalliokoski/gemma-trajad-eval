from __future__ import annotations

import argparse
from pathlib import Path

from dataset_builder.trajectory_explorer_payload import DEFAULT_OUTPUT_DIR, REPO_ROOT, export_payload_bundle


def main() -> None:
    parser = argparse.ArgumentParser(description="Export payloads for the static trajectory explorer.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=REPO_ROOT,
        help="Repository root containing data/processed and apps/trajectory_explorer/",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where JSON payloads and payload_bundle.js should be written.",
    )
    args = parser.parse_args()

    written = export_payload_bundle(repo_root=args.repo_root, output_dir=args.output_dir)
    for name, path in written.items():
        print(f"{name:10s} -> {path}")


if __name__ == "__main__":
    main()
