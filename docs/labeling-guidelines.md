# Labeling guidelines

Guidelines for annotating trajectories with anomaly labels, step localizations, and anomaly type classifications.

---

## Overview

Each trajectory record requires three labels:

| Label | Type | Description |
|-------|------|-------------|
| `is_anomalous` | `bool` | Whether the trajectory contains any anomalous behavior |
| `bad_step` | `int \| null` | Zero-indexed step number of the first anomalous action (null if normal) |
| `anomaly_type` | `str \| null` | Anomaly subtype from the taxonomy (null if normal) |

---

## What counts as a "step"

Steps are indexed from 0 across the full message list, including system and user messages.

| Index | Role | Example content |
|-------|------|----------------|
| 0 | system | System prompt with tool definitions |
| 1 | user | Task description |
| 2 | assistant | `<think>...</think><tool_call>...</tool_call>` |
| 3 | tool | `<tool_response>...</tool_response>` |
| 4 | assistant | Next reasoning + tool call or final answer |
| ... | ... | ... |

**`bad_step`** refers to the step where the anomalous behavior is **first introduced** — typically an assistant step with a bad reasoning block or bad tool call.

---

## Anomaly taxonomy

### Top-level classes

| Class | Code | When to use |
|-------|------|------------|
| Normal | `normal` | Expert trajectory with no anomalous steps |
| Task failure | `task_failure` | Agent could not or did not complete the task |
| Process inefficiency | `process_inefficiency` | Task completed but via a suboptimal path |
| Unwarranted continuation | `unwarranted_continuation` | Agent continued after task was effectively solved |

### Subtypes

#### `wrong_tool_choice`
- **Top-level:** process_inefficiency
- **Definition:** The agent selected a tool that is semantically inappropriate for the current subtask, even though the tool exists in the schema and the call is syntactically valid.
- **Example:** Using `search_wikipedia` when the task explicitly requires a live web search; using `read_file` when the agent needs to list directory contents.
- **Label:** `bad_step` = step of the bad tool call

#### `bad_tool_arguments`
- **Top-level:** task_failure
- **Definition:** The agent called a valid tool but passed incorrect, malformed, or logically wrong arguments.
- **Example:** Passing `filepath="/tmp/foo"` instead of `filepath="/home/user/foo"`; passing an integer where a string is required.
- **Label:** `bad_step` = step of the bad tool call

#### `skipped_required_step`
- **Top-level:** task_failure
- **Definition:** The agent omitted a necessary tool call or reasoning step that a correct trajectory would include. The final answer is therefore based on incomplete evidence.
- **Example:** Answering a file-content question without ever calling `read_file`; providing a web summary without searching.
- **Label:** `bad_step` = step immediately after the last valid step (where the missing step should have occurred)

#### `repeated_step`
- **Top-level:** process_inefficiency
- **Definition:** The agent duplicated an earlier tool call (same tool, same arguments) without new information that would justify repetition.
- **Example:** Calling `search("capital of France")` twice in sequence; reading the same file twice with no writes in between.
- **Label:** `bad_step` = step of the **second** (duplicated) call

#### `premature_final_answer`
- **Top-level:** task_failure
- **Definition:** The agent produced a final answer before gathering the evidence required to answer correctly. Typically triggered by truncating the reasoning mid-trajectory.
- **Example:** Answering based on only the first tool result when the correct answer requires two lookups; stopping after one search when three were needed.
- **Label:** `bad_step` = step of the premature final answer

#### `continued_after_sufficient_evidence`
- **Top-level:** unwarranted_continuation
- **Definition:** The agent had sufficient evidence to provide a correct final answer but continued calling tools unnecessarily.
- **Example:** Making three additional searches after the correct answer was already in the tool responses.
- **Label:** `bad_step` = first step after the trajectory should have ended

#### `contradicted_tool_result`
- **Top-level:** task_failure
- **Definition:** The agent's conclusion or final answer directly contradicts the content of a tool response.
- **Example:** Tool says "file not found" but agent reports the file was read successfully; tool returns temperature 42°C but agent reports 22°C.
- **Label:** `bad_step` = step of the contradicting final answer

#### `hallucinated_tool`
- **Top-level:** task_failure
- **Definition:** The agent called a tool that does not exist in the provided tool schema.
- **Example:** Calling `send_email()` when no email tool is defined; calling `delete_database_table()` which was never provided.
- **Label:** `bad_step` = step of the hallucinated call

#### `invalid_tool_json`
- **Top-level:** task_failure
- **Definition:** The agent produced a tool call with malformed JSON — either syntactically invalid or missing required fields.
- **Example:** `<tool_call>{"name": "search", "arguments": {broken json}}` ; `{"name": "read_file"}` with no `arguments` field.
- **Label:** `bad_step` = step of the malformed call

#### `unnecessary_replanning`
- **Top-level:** process_inefficiency
- **Definition:** The agent restarted or substantially revised its plan without a valid reason (no new contradicting information arrived).
- **Example:** Agent says "Let me reconsider my approach" after receiving a normal tool response; agent abandons a working strategy mid-execution.
- **Label:** `bad_step` = step of the unjustified replan

---

## Labeling procedure

### Step 1 — Read the full trajectory

Read all messages from system to final assistant response. Do not skim.

### Step 2 — Assess overall task completion

Ask: did the agent complete the task?

- If no → start from `task_failure` subtypes
- If yes → check for inefficiency and continuation subtypes

### Step 3 — Identify the anomalous step

Scan chronologically for the first step that introduces the anomaly. Tool calls are more likely to be the anomalous step than reasoning text, unless the reasoning explicitly states an incorrect plan.

### Step 4 — Assign labels

```
is_anomalous: true/false
bad_step:     <integer index> or null
anomaly_type: <subtype string> or null
```

### Step 5 — Flag edge cases

Mark with `needs_review: true` if:

- Multiple anomaly subtypes apply
- The trajectory is ambiguous (e.g., bad step is unclear)
- The anomaly is borderline (e.g., arguably inefficient but not clearly wrong)
- The perturbation was applied but the result still looks reasonable

---

## Normal trajectory criteria

A trajectory is labeled `normal` if all of the following hold:

1. The agent uses only tools present in the schema
2. All tool arguments are syntactically valid and logically appropriate
3. The agent does not skip steps required to answer the question correctly
4. The agent does not duplicate steps without new information
5. The final answer is consistent with tool responses
6. The agent stops after reaching a correct conclusion

---

## Consistency rules

- `is_anomalous: false` always implies `bad_step: null` and `anomaly_type: null`
- `is_anomalous: true` always implies both `bad_step` and `anomaly_type` are non-null
- `bad_step` must be a valid step index (0 ≤ index < len(trajectory))
- `bad_step` should point to an **assistant** step in almost all cases
- Exceptions: `tool` step can be `bad_step` if a tool response was artificially corrupted (rare)

---

## Synthetic perturbation labels

For synthetically perturbed trajectories, labels are assigned automatically by the perturbation script. The `generation_rule` field records which rule was applied. Manual review should verify that:

- The applied perturbation actually creates the labeled anomaly
- The perturbation is realistic (not trivially detectable)
- The `bad_step` index is correct

---

## Inter-annotator agreement targets

For the manual review set (100–200 samples):

| Label | Target agreement |
|-------|-----------------|
| `is_anomalous` (binary) | ≥ 0.90 Cohen's kappa |
| `anomaly_type` (10-class) | ≥ 0.75 Cohen's kappa |
| `bad_step` (exact match) | ≥ 0.80 |

Resolve disagreements by discussion. If unresolved, mark `needs_review: true` and exclude from training.

---

## Examples

### Example 1 — Normal trajectory

```json
{
  "id": "trace_000001_var_00",
  "is_anomalous": false,
  "bad_step": null,
  "anomaly_type": null
}
```

Justification: Agent searched, read the file, verified the answer, produced a correct response. No tool was misused.

---

### Example 2 — `bad_tool_arguments`

Trajectory excerpt (step 4):
```json
{"role": "assistant", "content": "<tool_call>{\"name\": \"read_file\", \"arguments\": {\"path\": \"/tmp/notes\"}}</tool_call>"}
```

The actual file is at `/home/user/notes`. The agent passed the wrong path.

```json
{
  "id": "trace_000045_var_01",
  "is_anomalous": true,
  "bad_step": 4,
  "anomaly_type": "bad_tool_arguments"
}
```

---

### Example 3 — `skipped_required_step`

The task requires reading a configuration file before answering. The agent answers directly in step 3 without calling `read_file`.

```json
{
  "id": "trace_000089_var_03",
  "is_anomalous": true,
  "bad_step": 3,
  "anomaly_type": "skipped_required_step"
}
```

---

### Example 4 — `contradicted_tool_result`

Tool response at step 5: `{"result": "temperature: 42°C"}`.  
Agent final answer at step 6: "The temperature is 22 degrees Celsius."

```json
{
  "id": "trace_000112_var_02",
  "is_anomalous": true,
  "bad_step": 6,
  "anomaly_type": "contradicted_tool_result"
}
```
