# Olivia Legal AI POWERED Assistant 

This project is a **FastAPI-based backend** integrated with **Semantic Kernel**, **Ollama**, and **MongoDB**, built to analyze legal documents, detect risks, and enhance legal comprehension using AI.

Run locally: `http://127.0.0.1:8000`

---

## Features

* Upload and store legal documents
* Analyze documents with LLMs via Semantic Kernel
* Detect legal risks and extract contract metadata
* Use Ollama with DeepSeek-R1 model locally

---

## Installation

### 1. Clone the Repo

```bash
git clone https://github.com/your-org/olivia-backend.git
cd olivia-backend
```

### 2. Install Python Dependencies

Create a virtual environment and install:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure `.env`

Create a `.env` file:

```
OLLAMA_API_BASE=http://localhost:11434
OLLAMA_MODEL=deepseek-r1:1.5b
MONGO_URI=mongodb://localhost:27017
MONGO_DB=olivia_legal_docs
```

### 4. Start Ollama

Install and run model:

```bash
ollama pull deepseek-r1:1.5b
ollama serve
```

### 5. Run Server

```bash
uvicorn main:app --reload
```

---

## 📁 Project Structure

```bash
src/
├── api
│   ├── controllers/
│   ├── routes/
│   └── middlewares/
├── application
│   ├── use_cases/
│   └── dtos/
├── domain
│   ├── entities/
│   ├── repositories/
│   ├── services/
│   └── value_objects/
├── infrastructure
│   ├── ai/ollama
│   ├── ai/semantic_kernel/plugins
│   ├── database/
│   ├── mappers/
│   └── repositories/
```

---

## 📌 Key Endpoints (FastAPI)

### 1. `POST /api/documents/upload`

Upload a legal document.
**Body (form-data):**

* `file`: File to upload
* `title`: Document title
* `doc_type`: Document type

### 2. `GET /api/documents/{id}`

Fetch document by ID.

### 3. `GET /api/documents`

List all documents.

### 4. `POST /api/documents/{id}/analyze`

Analyze a document using the Semantic Kernel + Ollama. Detects legal risks and returns them.

### 5. `DELETE /api/documents/{id}` *(Optional)*

Delete a specific document.

---

## 🧠 Semantic Kernel Plugins

* `DocumentAnalysisPlugin`

  * Identifies clauses with high legal risk.
  * Returns list of `risks` with severity, description, and recommendations.

* `LegalResearchPlugin`

  * Placeholder for smart precedent-based legal query answering.

---

## 🧪 Core Use Cases

* `analyze_document_use_case.py`

  * Orchestrates risk detection using Semantic Kernel

* `upload_document_use_case.py`

  * Saves documents to MongoDB

* `get_document_use_case.py`

  * Fetches one document by ID

---

## 🧩 Dependencies

* `FastAPI`
* `Uvicorn`
* `Semantic-Kernel`
* `Ollama`
* `Pymongo`
* `Pydantic v2`

---

## 📖 Technical Stories

1. **As a developer**, I want to upload a document via multipart form so that users can analyze PDFs or plain text easily.
2. **As a developer**, I want the `/analyze` endpoint to detect legal risks using an LLM.
3. **As a developer**, I want to extract metadata like `duration`, `amount`, and `parties` from contracts.
4. **As a developer**, I want Semantic Kernel to abstract the LLM logic so I can swap models easily.
5. **As a developer**, I want MongoDB to persist documents and allow re-analysis.
6. **As a developer**, I want to keep risks as embedded objects in each document to simplify queries.
7. **As a developer**, I want DTOs to decouple responses from entities.
8. **As a developer**, I want to centralize all Ollama model configs in `.env`.
9. **As a developer**, I want to plug and play future plugins using Semantic Kernel’s import\_plugin.
10. **As a developer**, I want to test endpoints using `curl` or `Postman` during early dev.
11. **As a developer**, I want to keep analysis errors visible to the client.
12. **As a developer**, I want to isolate use cases to follow Clean Architecture.
13. **As a developer**, I want logs for successful document analysis.
14. **As a developer**, I want to support large model switch-out via ENV (`OLLAMA_MODEL`).
15. **As a developer**, I want a clean and testable backend that can scale with a React frontend.

---

## 👨‍💻 Maintainer

**Developed by JosR-Coding**

---

## 📜 License

MIT or your preferred license.
