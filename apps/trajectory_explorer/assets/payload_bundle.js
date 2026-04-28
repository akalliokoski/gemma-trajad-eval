window.__TRAJAD_EXPLORER_DATA__ = {
  "overview": {
    "generated_at": "2026-04-27T10:14:10.336168Z",
    "project": {
      "name": "gemma-trajad-eval",
      "tagline": "Hermes-first trajectory anomaly engineering lab",
      "reference_visualization": {
        "github": "https://github.com/ArkAung/interactive-turboquant",
        "live_demo": "https://arkaung.github.io/interactive-turboquant/"
      }
    },
    "counts": {
      "raw_traces": 3679,
      "processed_examples": 71429,
      "normal_examples": 7358,
      "anomalous_examples": 64071,
      "train": 53557,
      "dev": 7154,
      "test": 10718
    },
    "anomaly_class_distribution": [
      {
        "id": "process_inefficiency",
        "count": 14716
      },
      {
        "id": "task_failure",
        "count": 42991
      },
      {
        "id": "unwarranted_continuation",
        "count": 6364
      }
    ],
    "taxonomy": [
      {
        "id": "wrong_tool_choice",
        "label": "Wrong Tool Choice",
        "anomaly_class": "process_inefficiency",
        "count": 7358
      },
      {
        "id": "bad_tool_arguments",
        "label": "Bad Tool Arguments",
        "anomaly_class": "task_failure",
        "count": 7279
      },
      {
        "id": "skipped_required_step",
        "label": "Skipped Required Step",
        "anomaly_class": "task_failure",
        "count": 14674
      },
      {
        "id": "repeated_step",
        "label": "Repeated Step",
        "anomaly_class": "process_inefficiency",
        "count": 7358
      },
      {
        "id": "premature_final_answer",
        "label": "Premature Final Answer",
        "anomaly_class": "task_failure",
        "count": 7316
      },
      {
        "id": "continued_after_sufficient_evidence",
        "label": "Continued After Sufficient Evidence",
        "anomaly_class": "unwarranted_continuation",
        "count": 6364
      },
      {
        "id": "contradicted_tool_result",
        "label": "Contradicted Tool Result",
        "anomaly_class": "task_failure",
        "count": 6364
      },
      {
        "id": "hallucinated_tool",
        "label": "Hallucinated Tool",
        "anomaly_class": "task_failure",
        "count": 0
      },
      {
        "id": "invalid_tool_json",
        "label": "Invalid Tool JSON",
        "anomaly_class": "task_failure",
        "count": 7358
      },
      {
        "id": "unnecessary_replanning",
        "label": "Unnecessary Replanning",
        "anomaly_class": "process_inefficiency",
        "count": 0
      }
    ],
    "taxonomy_mode": "observed-from-processed-all-jsonl",
    "execution_topology": [
      {
        "node": "vps",
        "role": "control-plane",
        "summary": "Hermes planning, docs, orchestration, and lightweight automation"
      },
      {
        "node": "apple-silicon-mac",
        "role": "bounded-compute-worker",
        "summary": "Preferred small/medium fine-tuning and local validation tier"
      },
      {
        "node": "modal",
        "role": "future-heavy-gpu-tier",
        "summary": "Deferred destination for truly heavy training or inference jobs"
      }
    ]
  },
  "samples": {
    "selected_ids": {
      "normal": "trace_003581_var_00",
      "anomalous": "c9978209-d7a5-41f3-9cab-0923a691d3da_var_02"
    },
    "samples": [
      {
        "id": "trace_003581_var_00",
        "sample_kind": "normal",
        "source_trace_id": "4382bae6-a55f-4ada-a042-06dcda54eda7",
        "split": "train",
        "is_anomalous": false,
        "anomaly_type": null,
        "anomaly_class": null,
        "bad_step": null,
        "generation_rule": null,
        "message_count": 11,
        "window": {
          "start": 0,
          "end": 11
        },
        "messages": [
          {
            "absolute_index": 0,
            "role": "system",
            "tool_name": null,
            "has_tool_call": true,
            "has_tool_response": true,
            "content_excerpt": "You are a function calling AI model. You are provided with function signatures within <tools> </tools> XML tags. You may call one or more functions to assist with the user query. If available tools are not relevant in assisting with user query, just respond in natural conversati\u2026"
          },
          {
            "absolute_index": 1,
            "role": "user",
            "tool_name": null,
            "has_tool_call": false,
            "has_tool_response": false,
            "content_excerpt": "Create documentation in Markdown for the deployment process with troubleshooting guide."
          },
          {
            "absolute_index": 2,
            "role": "assistant",
            "tool_name": "search_files",
            "has_tool_call": true,
            "has_tool_response": false,
            "content_excerpt": "<think> The user wants me to create documentation in Markdown for a deployment process with a troubleshooting guide. However, I don't know what kind of project this is for, what technologies are involved, or what the deployment process looks like. Let me first explore the curren\u2026"
          },
          {
            "absolute_index": 3,
            "role": "tool",
            "tool_name": null,
            "has_tool_call": false,
            "has_tool_response": true,
            "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.search_files:0\", \"name\": \"search_files\", \"content\": {\"total_count\": 0}} </tool_response> <tool_response> {\"tool_call_id\": \"functions.search_files:1\", \"name\": \"search_files\", \"content\": {\"total_count\": 0}} </tool_response>"
          },
          {
            "absolute_index": 4,
            "role": "assistant",
            "tool_name": "terminal",
            "has_tool_call": true,
            "has_tool_response": false,
            "content_excerpt": "<think> Let me check if there are any files in the current directory at all. </think> <tool_call> {\"name\": \"terminal\", \"arguments\": {\"command\": \"ls -la\"}} </tool_call>"
          },
          {
            "absolute_index": 5,
            "role": "tool",
            "tool_name": null,
            "has_tool_call": false,
            "has_tool_response": true,
            "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.terminal:2\", \"name\": \"terminal\", \"content\": {\"output\": \"total 8\\ndrwxrwxr-x 2 2013 2013 4096 Mar 27 18:48 .\\ndrwxr-xr-x 1 root root 4096 Mar 27 18:48 ..\", \"exit_code\": 0, \"error\": null}} </tool_response>"
          },
          {
            "absolute_index": 6,
            "role": "assistant",
            "tool_name": "write_file",
            "has_tool_call": true,
            "has_tool_response": false,
            "content_excerpt": "<think> The workspace is empty. Since there's no existing project structure, I'll create a comprehensive deployment documentation guide that can be adapted for various types of applications (web apps, APIs, microservices, etc.). This will include Docker, Kubernetes, cloud deploy\u2026"
          },
          {
            "absolute_index": 7,
            "role": "tool",
            "tool_name": null,
            "has_tool_call": false,
            "has_tool_response": true,
            "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.write_file:3\", \"name\": \"write_file\", \"content\": {\"bytes_written\": 39106, \"dirs_created\": false}} </tool_response>"
          },
          {
            "absolute_index": 8,
            "role": "assistant",
            "tool_name": "read_file",
            "has_tool_call": true,
            "has_tool_response": false,
            "content_excerpt": "<think> I need to rapidly create a practical deployment documentation file and check its actual content. First, I need to confirm whether it was successfully created and check if the file contents meet the requirements. </think> <tool_call> {\"name\": \"read_file\", \"arguments\": {\"p\u2026"
          },
          {
            "absolute_index": 9,
            "role": "tool",
            "tool_name": null,
            "has_tool_call": false,
            "has_tool_response": true,
            "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.read_file:4\", \"name\": \"read_file\", \"content\": {\"content\": \" 1|# Deployment Guide\\n 2|\\n 3|A comprehensive guide for deploying applications across various platforms and environments.\\n 4|\\n 5|## Table of Contents\\n 6|\\n 7|- [Overview](#\u2026"
          },
          {
            "absolute_index": 10,
            "role": "assistant",
            "tool_name": null,
            "has_tool_call": false,
            "has_tool_response": false,
            "content_excerpt": "<think> The documentation has been created successfully. The file is quite comprehensive with 1651 lines. Let me provide a summary of what's been created. </think> I've created a comprehensive deployment documentation file at `DEPLOYMENT.md`. Here's what's included: ## \ud83d\udcc4 **DEPLO\u2026"
          }
        ],
        "diff_hints": {
          "focus_indexes": [
            5
          ],
          "changed_message_indexes": []
        }
      },
      {
        "id": "c9978209-d7a5-41f3-9cab-0923a691d3da_var_02",
        "sample_kind": "anomalous",
        "source_trace_id": "c9978209-d7a5-41f3-9cab-0923a691d3da",
        "split": "train",
        "is_anomalous": true,
        "anomaly_type": "bad_tool_arguments",
        "anomaly_class": "task_failure",
        "bad_step": 16,
        "generation_rule": "P2",
        "message_count": 25,
        "window": {
          "start": 10,
          "end": 22
        },
        "messages": [
          {
            "absolute_index": 10,
            "role": "assistant",
            "tool_name": "terminal",
            "has_tool_call": true,
            "has_tool_response": false,
            "content_excerpt": "<think> I need to find the current working directory and run from there: </think> <tool_call> {\"name\": \"terminal\", \"arguments\": {\"command\": \"pwd && ls -la database_analysis.ipynb\", \"timeout\": 10}} </tool_call>"
          },
          {
            "absolute_index": 11,
            "role": "tool",
            "tool_name": null,
            "has_tool_call": false,
            "has_tool_response": true,
            "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.terminal:4\", \"name\": \"terminal\", \"content\": {\"output\": \"/root\\n-rw-r--r-- 1 root root 28250 Mar 27 18:29 database_analysis.ipynb\", \"exit_code\": 0, \"error\": null}} </tool_response>"
          },
          {
            "absolute_index": 12,
            "role": "assistant",
            "tool_name": "terminal",
            "has_tool_call": true,
            "has_tool_response": false,
            "content_excerpt": "<think> The notebook is in the current directory. Let me execute it. I need to be more specific about the matplotlib backend for headless execution. </think> <tool_call> {\"name\": \"terminal\", \"arguments\": {\"command\": \"jupyter nbconvert --to notebook --execute database_analysis.ip\u2026"
          },
          {
            "absolute_index": 13,
            "role": "tool",
            "tool_name": null,
            "has_tool_call": false,
            "has_tool_response": true,
            "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.terminal:5\", \"name\": \"terminal\", \"content\": {\"output\": \"[NbConvertApp] Converting notebook database_analysis.ipynb to notebook\\nTraceback (most recent call last):\\n File \\\"/usr/local/bin/jupyter-nbconvert\\\", line 6, in <module>\\n sys.e\u2026"
          },
          {
            "absolute_index": 14,
            "role": "assistant",
            "tool_name": "patch",
            "has_tool_call": true,
            "has_tool_response": false,
            "content_excerpt": "<think> There's a bug in the plotting code - the x variable was reused from a previous subplot and has 6 elements instead of 3. Let me fix the notebook: </think> Let me fix the plotting bug in the notebook: <tool_call> {\"name\": \"patch\", \"arguments\": {\"mode\": \"replace\", \"path\": \"\u2026"
          },
          {
            "absolute_index": 15,
            "role": "tool",
            "tool_name": null,
            "has_tool_call": false,
            "has_tool_response": true,
            "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.patch:6\", \"name\": \"patch\", \"content\": {\"success\": true, \"diff\": \"--- a/database_analysis.ipynb\\n+++ b/database_analysis.ipynb\\n@@ -291,14 +291,15 @@\\n \\\"ax2.set_xticklabels(categories, rotation=45, ha='right')\\\\n\\\",\\n \\\"ax2.legend()\\\\n\u2026"
          },
          {
            "absolute_index": 16,
            "role": "assistant",
            "tool_name": "read_file",
            "has_tool_call": true,
            "has_tool_response": false,
            "content_excerpt": "<think> The patch didn't apply correctly. Let me read the file to see what happened and fix it properly. </think> <tool_call>{\"name\": \"read_file\", \"arguments\": {\"path\": \"database_analysis.ipynb_CORRUPTED\", \"offset\": 270, \"limit\": 50}}</tool_call>"
          },
          {
            "absolute_index": 17,
            "role": "tool",
            "tool_name": null,
            "has_tool_call": false,
            "has_tool_response": true,
            "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.read_file:7\", \"name\": \"read_file\", \"content\": {\"content\": \" 270| \\\" managed_medium.monthly_storage_cost_per_gb * managed_medium.monthly_storage_gb,\\\\n\\\",\\n 271| \\\" managed_medium.monthly_data_transfer_cost,\\\\n\\\",\\n 272| \\\" managed_medi\u2026"
          },
          {
            "absolute_index": 18,
            "role": "assistant",
            "tool_name": "write_file",
            "has_tool_call": true,
            "has_tool_response": false,
            "content_excerpt": "<think> The patch didn't apply correctly. Let me rewrite the file with proper Python syntax instead of trying to patch the JSON notebook. I'll create a Python script instead that generates the analysis: </think> _transfer <tool_call> {\"name\": \"write_file\", \"arguments\": {\"path\":\u2026"
          },
          {
            "absolute_index": 19,
            "role": "tool",
            "tool_name": null,
            "has_tool_call": false,
            "has_tool_response": true,
            "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.write_file:8\", \"name\": \"write_file\", \"content\": {\"bytes_written\": 21993, \"dirs_created\": false}} </tool_response>"
          },
          {
            "absolute_index": 20,
            "role": "assistant",
            "tool_name": "terminal",
            "has_tool_call": true,
            "has_tool_response": false,
            "content_excerpt": "<think> I've created a Python script with a comprehensive analysis. Now let me run it to generate all the outputs and visualizations. </think> <tool_call> {\"name\": \"terminal\", \"arguments\": {\"command\": \"python database_analysis.py 2>&1\", \"timeout\": 60}} </tool_call>"
          },
          {
            "absolute_index": 21,
            "role": "tool",
            "tool_name": null,
            "has_tool_call": false,
            "has_tool_response": true,
            "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.terminal:9\", \"name\": \"terminal\", \"content\": {\"output\": \"======================================================================\\nMANAGED VS. SELF-HOSTED DATABASE ANALYSIS\\n================================================================\u2026"
          }
        ],
        "diff_hints": {
          "focus_indexes": [
            16
          ],
          "changed_message_indexes": [
            16
          ]
        },
        "source_pair": {
          "id": "trace_003558_var_00",
          "message_count": 25,
          "messages": [
            {
              "absolute_index": 10,
              "role": "assistant",
              "tool_name": "terminal",
              "has_tool_call": true,
              "has_tool_response": false,
              "content_excerpt": "<think> I need to find the current working directory and run from there: </think> <tool_call> {\"name\": \"terminal\", \"arguments\": {\"command\": \"pwd && ls -la database_analysis.ipynb\", \"timeout\": 10}} </tool_call>"
            },
            {
              "absolute_index": 11,
              "role": "tool",
              "tool_name": null,
              "has_tool_call": false,
              "has_tool_response": true,
              "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.terminal:4\", \"name\": \"terminal\", \"content\": {\"output\": \"/root\\n-rw-r--r-- 1 root root 28250 Mar 27 18:29 database_analysis.ipynb\", \"exit_code\": 0, \"error\": null}} </tool_response>"
            },
            {
              "absolute_index": 12,
              "role": "assistant",
              "tool_name": "terminal",
              "has_tool_call": true,
              "has_tool_response": false,
              "content_excerpt": "<think> The notebook is in the current directory. Let me execute it. I need to be more specific about the matplotlib backend for headless execution. </think> <tool_call> {\"name\": \"terminal\", \"arguments\": {\"command\": \"jupyter nbconvert --to notebook --execute database_analysis.ip\u2026"
            },
            {
              "absolute_index": 13,
              "role": "tool",
              "tool_name": null,
              "has_tool_call": false,
              "has_tool_response": true,
              "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.terminal:5\", \"name\": \"terminal\", \"content\": {\"output\": \"[NbConvertApp] Converting notebook database_analysis.ipynb to notebook\\nTraceback (most recent call last):\\n File \\\"/usr/local/bin/jupyter-nbconvert\\\", line 6, in <module>\\n sys.e\u2026"
            },
            {
              "absolute_index": 14,
              "role": "assistant",
              "tool_name": "patch",
              "has_tool_call": true,
              "has_tool_response": false,
              "content_excerpt": "<think> There's a bug in the plotting code - the x variable was reused from a previous subplot and has 6 elements instead of 3. Let me fix the notebook: </think> Let me fix the plotting bug in the notebook: <tool_call> {\"name\": \"patch\", \"arguments\": {\"mode\": \"replace\", \"path\": \"\u2026"
            },
            {
              "absolute_index": 15,
              "role": "tool",
              "tool_name": null,
              "has_tool_call": false,
              "has_tool_response": true,
              "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.patch:6\", \"name\": \"patch\", \"content\": {\"success\": true, \"diff\": \"--- a/database_analysis.ipynb\\n+++ b/database_analysis.ipynb\\n@@ -291,14 +291,15 @@\\n \\\"ax2.set_xticklabels(categories, rotation=45, ha='right')\\\\n\\\",\\n \\\"ax2.legend()\\\\n\u2026"
            },
            {
              "absolute_index": 16,
              "role": "assistant",
              "tool_name": "read_file",
              "has_tool_call": true,
              "has_tool_response": false,
              "content_excerpt": "<think> The patch didn't apply correctly. Let me read the file to see what happened and fix it properly. </think> <tool_call> {\"name\": \"read_file\", \"arguments\": {\"path\": \"database_analysis.ipynb\", \"offset\": 270, \"limit\": 50}} </tool_call>"
            },
            {
              "absolute_index": 17,
              "role": "tool",
              "tool_name": null,
              "has_tool_call": false,
              "has_tool_response": true,
              "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.read_file:7\", \"name\": \"read_file\", \"content\": {\"content\": \" 270| \\\" managed_medium.monthly_storage_cost_per_gb * managed_medium.monthly_storage_gb,\\\\n\\\",\\n 271| \\\" managed_medium.monthly_data_transfer_cost,\\\\n\\\",\\n 272| \\\" managed_medi\u2026"
            },
            {
              "absolute_index": 18,
              "role": "assistant",
              "tool_name": "write_file",
              "has_tool_call": true,
              "has_tool_response": false,
              "content_excerpt": "<think> The patch didn't apply correctly. Let me rewrite the file with proper Python syntax instead of trying to patch the JSON notebook. I'll create a Python script instead that generates the analysis: </think> _transfer <tool_call> {\"name\": \"write_file\", \"arguments\": {\"path\":\u2026"
            },
            {
              "absolute_index": 19,
              "role": "tool",
              "tool_name": null,
              "has_tool_call": false,
              "has_tool_response": true,
              "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.write_file:8\", \"name\": \"write_file\", \"content\": {\"bytes_written\": 21993, \"dirs_created\": false}} </tool_response>"
            },
            {
              "absolute_index": 20,
              "role": "assistant",
              "tool_name": "terminal",
              "has_tool_call": true,
              "has_tool_response": false,
              "content_excerpt": "<think> I've created a Python script with a comprehensive analysis. Now let me run it to generate all the outputs and visualizations. </think> <tool_call> {\"name\": \"terminal\", \"arguments\": {\"command\": \"python database_analysis.py 2>&1\", \"timeout\": 60}} </tool_call>"
            },
            {
              "absolute_index": 21,
              "role": "tool",
              "tool_name": null,
              "has_tool_call": false,
              "has_tool_response": true,
              "content_excerpt": "<tool_response> {\"tool_call_id\": \"functions.terminal:9\", \"name\": \"terminal\", \"content\": {\"output\": \"======================================================================\\nMANAGED VS. SELF-HOSTED DATABASE ANALYSIS\\n================================================================\u2026"
            }
          ]
        }
      }
    ]
  },
  "training": {
    "training_stages": [
      {
        "stage_id": "prepare-binary-sft",
        "label": "Prepare binary SFT data",
        "script": "training/prepare_sft_data.py --task binary",
        "input_artifact": "data/processed/train.jsonl",
        "output_artifact": "data/processed/train_sft_binary.jsonl"
      },
      {
        "stage_id": "train-e2b-binary",
        "label": "Train Gemma 4 E2B binary adapter",
        "script": "training/train_e2b.py --task binary",
        "input_artifact": "data/processed/train_sft_binary.jsonl",
        "output_artifact": "outputs/adapters/e2b-sft-binary-run1/final"
      },
      {
        "stage_id": "evaluate-run",
        "label": "Evaluate predictions against held-out data",
        "script": "training/evaluate.py --predictions <file> --ground-truth data/processed/test.jsonl",
        "input_artifact": "outputs/reports/predictions.jsonl",
        "output_artifact": "outputs/reports/eval_results.json"
      }
    ],
    "task_modes": [
      {
        "task": "binary",
        "train_rows": 13767,
        "dev_rows": 1833,
        "test_rows": 2755,
        "prompt_file": "prompts/anomaly_binary.txt"
      },
      {
        "task": "localize",
        "train_rows": 0,
        "dev_rows": 0,
        "test_rows": 0,
        "prompt_file": "prompts/anomaly_localize.txt"
      },
      {
        "task": "joint",
        "train_rows": 0,
        "dev_rows": 0,
        "test_rows": 0,
        "prompt_file": "prompts/anomaly_joint.txt"
      }
    ],
    "run_notes": [
      "E2B is the primary local-first fine-tuning target.",
      "E4B remains an optional comparison path for later runs.",
      "RL/GRPO belongs to a later phase after SFT and evaluation are stable."
    ]
  },
  "evaluation": {
    "split_counts": {
      "train": 53557,
      "dev": 7154,
      "test": 10718
    },
    "normal_examples": 7358,
    "anomalous_examples": 64071,
    "anomaly_type_distribution": [
      {
        "id": "wrong_tool_choice",
        "label": "Wrong Tool Choice",
        "anomaly_class": "process_inefficiency",
        "count": 7358
      },
      {
        "id": "bad_tool_arguments",
        "label": "Bad Tool Arguments",
        "anomaly_class": "task_failure",
        "count": 7279
      },
      {
        "id": "skipped_required_step",
        "label": "Skipped Required Step",
        "anomaly_class": "task_failure",
        "count": 14674
      },
      {
        "id": "repeated_step",
        "label": "Repeated Step",
        "anomaly_class": "process_inefficiency",
        "count": 7358
      },
      {
        "id": "premature_final_answer",
        "label": "Premature Final Answer",
        "anomaly_class": "task_failure",
        "count": 7316
      },
      {
        "id": "continued_after_sufficient_evidence",
        "label": "Continued After Sufficient Evidence",
        "anomaly_class": "unwarranted_continuation",
        "count": 6364
      },
      {
        "id": "contradicted_tool_result",
        "label": "Contradicted Tool Result",
        "anomaly_class": "task_failure",
        "count": 6364
      },
      {
        "id": "hallucinated_tool",
        "label": "Hallucinated Tool",
        "anomaly_class": "task_failure",
        "count": 0
      },
      {
        "id": "invalid_tool_json",
        "label": "Invalid Tool JSON",
        "anomaly_class": "task_failure",
        "count": 7358
      },
      {
        "id": "unnecessary_replanning",
        "label": "Unnecessary Replanning",
        "anomaly_class": "process_inefficiency",
        "count": 0
      }
    ],
    "anomaly_type_distribution_mode": "observed-from-processed-all-jsonl",
    "perturbation_rules": [
      {
        "eligible": 3679,
        "failed": 509,
        "failure_examples": [
          {
            "id": "trace_000007_var_00",
            "source_trace_id": "930977e3-cb4e-4bcd-8218-c717389c4c14",
            "tool_name": "clarify"
          },
          {
            "id": "trace_000008_var_00",
            "source_trace_id": "e0faf24b-e135-412f-b89d-c90b263e677b",
            "tool_name": "session_search"
          },
          {
            "id": "trace_000009_var_00",
            "source_trace_id": "66890ddc-faa5-4ca2-9f80-f751e2f8eed3",
            "tool_name": "terminal"
          },
          {
            "id": "trace_000011_var_00",
            "source_trace_id": "19be0b4f-b8d3-48f9-af88-6d22eda39812",
            "tool_name": "skills_list"
          },
          {
            "id": "trace_000016_var_00",
            "source_trace_id": "268a8715-aca4-4edd-908c-60feff040be7",
            "tool_name": "execute_code"
          }
        ],
        "ineligible": 0,
        "rule_name": "p1_replace_tool_choice",
        "succeeded": 3170,
        "success_rate": 0.8616
      },
      {
        "eligible": 3678,
        "failed": 32,
        "failure_examples": [
          {
            "id": "trace_000069_var_00",
            "source_trace_id": "ad251fb7-3f10-442e-b23d-5053d0668786",
            "tool_name": "todo"
          },
          {
            "id": "trace_000102_var_00",
            "source_trace_id": "b6097761-c1fb-4954-b269-8e29037d73fb",
            "tool_name": "skills_list"
          },
          {
            "id": "trace_000107_var_00",
            "source_trace_id": "deca8b65-9862-4948-a034-cd9ded553977",
            "tool_name": "skills_list"
          },
          {
            "id": "trace_000163_var_00",
            "source_trace_id": "c4915afa-ef10-4ea0-bcd1-378f89f436ec",
            "tool_name": "session_search"
          },
          {
            "id": "trace_000166_var_00",
            "source_trace_id": "f0b0a404-bc8b-4c89-ae77-31ecb67c8cc5",
            "tool_name": "todo"
          }
        ],
        "ineligible": 1,
        "rule_name": "p2_mutate_argument_value",
        "succeeded": 3646,
        "success_rate": 0.9913
      },
      {
        "eligible": 3679,
        "failed": 0,
        "failure_examples": [],
        "ineligible": 0,
        "rule_name": "p3_remove_step_pair",
        "succeeded": 3679,
        "success_rate": 1.0
      },
      {
        "eligible": 3679,
        "failed": 0,
        "failure_examples": [],
        "ineligible": 0,
        "rule_name": "p4_duplicate_tool_step",
        "succeeded": 3679,
        "success_rate": 1.0
      },
      {
        "eligible": 3182,
        "failed": 0,
        "failure_examples": [],
        "ineligible": 497,
        "rule_name": "p5_append_continuation",
        "succeeded": 3182,
        "success_rate": 1.0
      },
      {
        "eligible": 3182,
        "failed": 0,
        "failure_examples": [],
        "ineligible": 497,
        "rule_name": "p6_contradict_final_answer",
        "succeeded": 3182,
        "success_rate": 1.0
      },
      {
        "eligible": 3658,
        "failed": 0,
        "failure_examples": [],
        "ineligible": 21,
        "rule_name": "p7_truncate_before_decision",
        "succeeded": 3658,
        "success_rate": 1.0
      },
      {
        "eligible": 3658,
        "failed": 0,
        "failure_examples": [],
        "ineligible": 21,
        "rule_name": "p8_swap_dependent_steps",
        "succeeded": 3658,
        "success_rate": 1.0
      },
      {
        "eligible": 3679,
        "failed": 0,
        "failure_examples": [],
        "ineligible": 0,
        "rule_name": "p9_invalid_tool_json",
        "succeeded": 3679,
        "success_rate": 1.0
      }
    ],
    "reported_runs": [],
    "notes": [
      "Anomaly-type counts are measured from data/processed/all.jsonl and cover the full currently exported taxonomy.",
      "No evaluation report JSON artifacts are committed yet, so this panel emphasizes measured dataset distributions and rule coverage rather than model metrics."
    ]
  }
};
