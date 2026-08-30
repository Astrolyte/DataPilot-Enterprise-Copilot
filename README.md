# DataPilot Enterprise Copilot

DataPilot Enterprise Copilot is an enterprise AI analytics assistant that lets users ask business questions in natural language and receive answers from either structured data, policy/document knowledge, or a combined SQL + RAG flow. It is designed for internal teams that need fast access to operational metrics, customer contract information, and document-based policy guidance without writing SQL or manually searching knowledge repositories.

---

## What DataPilot is

DataPilot is a multi-layer AI application that combines:

- a FastAPI backend for authentication, orchestration, and API access
- a React + Vite frontend for the user experience
- PostgreSQL for structured business data
- Qdrant for vector search over enterprise documents and contracts
- LLM-based routing and answer generation with Ollama / LangChain

The product supports three main query patterns:

1. SQL route: answers from structured database tables
2. RAG route: answers from enterprise documents and policy content
3. HYBRID route: combines customer/contract metadata from PostgreSQL with contract text from Qdrant

The application is built as a modern enterprise copilot with authentication, role-aware access, audit logging, and query metrics.

---

## Problem it solves

Enterprise teams often have to bridge three disconnected systems:

- business data in relational databases
- compliance and contract documentation in files or document repositories
- user questions expressed in plain language

The result is slow, manual work: analysts must translate questions into SQL, find the right document, and then manually reconcile the two sources. DataPilot reduces that friction by routing the question automatically and returning answers grounded in both business data and enterprise documents.

Typical use cases include:

- “Which customer generated the most revenue?”
- “What is the refund policy for Price LLC?”
- “What is the refund window for Price LLC and how much revenue has the account generated?”

---

## Key capabilities

- Natural-language question handling
- Route selection using an LLM router:
  - SQL
  - RAG
  - HYBRID
- Structured data queries against PostgreSQL
- Retrieval over enterprise docs and contracts via Qdrant
- Hybrid answer synthesis using SQL + retrieved document context
- JWT-based authentication
- Google OAuth login support
- Role-based access patterns for sales/admin usage
- Audit trail for query activity and latency
- Request ID middleware for traceability
- Query metrics to understand performance hotspots

---

## Architecture diagram

```mermaid
flowchart LR
    U[User] --> FE[React Frontend\nVite + React Router]
    FE --> API[FastAPI Backend\n/auth + /query]
    API --> Router[LLM Query Router]
    Router --> SQL[SQL Pipeline]
    Router --> RAG[RAG Pipeline]
    Router --> HYB[Hybrid Pipeline]

    SQL --> PG[(PostgreSQL\nCustomers, Orders, Contracts)]
    RAG --> QDR[Qdrant\nDocument Vector Store]
    HYB --> PG
    HYB --> QDR

    PG --> LLM[Ollama LLM\nAnswer Synthesis]
    QDR --> LLM
    LLM --> FE

    API --> AUTH[JWT + Google OAuth]
    AUTH --> USERS[(Users / Roles)]
    API --> AUDIT[(Audit Logs)]
```

---

## End-to-end query flow

1. The frontend sends a natural-language query to the backend.
2. The backend authenticates the caller and validates the JWT.
3. The query router classifies the request as SQL, RAG, or HYBRID.
4. The selected pipeline executes:
   - SQL reads from PostgreSQL
   - RAG retrieves relevant document chunks from Qdrant
   - HYBRID combines customer/contract metadata with document context
5. The response is normalized into the API schema and returned to the UI.
6. The backend logs latency, request ID, used tables, source documents, and status to the audit log.

---

## SQL pipeline

The SQL workflow is responsible for answering questions that are fully contained in the relational database.

Flow:

- natural language question
- LLM SQL generation
- SQL execution against PostgreSQL
- result formatting and return to frontend

Implementation files:

- backend/app/services/sql_generator.py
- backend/app/services/sql_executor.py
- backend/app/services/sql_repair.py
- backend/app/services/sql.py

Example question patterns:

- “How many customers do we have?”
- “What is the total revenue this year?”
- “Which customer has the highest completed order value?”

---

## RAG pipeline

The RAG workflow is used when the answer is grounded in enterprise documents, policies, or contract text.

Flow:

- user question enters the backend
- retriever searches Qdrant for relevant chunks
- context builder assembles retrieved content
- LLM answers using only the provided context

Implementation files:

- backend/app/services/retriever.py
- backend/app/services/context.py
- backend/app/services/llm.py
- backend/app/services/rag.py

The retrieval layer supports role-aware filtering and document-level metadata such as owner, document ID, and customer association.

---

## Hybrid pipeline

The hybrid pipeline answers questions that require both structured data and document context, such as contract clauses plus customer revenue or account information.

Flow:

- extract the customer or company name from the question
- find the matching customer record in PostgreSQL
- fetch customer contract metadata
- compute completed revenue from orders
- retrieve the exact contract document from Qdrant
- synthesize a final answer using both database data and contract text

Implementation files:

- backend/app/services/entity_extractor.py
- backend/app/services/hybrid.py
- backend/app/services/hybrid_answer.py

Example question:

- “What is Price LLC’s refund window and how much revenue has Price LLC generated?”

---

## Authentication + RBAC

The application includes authentication and authorization logic for enterprise usage.

### Authentication

- JWT-based session tokens
- password login support
- Google OAuth login support

### Authorization

- users are stored with a role value
- access is checked at the backend for protected endpoints
- role information is included in issued tokens and request processing

Key files:

- backend/app/core/auth.py
- backend/app/api/routes/auth.py
- backend/app/api/dependencies.py
- backend/app/services/user_service.py

The auth routes support:

- POST /auth/register
- POST /auth/login
- GET /auth/google/login
- GET /auth/google/callback

---

## Audit logging

Every query is logged to the audit trail for traceability and compliance visibility.

Audit data includes:

- request ID
- user ID and role
- raw query text
- selected route
- tables used
- source documents used
- latency in milliseconds
- status (success, validation error, error)

Implementation file:

- backend/app/services/audit_service.py

The schema for audit events is defined in:

- backend/app/db/sql/schema.sql

---

## Observability / latency metrics

The backend captures timing metrics for each route to measure where time is spent:

- routing duration
- SQL execution time
- RAG retrieval time
- hybrid entity extraction time
- total query latency

This information is surfaced in the process layer and logged to the audit table.

Relevant code:

- backend/app/services/query_service.py
- backend/app/api/routes/query.py

These metrics are especially useful for identifying whether a slow response is dominated by:

- LLM routing
- SQL generation/execution
- Qdrant retrieval
- answer synthesis

---

## Performance testing with k6

The project is structured to support load and performance testing against the API. k6 is a strong fit for validating request throughput, latency, and error rate under concurrent user traffic.

---

## Evaluation results

The repository includes evaluation scripts for retrieval and RAG quality. These are designed to validate whether the system is returning the correct sources and answers for benchmark questions.

Relevant scripts:

- backend/app/scripts/evaluate_rag.py
- backend/app/scripts/evaluate_retrieval.py

What the evaluation harness covers:

- retrieval accuracy by document/source match
- answer quality checks against benchmark question sets
- quality validation for document-grounded responses

The exact benchmark numbers should be run in your local environment and recorded as the evaluation dataset evolves. The code is prepared to support consistent regression measurement over time.

---

## Project structure

```text
DataPilot Enterprise Copilot/
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   ├── routes/
│   │   │   │   ├── auth.py
│   │   │   │   └── query.py
│   │   │   └── schemas/
│   │   │       └── query.py
│   │   ├── core/
│   │   │   ├── auth.py
│   │   │   ├── config.py
│   │   │   └── database.py
│   │   ├── data/
│   │   │   ├── contracts/
│   │   │   ├── documents/
│   │   │   └── evaluation/
│   │   ├── db/
│   │   │   └── sql/
│   │   │       └── schema.sql
│   │   ├── middleware/
│   │   │   └── request_id.py
│   │   ├── scripts/
│   │   │   ├── create_auth_user.py
│   │   │   ├── evaluate_rag.py
│   │   │   ├── evaluate_retrieval.py
│   │   │   ├── generate_customer_contract.py
│   │   │   ├── generate_data.py
│   │   │   ├── generate_policy_docs.py
│   │   │   ├── ingest_documents.py
│   │   │   └── ...
│   │   └── services/
│   │       ├── audit_service.py
│   │       ├── context.py
│   │       ├── embeddings.py
│   │       ├── entity_extractor.py
│   │       ├── hybrid_answer.py
│   │       ├── hybrid.py
│   │       ├── llm.py
│   │       ├── query_service.py
│   │       ├── rag.py
│   │       ├── retriever.py
│   │       ├── router.py
│   │       ├── sql_executor.py
│   │       ├── sql_generator.py
│   │       ├── sql_repair.py
│   │       ├── sql_validator.py
│   │       ├── sql.py
│   │       ├── user_service.py
│   │       └── vector_store.py
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── App.jsx
│       ├── components/
│       ├── hooks/
│       ├── lib/
│       ├── pages/
│       └── assets/
├── infra/
│   └── docker-compose.yml
└── .env.example (recommended to create locally)
```

---

## Setup instructions

### Prerequisites

- Python 3.12+
- Node.js 18+
- PostgreSQL 16+
- Qdrant
- Ollama with a model such as llama3.2:3b
- Docker and Docker Compose (optional, for infrastructure)

### 1. Start infrastructure services

From the project root:

```bash
docker compose -f infra/docker-compose.yml up -d
```

This starts:

- PostgreSQL on port 5432
- Qdrant on ports 6333 and 6334

### 2. Create environment variables

Create a local `.env` file in the backend directory or project root depending on how your environment is loaded. At minimum, define:

```env
DATABASE_URL=postgresql://postgres:datapilot@localhost:5432/datapilot
SECRET_KEY=change-me-to-a-secure-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
FRONTEND_URL=http://localhost:5173
```

### 3. Install backend dependencies

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# or .venv\Scripts\activate   # Windows
pip install -r requirements.txt
```

### 4. Start the backend

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend is configured for port 5173 by default.

### 6. Optional: initialize test users

If you need a development user for login testing, use the provided scripts or create a user through the register flow.

---

## API endpoints

### Health

- GET /health

### Authentication

- POST /auth/register
- POST /auth/login
- GET /auth/google/login
- GET /auth/google/callback

### Query

- POST /query

Request body:

```json
{
  "question": "Which customer generated the most revenue?"
}
```

Response structure:

```json
{
  "route": "SQL",
  "answer": null,
  "sql": "SELECT ...",
  "rows": [{ "company_name": "Acme Corp", "total_revenue": 125000 }],
  "sources": null
}
```

For RAG and HYBRID responses, the payload usually includes `answer` and `sources` with document information.

---

## Example queries

### SQL examples

- How many customers do we have?
- Which customer generated the most revenue?
- What are the completed order totals by customer?

### RAG examples

- What is the refund policy?
- What is the enterprise SLA?
- What is the privacy retention period?

### Hybrid examples

- What is Price LLC’s refund window and how much revenue has Price LLC generated?
- What are the contract terms for Northwind and how much business has it brought in?

---

## Data model and domain

The system is tuned for an enterprise B2B dataset with tables such as:

- customers
- employees
- products
- orders
- order_items
- transactions
- customer_contracts
- users
- audit_logs

This allows the assistant to mix customer, contract, and commercial metrics with document-grounded policy answers.

---

## Limitations and future improvements

### Current limitations

- answer quality depends on the chosen LLM and prompt quality
- routing correctness can vary with ambiguous questions
- hybrid answers are only as strong as the contract metadata and Qdrant indexing quality
- dependency on external services such as Google OAuth and Ollama must be configured correctly

### High-value future improvements

- add role-aware front-end views and permissions matrices
- improve query validation and SQL safety checks
- add a formal benchmark suite for SQL vs RAG vs HYBRID routes
- integrate a production-grade observability stack (Prometheus, Grafana, tracing)
- support more document types and metadata extraction
- add caching for common queries and document retrieval
- expand k6-generated performance baselines and CI checks

---

## Summary

DataPilot Enterprise Copilot is a practical enterprise assistant for combining structured analytics with document-grounded knowledge. It demonstrates how an AI copilot can route user questions to the right backend capability, answer using the right source of truth, and maintain auditability and performance observability for real business use.

If you want to quickly evaluate it locally, start the infrastructure, launch the backend and frontend, authenticate, then ask a SQL, RAG, or HYBRID question from the dashboard.
