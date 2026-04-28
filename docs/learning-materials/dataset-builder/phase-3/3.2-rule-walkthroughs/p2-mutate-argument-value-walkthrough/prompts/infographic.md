Create a portrait technical infographic in a dense-modules × pop-laboratory style.

Title: P2 mutate_argument_value
Subtitle: Type-aware argument corruption for bad_tool_arguments

The infographic should look like a polished ML/data-engineering design review board: dark grid background, clean module cards, bright lab accents, crisp typography, large readable headings, minimal body text, and no garbled text.

Content modules:
1. Rule contract
- Keep the same tool
- Corrupt one argument value
- anomaly_type = bad_tool_arguments
- generation_rule = P2

2. Real string sample
- Before: terminal.command = "ls -la"
- After: terminal.command = "sl -la"
- Note: better than literal "_CORRUPTED" suffixes

3. Real integer sample
- Before: read_file.offset = 501
- After: read_file.offset = -498
- Note: same key, wrong retrieval behavior

4. Boolean bug and fix
- Old bad behavior: background = true -> -998
- Fixed behavior: background = true -> false
- Note: Python bool is a subclass of int, so branch order mattered

5. Implementation fix
- Check bool before int
- Use typo/path-like string corruption instead of explicit corruption markers
- Keep the rest of the P2 rule unchanged

6. Verification
- Focused regression tests added
- uv run pytest tests/test_perturbations.py -v
- Result: 12 passed

7. Final takeaway
- Corrupt values in the way the field itself fails
- booleans flip
- file paths become nearby wrong paths
- commands become plausible typos
- integers stay numeric but become bad values

Design constraints:
- portrait 9:16 composition
- very high text legibility
- short labels, chips, arrows, and callout boxes instead of paragraphs
- perfect spelling
- no gibberish
- no fake code walls
- emphasize before/after mutation arrows visually
