# Portfolio project review

Reviewed on 6 October 2026. Three parallel reviewers inspected repository trees, representative implementation files, dependency manifests, tests, and available release records. The selection reflects implemented architecture and completeness; it is not a benchmark or security audit.

| Placement | Project | Why it earns the space |
| --- | --- | --- |
| 01, featured | [Taskflow Local](https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend) | Released Windows app; Tauri/Rust lifecycle and reminders; SQLite persistence; on-device model execution; schema-validated, approval-gated task changes. |
| 02 | [Financial Reconciliation Agent](https://github.com/S-Srinivasan-06/Razorpay-Buildathon-webui-and-cli) | Staged and resumable reconciliation, multitable matching, fee rules, exception review, journal exports, hash-chained audit records, REST/WebSockets, and unit/integration/API tests. |
| 03 | [CrowdShield](https://github.com/S-Srinivasan-06/CrowdShield) | Head detection, custom motion tracking, cached KDE density and pressure metrics, threaded sessions, REST/SSE/MJPEG, adjustable ROI, and archived run artifacts. |
| 04 | [Sandman](https://github.com/S-Srinivasan-06/sandman-ai-sandbox) | LangGraph execution/retry/cleanup, Docker resource controls, MCP tools, provider routing, and artifact bundles. A distinct systems project rather than another application of the same engine. |
| 05, compact | [Taskflow](https://github.com/S-Srinivasan-06/Taskflow) | A complementary web implementation with scoped authentication, ownership checks, optimistic concurrency, timezone-aware scheduling, isolated offline cache, and integration tests. |

## Other projects considered

| Project | Relative depth and selection decision |
| --- | --- |
| Original Razorpay Buildathon | Substantial core engine, but overlaps the more complete web console and CLI repository. |
| Customer Churn with LightGBM | Solid script-based ML workflow with feature engineering, cross-validation, SMOTE, and Optuna. Less complete as a product; evaluation and leakage caveats rule out headline performance claims. |
| Breast Cancer Detection model | Educational browser dashboard and Python experiments. Browser inference and README evaluation use different classifiers; avoid medical or accuracy claims. |
| Pandas CSV data pipeline | Complete learning-scale sequence of data scripts, indicators, exports, and charts; less architectural depth. |
| EEG seizure detection reference repository | Extensive research documentation, explicitly not an implemented detector. |
| BiteSync | Small FastAPI/Gemini backend prototype; README mentions tests/frontend absent from the tree. |
| AI-based coding teacher | Small Flask/Gemini learning prototype; lacks persistence, tests, and complete setup files. |

## Design maintenance

The profile uses local SVG illustrations and ordinary GitHub Markdown. The illustrations are conceptual graphics, not product screenshots. The Taskflow Local interface link points to the repository's real UI capture, which uses synthetic tasks and mocked native/model calls.

Edit `README.md` for copy and links. Edit `assets/*.svg` for artwork. The hero's sculpture and featured card's flow animate through CSS inside the SVG; both stop under `prefers-reduced-motion: reduce`. All text remains static. No runtime scripts, external image services, scheduled workflow, or generated statistics are required.
