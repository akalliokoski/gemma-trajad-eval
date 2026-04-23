#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys

root = Path('/home/hermes/gemma-trajad-eval/docs/learning-materials/dataset-builder/phase-0/0.4-implementation-synthesis/dataset-builder-phase-0-improvements-podcast-playlist/episodes')
helper = '/opt/hermes/scripts/make-podcast.py'
python = '/home/hermes/.venvs/podcast-pipeline/bin/python'
for transcript in sorted(root.glob('*/podcast-transcript.json')):
    data = json.loads(transcript.read_text(encoding='utf-8'))
    title = data['title']
    slug = data['episode_slug']
    out = Path('/data/audiobookshelf/podcasts/profiles/gemma') / data['show_slug'] / f'{slug}.mp3'
    if out.exists():
        print(f'SKIP {slug} {out}')
        continue
    cmd = [python, helper, '--title', title, '--transcript', str(transcript), '--profile', 'gemma', '--skip-notify']
    print('RUN', slug)
    proc = subprocess.run(cmd)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    print(f'DONE {slug} {out}')
print('ALL_DONE')
