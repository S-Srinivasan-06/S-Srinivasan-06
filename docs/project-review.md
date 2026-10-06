# Portfolio project review

Reviewed on 6 October 2026. Three parallel reviewers inspected repository trees, representative implementation files, dependency manifests, tests, and available release records. The selection reflects implemented architecture and completeness; it is not a benchmark or security audit.

| Placement | Project | Why it earns the space |
| --- | --- | --- |
| Featured | [Taskflow Local](https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend) | Released Windows app; native desktop lifecycle and reminders; SQLite persistence; on-device model execution; schema-validated, approval-gated task changes. |
| Backend | [Taskflow](https://github.com/S-Srinivasan-06/Taskflow) | Java and Spring Boot implementation with scoped authentication, ownership checks, optimistic concurrency, timezone-aware scheduling, isolated offline cache, and integration tests. |
| Backend | [Financial Reconciliation Agent](https://github.com/S-Srinivasan-06/Razorpay-Buildathon-webui-and-cli) | Staged and resumable reconciliation, multitable matching, fee rules, exception review, journal exports, hash-chained audit records, REST/WebSockets, and unit/integration/API tests. |
| ML | [CrowdShield](https://github.com/S-Srinivasan-06/CrowdShield) | Head detection, custom motion tracking, cached KDE density and pressure metrics, threaded sessions, REST/SSE/MJPEG, adjustable ROI, and archived run artifacts. |
| ML | [Customer Churn Prediction](https://github.com/S-Srinivasan-06/Customer-Churn-Prediction-with-LightGBM) | Feature engineering, stratified cross-validation, training-fold scaling and SMOTE, threshold selection, and a separate Optuna search. Added to give tabular ML clear representation; no headline performance or leakage-free claims. |
| Agentic AI | [Sandman](https://github.com/S-Srinivasan-06/sandman-ai-sandbox) | LangGraph execution/retry/cleanup, Docker resource controls, MCP tools, provider routing, and artifact bundles. |

## Other projects considered

| Project | Relative depth and selection decision |
| --- | --- |
| Original Razorpay Buildathon | Substantial core engine, but overlaps the more complete web console and CLI repository. |
| Breast Cancer Detection model | Educational browser dashboard and Python experiments. Browser inference and README evaluation use different classifiers; avoid medical or accuracy claims. |
| Pandas CSV data pipeline | Complete learning-scale sequence of data scripts, indicators, exports, and charts; less architectural depth. |
| EEG seizure detection reference repository | Extensive research documentation, explicitly not an implemented detector. |
| BiteSync | Small FastAPI/Gemini backend prototype; README mentions tests/frontend absent from the tree. |
| AI-based coding teacher | Small Flask/Gemini learning prototype; lacks persistence, tests, and complete setup files. |

## Design maintenance

The current profile is a project-focused GitHub README: a short introduction, one featured project, and backend, machine-learning, and agentic-AI sections. Each project has a concise description, repository technologies, and links to representative implementation files. Taskflow Local stays first. Generic slogans, animated geometry, decorative SVG panels, colour switching, and the previous personal-content proportions are no longer part of the visible page.

The author's stated core stack is Python, Java, and Spring Boot. Repository technologies are listed under the relevant project and do not imply personal proficiency in every language in its tree. The author's correction about Rust, Go, and Ruby is respected: none appears in the profile's skill or technology labels. Codex and Claude Code experience is kept in a brief workflow note, with concrete harness and orchestration evidence in Taskflow Local and Sandman.

The only featured image is Taskflow Local's existing interface capture, linked to its original repository. It shows example tasks; the capture uses synthetic tasks and mocked native/model calls. It is an interface preview, not a claim that the native application was independently exercised during this profile revision.

Design references inspected on 6 October 2026: [Brittany Chiang](https://brittanychiang.com/) for clear project descriptions, technology lists, and source links; [Lee Robinson](https://leerob.com/) for compact typography and a short introduction; [Arpit Bhayani](https://arpitbhayani.me/) for engineering work as the centre of a personal homepage. The README uses GitHub's native responsive typography rather than copying their layouts or prose.

Edit README.md for the current content. Earlier SVG versions remain in assets as history but are not displayed. Only public repositories are featured. The LightGBM implementation and Optuna script were re-read for the new ML entry; evaluation results and medical claims are not included.
