# Structured infographic content

Title:
- P1 realism upgrade

Subtitle:
- Remove fake tool names, keep believable confusion

Metric cards:
- Records checked: 3,679
- Success before: 3,679
- Fake `_v2` before: 509
- Success after: 3,170
- Fake `_v2` after: 0

Example card 1:
- Label: terminal
- Before: command -> execute_code with shell-shaped args
- After: command -> execute_code with code arg

Example card 2:
- Label: search_files
- Before: search args copied across
- After: search args become shell command

Policy card:
- Old: always mutate
- New: skip unmapped tools
- Principle: precision over recall

Remaining gaps card:
- browser_navigate 126
- patch 114
- browser_click 70
- process 32
- browser_vision 29

Footer takeaway:
- Removed 509 synthetic cases without hurting curated cases
