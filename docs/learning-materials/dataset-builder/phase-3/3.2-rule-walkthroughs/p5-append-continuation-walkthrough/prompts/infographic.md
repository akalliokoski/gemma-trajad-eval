Create a clean, highly legible technical infographic PNG in a dark bento-dashboard style.

Title: P5 append_continuation
Subtitle: continued_after_sufficient_evidence

Goal:
Explain that the old P5 rule was structurally complete but unrealistic because it always appended a hard-coded search_web call after the answer was already complete. The improved rule now copies an existing assistant/tool pair from the trajectory and prefers lightweight verification-style tools, which makes the anomaly look like one more unnecessary verification pass.

Use exactly 6 large panels with large typography and minimal text.
Do not use paragraphs. Do not use code blocks. Do not use tiny annotations. Do not use filler labels. All spelling must be perfect.

Panel content:
1. Why old P5 felt wrong
- answer already complete
- still appended more work
- hard-coded search_web
- out-of-distribution tool insertion

2. New rule behavior
- find assistant/tool pairs
- prefer lightweight verification pair
- copy exact pair
- append wrap-up assistant step
- bad_step = first appended step

3. Preferred tools
- terminal
- read_file
- browser_snapshot
- search_files
- browser/session-search variants when present

4. Corpus evidence
- eligible: 3182
- preferred choice: 3150 (98.99%)
- fallback: 32 (1.01%)
- minimum source length: 5

5. Top appended tools after fix
- terminal 2146
- read_file 546
- browser_snapshot 314
- search_files 113

6. Verification
- focused P5 tests passed
- perturbations file: 17 passed
- label validation check passed

Footer takeaway:
Structural correctness is not enough. P5 got better when the continuation stayed inside the trace's established tool ecosystem.

Visual direction:
- dark slate or charcoal background
- cyan, teal, and amber accents
- crisp rounded cards
- arrows between before and after concepts
- subtle terminal and file icons
- professional, technical, polished, readable
