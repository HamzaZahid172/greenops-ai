# Contributing to GreenOps AI

Thank you for your interest in contributing to GreenOps AI.

GreenOps AI is an open-source AI Engineering and GreenOps project focused on workload efficiency, carbon-aware computing, local AI, agentic workflows, Retrieval-Augmented Generation (RAG), evaluation, observability, and modern software engineering practices.

This guide explains how to set up the project, create changes safely, run quality checks, and submit pull requests.

---

## 1. Ways to Contribute

Contributions are welcome in areas such as:

- backend engineering
- frontend development
- workload optimization
- carbon-intensity integrations
- carbon-aware scheduling
- AI Assistant improvements
- agentic AI
- agent tools
- RAG
- embeddings
- vector search
- PostgreSQL / pgvector
- AI evaluation
- testing
- Docker
- CI/CD
- Prometheus
- Grafana
- documentation
- accessibility
- cloud integrations
- Kubernetes and Helm

You can contribute by:

- fixing bugs
- adding tests
- improving documentation
- proposing new features
- creating new AI evaluation scenarios
- adding new agent tools
- improving RAG quality
- improving frontend usability
- improving observability
- improving developer experience

---

## 2. Project Principles

Before contributing, please keep these principles in mind:

1. Prefer clear, maintainable code over unnecessary complexity.
2. Keep API routing separate from domain logic.
3. Keep persistence logic separate from services.
4. Keep AI provider details behind provider abstractions.
5. Keep agent capabilities explicit through tools.
6. Ground documentation answers through RAG.
7. Add tests for deterministic behavior.
8. Add evaluation scenarios for AI behavior.
9. Preserve local-first and free-to-run development where practical.
10. Measure important AI operations with observability.
11. Do not introduce paid services as mandatory dependencies.
12. Do not commit secrets or private infrastructure data.

---

## 3. Repository Structure

The repository is organized roughly as follows:

```text
greenops-ai/
│
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   ├── observability/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   └── services/
│   │       ├── agent/
│   │       ├── ai/
│   │       ├── carbon/
│   │       └── rag/
│   ├── tests/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   ├── Dockerfile
│   └── nginx.conf
│
├── evaluation/
│   ├── fixtures/
│   ├── results/
│   ├── metrics.py
│   ├── run_evaluation.py
│   └── scenarios.json
│
├── observability/
│   ├── grafana/
│   └── prometheus/
│
├── datasets/
├── docs/
├── scripts/
│
├── docker-compose.yml
├── .env.example
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

---

## 4. Prerequisites

For the full local development environment, install:

- Git
- Python 3.12
- Node.js
- Docker Desktop
- Ollama
- PostgreSQL if you want to run the database outside Docker

Recommended:

- VS Code
- Docker extension
- Python extension
- ESLint support
- Prettier support

---

## 5. Fork and Clone

Fork the repository on GitHub, then clone your fork:

```bash
git clone https://github.com/<your-username>/greenops-ai.git
cd greenops-ai
```

Add the original repository as an upstream remote:

```bash
git remote add upstream https://github.com/HamzaZahid172/greenops-ai.git
```

Verify:

```bash
git remote -v
```

You should see both:

```text
origin
upstream
```

---

## 6. Branch Strategy

Development work should normally start from the latest `develop` branch.

Update your local branch:

```bash
git checkout develop
git pull upstream develop
```

Create a new branch:

```bash
git checkout -b feature/<short-name>
```

Recommended branch prefixes:

```text
feature/<name>
fix/<name>
docs/<name>
test/<name>
refactor/<name>
chore/<name>
```

Examples:

```text
feature/aws-workload-provider
feature/rag-pdf-support
fix/carbon-provider-timeout
docs/update-rag-guide
test/add-agent-evaluation
refactor/embedding-service
```

Do not develop directly on `main`.

Avoid developing directly on `develop` unless you are maintaining your own repository and intentionally doing so.

---

## 7. Environment Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Review the configuration before running the project.

Typical environment settings include:

- application version
- database URL
- Ollama URL
- generation model
- embedding model
- embedding dimension
- RAG chunk configuration
- carbon provider URL
- CORS origins

Never commit your real `.env` file.

Do not commit:

- passwords
- API keys
- personal access tokens
- private database URLs
- private cloud credentials
- private infrastructure information

---

## 8. Ollama Setup

GreenOps AI currently uses Ollama for local AI.

Install the generation model:

```bash
ollama pull llama3.2:3b
```

Install the embedding model:

```bash
ollama pull nomic-embed-text
```

Verify:

```bash
ollama list
```

Expected models include:

```text
llama3.2:3b
nomic-embed-text
```

Make sure Ollama is running before testing AI, Agent, RAG, or evaluation functionality.

---

## 9. Backend Development Setup

Move to the backend:

```bash
cd backend
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the backend:

```bash
uvicorn app.main:app --reload
```

The API should become available at:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## 10. Frontend Development Setup

From the repository root:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

Open:

```text
http://localhost:5173
```

---

## 11. Docker Development

The easiest way to run the complete stack is Docker Compose.

Make sure:

- Docker Desktop is running
- Ollama is running on the host

Then run:

```bash
docker compose up -d --build
```

Check containers:

```bash
docker compose ps
```

Expected services include:

```text
backend
db
frontend
prometheus
grafana
```

Useful local URLs:

```text
Frontend:     http://localhost:5173
Backend:      http://localhost:8000
Swagger:      http://localhost:8000/docs
Metrics:      http://localhost:8000/metrics
Prometheus:   http://localhost:9090
Grafana:      http://localhost:3000
```

Stop the stack:

```bash
docker compose down
```

---

## 12. Database Migrations

GreenOps AI uses Alembic.

From `backend/`, apply migrations:

```bash
alembic upgrade head
```

Check current migration:

```bash
alembic current
```

Check migration heads:

```bash
alembic heads
```

If you change SQLAlchemy models and need a new migration:

```bash
alembic revision --autogenerate -m "describe migration"
```

Always inspect generated migration files before committing them.

Do not blindly trust autogeneration for:

- pgvector types
- extensions
- complex indexes
- data migrations

---

## 13. Backend Code Organization

Keep responsibilities separated.

### API Routes

Location:

```text
backend/app/api/routes/
```

Routes should mainly handle:

- request parsing
- dependency injection
- service calls
- HTTP error conversion
- response construction

Avoid putting large business rules directly into route files.

---

### Schemas

Location:

```text
backend/app/schemas/
```

Use Pydantic models for:

- requests
- responses
- structured internal data

Keep API contracts explicit.

---

### Services

Location:

```text
backend/app/services/
```

Services should contain business and domain logic.

Examples:

- workload analysis
- carbon provider logic
- scheduling
- AI generation
- RAG retrieval
- embedding generation
- agent planning

---

### Repositories

Location:

```text
backend/app/repositories/
```

Repositories should handle database persistence and queries.

Avoid mixing SQLAlchemy persistence logic deeply into domain services where possible.

---

## 14. Adding a New API Endpoint

When adding an endpoint:

1. Define request/response schemas.
2. Implement or reuse a service.
3. Add the route.
4. Add tests.
5. Update Swagger descriptions if useful.
6. Add observability if the operation is important.
7. Update documentation if the endpoint is user-facing.

Example layout:

```text
schemas/
    new_feature.py

services/
    new_feature.py

api/routes/
    new_feature.py

tests/
    test_new_feature.py
```

---

## 15. Adding a New Agent Tool

Agent tools should represent explicit, controlled application capabilities.

Do not give the model unrestricted code execution.

A new tool should:

1. Have one clear responsibility.
2. Validate its input.
3. Call an existing service where possible.
4. Return structured output.
5. Handle known service failures.
6. Be observable.
7. Be tested.
8. Be included in evaluation if it affects agent behavior.

Conceptually:

```text
User Request
     ↓
Planner
     ↓
Tool Selection
     ↓
Validated Tool Arguments
     ↓
Application Service
     ↓
Structured Observation
     ↓
Final Response
```

When adding a tool, also consider:

- Should the tool be available for every request?
- Could the tool expose sensitive data?
- Could the tool cause side effects?
- Does the tool require authorization in a future production environment?

---

## 16. Adding a New AI Provider

AI provider logic should remain behind provider abstractions.

A new provider should avoid forcing route handlers to understand provider-specific details.

Recommended responsibilities:

- request construction
- model invocation
- timeout handling
- provider error translation
- response normalization
- metrics

Provider-specific HTTP errors should be converted into application-level exceptions.

---

## 17. Adding RAG Support

The current RAG pipeline follows this pattern:

```text
Document
   ↓
Parse
   ↓
Chunk
   ↓
Embed
   ↓
Store in PostgreSQL + pgvector
```

Query flow:

```text
Question
   ↓
Embed
   ↓
Vector Search
   ↓
Relevant Chunks
   ↓
Context
   ↓
LLM
   ↓
Grounded Answer
```

When improving RAG, preserve:

- source metadata
- chunk traceability
- deterministic ingestion where possible
- retrieval tests
- evaluation coverage

---

## 18. Adding Support for a New Document Type

When adding a new document type:

1. Validate MIME type / extension.
2. Parse text safely.
3. Normalize extracted content.
4. Preserve filename metadata.
5. Chunk the extracted text.
6. Generate embeddings.
7. Store document and chunk records.
8. Add tests.
9. Add at least one evaluation scenario if appropriate.

Potential future formats include:

- PDF
- DOCX
- HTML
- YAML
- JSON
- source code

---

## 19. Adding Evaluation Scenarios

AI behavior should not rely only on normal unit tests.

Evaluation files are located under:

```text
evaluation/
```

Core files include:

```text
evaluation/scenarios.json
evaluation/run_evaluation.py
evaluation/metrics.py
```

When adding a scenario, define what behavior is expected.

Examples:

- expected agent tools
- required answer terms
- forbidden terms
- expected sources
- scenario type

Good evaluation scenarios should test behavior rather than exact model wording.

Avoid assertions that require the LLM to return one exact sentence unless the behavior truly requires it.

---

## 20. Running AI Evaluation

Make sure the GreenOps API and Ollama are running.

From the project root:

```bash
python -m evaluation.run_evaluation
```

The current v1.0 evaluation target is:

```text
Passed: 4/4
Pass rate: 100.0%
```

The report is written to:

```text
evaluation/results/latest.json
```

If your change affects:

- RAG
- agent planning
- agent tools
- AI prompting
- embeddings
- retrieval

you should run the evaluation before submitting the pull request.

---

## 21. Backend Tests

From `backend/`:

```bash
python -m pytest -v
```

All tests should pass before opening a pull request.

When fixing a bug, add a regression test where practical.

---

## 22. Python Compilation Check

From `backend/`:

```bash
python -m compileall app tests
```

This should complete without syntax or import compilation errors.

---

## 23. Frontend Quality Checks

From `frontend/`:

```bash
npm run lint
```

Then:

```bash
npm run build
```

Both should pass before opening a frontend-related pull request.

---

## 24. Docker Validation

If your change affects:

- dependencies
- environment variables
- Dockerfiles
- entrypoint scripts
- networking
- PostgreSQL
- Prometheus
- Grafana

run:

```bash
docker compose config
```

Then:

```bash
docker compose up -d --build
```

Verify:

```bash
docker compose ps
```

---

## 25. Observability Guidelines

Important backend operations should be observable.

Consider metrics for:

- request count
- latency
- errors
- LLM generation
- embeddings
- RAG retrieval
- agent tool execution

Avoid metrics with uncontrolled high-cardinality labels.

Bad example:

```text
user_question="entire arbitrary user prompt"
```

Better labels include bounded values such as:

```text
route
method
status
tool
provider
outcome
```

---

## 26. Prometheus Changes

Prometheus configuration is located under:

```text
observability/prometheus/
```

If you modify scraping:

1. validate the configuration
2. start Docker Compose
3. open Prometheus
4. verify the target is `UP`
5. query the expected metric

Prometheus UI:

```text
http://localhost:9090
```

---

## 27. Grafana Changes

Grafana provisioning files are located under:

```text
observability/grafana/
```

When modifying dashboards:

- keep datasource provisioning reproducible
- keep dashboard JSON in source control
- avoid requiring manual setup
- verify panels after a clean container restart

Grafana:

```text
http://localhost:3000
```

---

## 28. Health and Readiness

GreenOps AI provides:

```text
GET /api/v1/health
```

and:

```text
GET /api/v1/health/ready
```

Use them for different purposes.

`/health` answers:

> Is the FastAPI application running?

`/health/ready` answers:

> Is the application ready to serve requests that require its dependencies?

If required dependencies are unavailable, readiness should return an appropriate non-success response such as HTTP `503`.

---

## 29. Code Style

### Python

Prefer:

- type hints
- small focused functions
- descriptive names
- explicit error handling
- clear service boundaries
- async code for async I/O paths

Avoid:

- large route handlers
- broad `except Exception` without a reason
- hidden global state
- duplicated provider logic
- unnecessary abstractions

### TypeScript / React

Prefer:

- typed props
- typed API responses
- reusable services
- small components
- clear loading/error states

Avoid:

- repeated raw fetch logic across pages
- `any` unless necessary
- large components with unrelated responsibilities

---

## 30. Formatting

Before committing:

```bash
git diff --check
```

This should produce no output.

Also inspect your actual diff:

```bash
git diff
```

If changes are staged:

```bash
git diff --cached
```

---

## 31. Commit Messages

Use clear commit messages.

Recommended style:

```text
type: short description
```

Examples:

```text
feat: add AWS workload provider
fix: handle carbon provider timeout
docs: update architecture guide
test: add agent tool evaluation
refactor: simplify embedding provider
chore: update Docker configuration
```

Useful types include:

```text
feat
fix
docs
test
refactor
chore
ci
build
```

Keep commits focused where practical.

---

## 32. Pull Request Workflow

Before opening a pull request:

```bash
git status
git diff --check
```

Run relevant checks.

Typical full verification:

```bash
cd backend
python -m pytest -v
python -m compileall app tests

cd ../frontend
npm run lint
npm run build

cd ..
docker compose config
python -m evaluation.run_evaluation
```

Not every change requires every expensive check, but changes affecting AI, RAG, Docker, or infrastructure should receive appropriate verification.

Push your branch:

```bash
git push -u origin <branch-name>
```

Open a pull request targeting:

```text
develop
```

unless the maintainers specify otherwise.

---

## 33. Pull Request Description

A good pull request should explain:

### What changed?

Describe the implementation.

### Why?

Explain the problem or goal.

### How was it tested?

Include commands or evidence.

### Does it affect AI behavior?

If yes, include evaluation results.

### Does it affect infrastructure?

If yes, include Docker/Prometheus/Grafana verification.

Example:

```markdown
## Summary

Adds retry handling to the carbon provider.

## Why

Temporary provider failures were causing immediate API failures.

## Testing

- `pytest -v`
- `python -m compileall app tests`
- manual carbon endpoint verification

## Result

All backend tests pass.
```

---

## 34. Pull Request Checklist

Before requesting review, confirm:

- [ ] I created my work on an appropriate branch.
- [ ] I reviewed my own diff.
- [ ] `git diff --check` passes.
- [ ] Backend tests pass if backend code changed.
- [ ] Frontend lint passes if frontend code changed.
- [ ] Frontend build passes if frontend code changed.
- [ ] AI evaluation passes if AI / RAG / Agent behavior changed.
- [ ] Docker configuration is valid if infrastructure changed.
- [ ] I added or updated tests where appropriate.
- [ ] I updated documentation where appropriate.
- [ ] I did not commit secrets.
- [ ] I did not commit my local `.env`.
- [ ] My pull request explains what changed and why.

---

## 35. Bug Reports

A useful bug report should include:

- expected behavior
- actual behavior
- reproduction steps
- environment
- relevant logs
- screenshots if useful

For AI-related issues, also include:

- model name
- endpoint
- user request
- tools selected
- relevant RAG sources
- evaluation scenario if available

Do not include secrets or private data.

---

## 36. Feature Requests

Feature requests should explain:

- the problem
- the proposed behavior
- why it belongs in GreenOps AI
- possible implementation approach
- potential complexity
- whether it affects v1.x or is better suited for a later release

Before implementing a large feature, consider discussing it in an issue first.

---

## 37. Security Issues

Do not publicly post sensitive security vulnerabilities with exploit details before maintainers have had a reasonable opportunity to review them.

Do not include:

- real credentials
- real tokens
- private infrastructure access details
- private datasets

For normal development, use fake or local test values.

---

## 38. Scope Control

GreenOps AI is intentionally developed in phases.

Not every useful idea should be added immediately.

For v1.x contributions, prefer improvements that strengthen:

- reliability
- evaluation
- observability
- cloud integrations
- RAG quality
- workload analysis
- carbon intelligence
- developer experience

Large architectural changes should be discussed before implementation.

---

## 39. Current Roadmap

See:

```text
docs/ROADMAP.md
```

for planned releases and future contribution opportunities.

See:

```text
docs/ARCHITECTURE.md
```

for the current system architecture.

---

## 40. Contributor Development Flow

Recommended flow:

```text
Read issue / define change
        ↓
Sync develop
        ↓
Create feature branch
        ↓
Implement
        ↓
Add tests
        ↓
Run checks
        ↓
Run AI evaluation if needed
        ↓
Review git diff
        ↓
Commit
        ↓
Push
        ↓
Open PR to develop
        ↓
CI
        ↓
Review
        ↓
Merge
```

---

## 41. First-Time Contributor Suggestions

If you are new to the project, good starting areas include:

- documentation improvements
- unit tests
- frontend usability
- new evaluation scenarios
- Grafana panels
- carbon provider tests
- input validation
- error messages

More advanced contributions include:

- new agent tools
- new document parsers
- cloud provider integrations
- Kubernetes
- Helm
- OpenTelemetry
- hybrid RAG search
- reranking

---

## 42. Questions

If something in the project is unclear:

1. Read `README.md`.
2. Read `docs/ARCHITECTURE.md`.
3. Read `docs/ROADMAP.md`.
4. Search existing issues.
5. Open a focused issue or discussion if clarification is still needed.

---

## 43. License

By contributing to GreenOps AI, you agree that your contributions may be distributed under the project's MIT License.

See:

```text
LICENSE
```

for details.

---

## 44. Thank You

GreenOps AI is intended to be both a practical engineering project and a learning platform.

Contributions that improve code quality, AI quality, sustainability reasoning, documentation, testing, observability, or usability are welcome.

Thank you for helping improve GreenOps AI.