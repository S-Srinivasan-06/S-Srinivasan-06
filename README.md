<picture>
  <source media="(max-width: 600px)" srcset="./assets/hero-mobile.svg" />
  <img src="./assets/hero.svg" width="1200" alt="Srinivasan. LLM systems, harness engineering, and backend development. Built with logic. Shaped with care." />
</picture>

# LLMs, tools, and the systems between them.

I'm **Srinivasan**, a Computer Science undergraduate at **KIIT (2024–2028)**. I work with **Codex and Claude Code**, build **custom LLM harnesses**, and connect **local models, tools, and multi-step agents** to real products.

My foundation is **Java and Python backends, TypeScript interfaces, and Rust desktop integration**. I care about what happens around a model: the context it receives, the tools it can use, the checks around its output, and the experience it creates.

**[Explore my work](#selected-work)** &nbsp; / &nbsp; **[Read my code](#engineering-in-practice)** &nbsp; / &nbsp; **[LinkedIn](https://www.linkedin.com/in/s-srinivasan-a69006315/)** &nbsp; / &nbsp; **[Email me](mailto:srinivasansubr2006@gmail.com)**

<br>

## LLMs & agent engineering

<picture>
  <source media="(max-width: 600px)" srcset="./assets/agents-mobile.svg" />
  <img src="./assets/agents.svg" width="1200" alt="AI engineering across four areas: Codex and Claude Code workflows; custom harnesses connecting context, tools, and validation; local LLM execution with llama.cpp, Gemma, and Ollama; agent orchestration with LangGraph, MCP, and Docker." />
</picture>

**AI-assisted development:** I use **Codex and Claude Code** for repository exploration, planning, implementation, debugging, and verification. I treat context, task scope, tool access, and feedback loops as part of the engineering work.

**Building the agent system:** I connect models to **bounded context, structured outputs, tool registries, execution loops, retries, and human review**. My projects include **on-device inference**, **model lifecycle management**, **provider routing**, and **stateful orchestration**.

[Local inference & harness code ↗](https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend/blob/main/src/model/modelService.ts) &nbsp; · &nbsp; [Agent graph ↗](https://github.com/S-Srinivasan-06/sandman-ai-sandbox/blob/main/src/core/graph.py) &nbsp; · &nbsp; [Model routing ↗](https://github.com/S-Srinivasan-06/sandman-ai-sandbox/blob/main/src/infrastructure/models.py)

<br>

## Selected work

Desktop software, backend systems, and AI tools — with the implementation open to explore.

### 01 / Taskflow Local

<a href="https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend">
  <img src="./assets/taskflow-local.svg" width="1200" alt="Taskflow Local — an offline Windows workspace with local AI. Input moves through model inference, review, and SQLite persistence." />
</a>

**A desktop workspace that keeps tasks and inference on your machine.** Natural-language and screenshot input become reviewable task changes, with reminders and a system tray for daily use.

**Engineering highlights:** on-device Gemma through llama.cpp, a custom inference harness, schema-validated actions, approval before changes, and Rust-managed model lifecycle.

`Tauri 2` `Rust` `React` `TypeScript` `SQLite` `llama.cpp`

**[View source ↗](https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend)** &nbsp; · &nbsp; [Windows download ↗](https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend/releases/latest) &nbsp; · &nbsp; [Interface preview ↗](https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend/blob/main/docs/screenshots/forest-2026-10-05.png)

<br>

### 02 / Financial Reconciliation Agent

<a href="https://github.com/S-Srinivasan-06/Razorpay-Buildathon-webui-and-cli">
  <img src="./assets/reconciliation.svg" width="1200" alt="Financial Reconciliation Agent — connecting sales, gateway ledgers, and bank statements through matching, human review, and audit records." />
</a>

**A workbench for connecting financial records.** A staged pipeline combines fee-aware matching, exception review, and double-entry journal exports through a web console and CLI.

**Engineering highlights:** resumable pipeline state, multitable matching, WebSocket telemetry, and a durable SHA-256 audit chain.

`Python` `FastAPI` `Pandas` `Pydantic` `WebSockets` `Docker`

**[View source ↗](https://github.com/S-Srinivasan-06/Razorpay-Buildathon-webui-and-cli)** &nbsp; · &nbsp; [Read the pipeline ↗](https://github.com/S-Srinivasan-06/Razorpay-Buildathon-webui-and-cli/blob/main/src/app/pipeline.py)

<br>

### 03 / CrowdShield

<a href="https://github.com/S-Srinivasan-06/CrowdShield">
  <img src="./assets/crowdshield.svg" width="1200" alt="CrowdShield — computer vision with head detection, motion tracking, editable regions, and density visualization." />
</a>

**A computer vision dashboard for understanding crowd movement.** Detection and tracking feed density and pressure visualizations, with editable regions of interest and archived runs.

**Engineering highlights:** predictive centroid tracking, cached Gaussian KDE, threaded sessions, SSE telemetry, and MJPEG streaming.

`Python` `OpenCV` `YOLOv8` `OpenVINO` `NumPy` `JavaScript`

**[View source ↗](https://github.com/S-Srinivasan-06/CrowdShield)** &nbsp; · &nbsp; [Read the tracking engine ↗](https://github.com/S-Srinivasan-06/CrowdShield/blob/main/src/features.py)

<br>

### 04 / Sandman

<a href="https://github.com/S-Srinivasan-06/sandman-ai-sandbox">
  <img src="./assets/sandman.svg" width="1200" alt="Sandman — an AI coding agent that executes, inspects, retries, and bundles code inside Docker workspaces." />
</a>

**An AI coding agent with a workspace and an execution loop.** It writes, runs, and retries code inside Docker workspaces, then packages the output for use outside the session.

**Engineering highlights:** LangGraph orchestration, MCP tools, execution and cleanup paths, Docker resource controls, and routing across local and hosted model providers.

`Python` `LangGraph` `LangChain` `MCP` `Docker` `Ollama`

**[View source ↗](https://github.com/S-Srinivasan-06/sandman-ai-sandbox)** &nbsp; · &nbsp; [Read the agent graph ↗](https://github.com/S-Srinivasan-06/sandman-ai-sandbox/blob/main/src/core/graph.py)

<br>

### 05 / Taskflow

<a href="https://github.com/S-Srinivasan-06/Taskflow">
  <img src="./assets/taskflow-web.svg" width="1200" alt="Taskflow — a React and Spring Boot workspace with scoped sessions, ownership checks, PostgreSQL storage, and integration tests." />
</a>

**A task workspace for the web.** Calendars, timezone-aware scheduling, and instant status updates connect a React interface to a Spring Boot and PostgreSQL backend.

**Engineering highlights:** ownership checks, optimistic concurrency, an isolated offline read cache, and Testcontainers integration tests.

`Java` `Spring Boot` `React` `TypeScript` `PostgreSQL` `Docker`

**[View source ↗](https://github.com/S-Srinivasan-06/Taskflow)** &nbsp; · &nbsp; [Read the integration tests ↗](https://github.com/S-Srinivasan-06/Taskflow/blob/main/src/test/java/com/taskflow/security/AuthOwnershipIntegrationTest.java)

<br>

## Working stack

<picture>
  <source media="(max-width: 600px)" srcset="./assets/toolkit-mobile.svg" />
  <img src="./assets/toolkit.svg" width="1200" alt="Languages: Java, Python, TypeScript, Rust, SQL. Frameworks: Spring Boot, FastAPI, React, Tauri. Data and AI: PostgreSQL, SQLite, Docker, LangGraph, MCP, OpenCV." />
</picture>

My main languages are **Java, Python, TypeScript, Rust, and SQL**. I use **Spring Boot and FastAPI** for services, **React and Tauri** for products, and **LangGraph, MCP, and Docker** for agent workflows.

<br>

## Engineering in practice

<picture>
  <source media="(max-width: 600px)" srcset="./assets/harness-mobile.svg" />
  <img src="./assets/harness.svg" width="1200" alt="An agent harness connects a goal and bounded context to models and tools, executes actions, validates results, and routes changes through review. Feedback supports retries and refinement." />
</picture>

A capable model is one part of the system. The harness also needs **clear state, scoped tools, useful feedback, and explicit control over mutations**. These are the boundaries I work on in Taskflow Local and Sandman.

<picture>
  <source media="(max-width: 600px)" srcset="./assets/code-mobile.svg" />
  <img src="./assets/code.svg" width="1200" alt="Code you can reason about. A TypeScript and Zod schema from Taskflow Local validates task-creation inputs before they reach the write service." />
</picture>

| Engineering decision | Implementation to explore |
| --- | --- |
| **Validate before changing state** | [Strict Zod action schemas](https://github.com/S-Srinivasan-06/Taskflow-Local-hacktoberfest-weekend/blob/main/src/model/actionSchema.ts) constrain model-generated task operations. |
| **Make ownership explicit** | [Task service](https://github.com/S-Srinivasan-06/Taskflow/blob/main/src/main/java/com/taskflow/service/TaskService.java) scopes operations to users and checks versions before mutations. |
| **Test the boundaries** | [Integration tests](https://github.com/S-Srinivasan-06/Taskflow/blob/main/src/test/java/com/taskflow/security/AuthOwnershipIntegrationTest.java) exercise isolation, CSRF, session revocation, and conflicting updates. |
| **Leave an inspectable trail** | [Append-only audit ledger](https://github.com/S-Srinivasan-06/Razorpay-Buildathon-webui-and-cli/blob/main/src/app/core/audit.py) chains records with SHA-256 hashes and persists them to disk. |

<br>

## Beyond the code

<img src="./assets/about.svg" width="1200" alt="Computer Science at KIIT, 2024–2028. WorldQuant BRAIN Gold Tier Consultant. Interested in systems, product craft, and quantitative research." />

I enjoy the space where **engineering rigor meets product craft**: a clear data model, a predictable workflow, and an interface that helps someone get things done. Alongside my Computer Science degree, I work on quantitative research as a **WorldQuant BRAIN Gold Tier Consultant**.

[More repositories ↗](https://github.com/S-Srinivasan-06?tab=repositories) &nbsp; · &nbsp; [LeetCode ↗](https://leetcode.com/u/aKpXSchpeo/)

<br>

<a href="mailto:srinivasansubr2006@gmail.com">
  <img src="./assets/contact.svg" width="1200" alt="Let's build something useful. Get in touch about LLM systems, agent harnesses, or backend engineering at srinivasansubr2006@gmail.com." />
</a>

**[Get in touch ↗](mailto:srinivasansubr2006@gmail.com)** &nbsp; · &nbsp; [Connect on LinkedIn ↗](https://www.linkedin.com/in/s-srinivasan-a69006315/)
