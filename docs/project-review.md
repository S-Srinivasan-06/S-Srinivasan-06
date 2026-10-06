# Portfolio project review

Reviewed on 6 October 2026. Three parallel reviewers inspected repository trees, representative implementation files, dependency manifests, tests, and available release records. The selection reflects implemented architecture and completeness; it is not a benchmark or security audit.

| Placement | Project | Why it earns the space |
| --- | --- | --- |
| Featured | [Taskflow Local](https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend) | Released Windows app; native desktop lifecycle and reminders; SQLite persistence; on-device model execution; schema-validated, approval-gated task changes. |
| Backend | [Taskflow](https://github.com/S-Srinivasan-06/Taskflow) | Java and Spring Boot implementation with scoped authentication, ownership checks, optimistic concurrency, timezone-aware scheduling, isolated offline cache, and integration tests. |
| Backend | [Financial Reconciliation Agent](https://github.com/S-Srinivasan-06/Razorpay-Buildathon-webui-and-cli) | Staged and resumable reconciliation, multitable matching, fee rules, exception review, journal exports, hash-chained audit records, REST/WebSockets, and unit/integration/API tests. |
| ML | [CrowdShield](https://github.com/S-Srinivasan-06/CrowdShield) | Head detection, custom motion tracking, cached KDE density and pressure metrics, threaded sessions, REST/SSE/MJPEG, adjustable ROI, and archived run artifacts. |
| Agentic AI | [Sandman](https://github.com/S-Srinivasan-06/sandman-ai-sandbox) | LangGraph execution/retry/cleanup, Docker resource controls, MCP tools, provider routing, and artifact bundles. |

## Other projects considered

| Project | Relative depth and selection decision |
| --- | --- |
| Customer Churn with LightGBM | Feature engineering, cross-validation, SMOTE, and Optuna. Available as additional tabular ML work; the primary five projects retain the broader backend, desktop, vision, and agent coverage. Evaluation caveats rule out headline performance claims. |
| Original Razorpay Buildathon | Substantial core engine, but overlaps the more complete web console and CLI repository. |
| Breast Cancer Detection model | Educational browser dashboard and Python experiments. Browser inference and README evaluation use different classifiers; avoid medical or accuracy claims. |
| Pandas CSV data pipeline | Complete learning-scale sequence of data scripts, indicators, exports, and charts; less architectural depth. |
| EEG seizure detection reference repository | Extensive research documentation, explicitly not an implemented detector. |
| BiteSync | Small FastAPI/Gemini backend prototype; README mentions tests/frontend absent from the tree. |
| AI-based coding teacher | Small Flask/Gemini learning prototype; lacks persistence, tests, and complete setup files. |

## Design maintenance

The current profile is an SVG portfolio. All visible names, project descriptions, technologies, skills, interests, and social details are rendered as SVG text. README.md only arranges picture elements and links. The main sequence is an introduction, five coloured project tabs, the five project cards, skills, tools, LLM workflow, interests, and social links. Taskflow Local is first.

Each project has its own four-colour scheme: shared ivory (#F5F0E7) and ink (#252C36), plus an accent and tint. Taskflow Local uses burgundy (#96394A / #EAD5D4); Taskflow uses blue (#315A88 / #D7E2ED); Reconciliation uses amber (#7B5725 / #EADFC6); CrowdShield uses forest (#2A6252 / #D5E4DC); Sandman uses purple (#67487F / #E0D8E9). Colour tabs link to repositories; they are navigation images, not JavaScript theme switches.

Animations show relevant system behaviour: dashed execution paths, moving packets, scan lines, and squares on a tracking grid. Main descriptions remain static. Every animation stops with prefers-reduced-motion: reduce. Desktop and mobile have separate SVG compositions, including the tab and social images. No JavaScript, foreignObject, external fonts, or image dependencies are used inside the SVGs.

Python, Java, and Spring Boot lead the skills section, with SQL for relational data. The tool panel names FastAPI, Docker, PostgreSQL, React, OpenCV, LangGraph, MCP, Ollama, Codex, and Claude Code. The author's correction about Rust, Go, and Ruby is respected; these languages are not presented as skills. Project architecture descriptions do not imply personal proficiency in every language in a repository.

The LLM panel describes Codex and Claude Code workflows, custom harnesses, local models, structured outputs, validation, scoped tool access, and agent orchestration, supported by the author’s stated experience and the reviewed Taskflow Local and Sandman implementations. Interests cover backend systems, ML evaluation and vision, and agent infrastructure. Social panels link to GitHub, LinkedIn, email, and LeetCode. Icons are original vector line drawings and are labelled with tool names.

The diagrams are conceptual illustrations of reviewed project behaviour, not screenshots. No benchmark, medical, proficiency-percentage, or invented employment claims are included. The structure draws on the project descriptions and concise navigation of [Brittany Chiang](https://brittanychiang.com/), [Lee Robinson](https://leerob.com/), and [Arpit Bhayani](https://arpitbhayani.me/), inspected earlier in this session. No website prose or layout code was copied.

Edit README.md for destinations and assets/p5-*.svg for the current artwork and descriptions. Earlier assets remain for history and are not displayed. Browser verification covers image loading, text bounds and overlap, mobile source selection, horizontal overflow, and reduced-motion behaviour.
