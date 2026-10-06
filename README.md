# Srinivasan

**Backend development · Machine learning · Agentic AI & LLMs**

Computer Science undergraduate at KIIT (2024–2028). I work primarily with **Python, Java, and Spring Boot**. These repositories cover task management, financial reconciliation, computer vision, tabular ML, and agents that execute code.

[GitHub repositories](https://github.com/S-Srinivasan-06?tab=repositories) &nbsp; · &nbsp; [LinkedIn](https://www.linkedin.com/in/s-srinivasan-a69006315/) &nbsp; · &nbsp; [Email](mailto:srinivasansubr2006@gmail.com)

## Featured project

### [Taskflow Local](https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend)

An offline Windows task manager with on-device LLM inference. Natural-language and screenshot input become task operations that are validated and presented for review before anything is saved.

- Local Gemma inference through llama.cpp, with structured action schemas and retry handling.
- SQLite persistence, desktop reminders, and a system tray.
- A review step between model output and changes to task data.

`Local LLMs` `llama.cpp` `Gemma` `React` `SQLite`

[Source](https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend) &nbsp; · &nbsp; [Windows release](https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend/releases/latest) &nbsp; · &nbsp; [Inference harness](https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend/blob/main/src/model/modelService.ts) &nbsp; · &nbsp; [Action validation](https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend/blob/main/src/model/actionSchema.ts)

<a href="https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend/blob/main/docs/screenshots/forest-2026-10-05.png">
  <img src="https://raw.githubusercontent.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend/main/docs/screenshots/forest-2026-10-05.png" width="320" alt="Taskflow Local interface preview with example tasks, a timeline, and local model controls." />
</a>

## Backend engineering

### [Taskflow](https://github.com/S-Srinivasan-06/Taskflow)

A web task manager built on Spring Boot and PostgreSQL, with a React interface. The backend checks task ownership, scopes sessions to users, and uses optimistic concurrency to handle conflicting updates. Integration tests exercise authentication and isolation boundaries.

`Java` `Spring Boot` `PostgreSQL` `React` `Docker`

[Source](https://github.com/S-Srinivasan-06/Taskflow) &nbsp; · &nbsp; [Task service](https://github.com/S-Srinivasan-06/Taskflow/blob/main/src/main/java/com/taskflow/service/TaskService.java) &nbsp; · &nbsp; [Integration tests](https://github.com/S-Srinivasan-06/Taskflow/blob/main/src/test/java/com/taskflow/security/AuthOwnershipIntegrationTest.java)

### [Financial Reconciliation Agent](https://github.com/S-Srinivasan-06/Razorpay-Buildathon-webui-and-cli)

A Python workbench for matching sales, gateway ledgers, and bank statements. The resumable pipeline handles fee rules, exception review, and double-entry journal exports. A web console and CLI expose progress, with WebSocket telemetry and a persistent SHA-256 audit chain.

`Python` `FastAPI` `Pandas` `Pydantic` `WebSockets`

[Source](https://github.com/S-Srinivasan-06/Razorpay-Buildathon-webui-and-cli) &nbsp; · &nbsp; [Pipeline](https://github.com/S-Srinivasan-06/Razorpay-Buildathon-webui-and-cli/blob/main/src/app/pipeline.py) &nbsp; · &nbsp; [Audit ledger](https://github.com/S-Srinivasan-06/Razorpay-Buildathon-webui-and-cli/blob/main/src/app/core/audit.py)

## Machine learning

### [CrowdShield](https://github.com/S-Srinivasan-06/CrowdShield)

A computer vision pipeline combining head detection, motion tracking, and crowd density analysis. The browser dashboard supports editable regions of interest and archived runs. Threaded processing connects the tracking engine to live SSE telemetry and MJPEG video streams.

`Python` `OpenCV` `OpenVINO` `NumPy` `YOLOv8`

[Source](https://github.com/S-Srinivasan-06/CrowdShield) &nbsp; · &nbsp; [Tracking and density engine](https://github.com/S-Srinivasan-06/CrowdShield/blob/main/src/features.py)

### [Customer Churn Prediction](https://github.com/S-Srinivasan-06/Customer-Churn-Prediction-with-LightGBM)

A LightGBM classification workflow for the IBM Telco churn dataset. It includes domain feature engineering, stratified cross-validation, training-fold scaling and SMOTE, and decision-threshold selection from out-of-fold predictions. A separate Optuna script explores model hyperparameters.

`Python` `LightGBM` `scikit-learn` `Pandas` `SMOTE` `Optuna`

[Source](https://github.com/S-Srinivasan-06/Customer-Churn-Prediction-with-LightGBM) &nbsp; · &nbsp; [Training and evaluation](https://github.com/S-Srinivasan-06/Customer-Churn-Prediction-with-LightGBM/blob/main/src/model.py) &nbsp; · &nbsp; [Hyperparameter search](https://github.com/S-Srinivasan-06/Customer-Churn-Prediction-with-LightGBM/blob/main/optuna_finetuner/finetune.py)

## Agentic AI & LLMs

### [Sandman](https://github.com/S-Srinivasan-06/sandman-ai-sandbox)

An agent that writes, runs, tests, and packages code inside Docker workspaces. LangGraph coordinates execution, inspection, retries, and cleanup. MCP tools provide workspace operations, while model routing supports local and hosted providers.

`Python` `LangGraph` `MCP` `Docker` `Ollama`

[Source](https://github.com/S-Srinivasan-06/sandman-ai-sandbox) &nbsp; · &nbsp; [Agent graph](https://github.com/S-Srinivasan-06/sandman-ai-sandbox/blob/main/src/core/graph.py) &nbsp; · &nbsp; [Model routing](https://github.com/S-Srinivasan-06/sandman-ai-sandbox/blob/main/src/infrastructure/models.py)

**How I work with LLMs:** I use Codex and Claude Code for repository exploration, implementation, debugging, and review. Taskflow Local and Sandman show my work with custom harnesses, local inference, structured outputs, tool execution, and agent orchestration.

---

[All repositories](https://github.com/S-Srinivasan-06?tab=repositories) &nbsp; · &nbsp; [LeetCode](https://leetcode.com/u/aKpXSchpeo/) &nbsp; · &nbsp; [Contact](mailto:srinivasansubr2006@gmail.com)
