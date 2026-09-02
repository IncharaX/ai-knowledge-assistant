# 🤖 AI Knowledge Assistant

A production-oriented **Retrieval-Augmented Generation (RAG)** application that allows users to ask questions about a knowledge base or dynamically uploaded PDF documents.

The system combines **semantic search**, **BM25 keyword retrieval**, **Reciprocal Rank Fusion (RRF)**, **cross-encoder reranking**, and **retrieval confidence validation** to generate grounded answers backed by document sources.

---

## ✨ Features

- 📄 Upload and ask questions about PDF documents
- 🧠 Retrieval-Augmented Generation (RAG)
- 🔍 Semantic vector search using embeddings
- 🔎 BM25 keyword search
- 🔀 Hybrid retrieval using Reciprocal Rank Fusion (RRF)
- 🎯 Cross-encoder reranking for improved relevance
- 🛡️ Confidence-based retrieval validation
- 🤖 AI-generated answers grounded in retrieved context
- 📚 Source citations with document names and page numbers
- 🗂️ Grouped document sources for a cleaner UI
- 📋 Copy AI answers with visual feedback
- 🟢 Grounded answer indicators
- 🔴 Insufficient-information detection
- 💬 Interactive chat interface
- ⚡ REST API powered by FastAPI
- 🩺 Health check endpoint
- 🐳 Dockerized application using Docker Compose

---

## 🖥️ Application Preview

![AI Knowledge Assistant Preview](assets/ai-knowledge-assistant-preview.png)

The application provides an interactive chat interface where users can:

- Ask questions about the knowledge base
- Upload a PDF and ask questions specifically about that document
- View grounded answers with source citations
- See whether sufficient retrieval evidence was found
- Copy generated answers

---

# 🏗️ Architecture

```text
                         ┌──────────────────┐
                         │     Next.js      │
                         │    Frontend      │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             Ask Question                  Upload PDF
                    │                           │
                    ▼                           ▼
          ┌──────────────────┐       ┌──────────────────┐
          │     FastAPI      │       │ PDF Processing   │
          │ Retrieval Service│       │ + Chunking       │
          └────────┬─────────┘       └────────┬─────────┘
                   │                          │
                   │                          ▼
                   │                 ┌──────────────────┐
                   │                 │   Embeddings     │
                   │                 │    + ChromaDB    │
                   │                 └────────┬─────────┘
                   │                          │
                   └──────────────┬───────────┘
                                  ▼
                    ┌─────────────────────────┐
                    │    Hybrid Retrieval     │
                    │                         │
                    │ Semantic Search + BM25  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                       ┌──────────────────┐
                       │   RRF Fusion     │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │ Cross-Encoder    │
                       │   Reranking      │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Confidence     │
                       │    Validation    │
                       └────────┬─────────┘
                                │
                     ┌──────────┴──────────┐
                     │                     │
                     ▼                     ▼
              Enough Evidence        Insufficient Evidence
                     │                     │
                     ▼                     ▼
              LLM Generation         Safe Refusal
                     │
                     ▼
              Answer + Sources
````

---

# 🔄 Retrieval Pipeline

When a user asks a question, the system follows this process:

1. The user submits a question through the Next.js chat interface.
2. The request is sent to the FastAPI retrieval service.
3. The system performs **semantic vector search** using embeddings and ChromaDB.
4. **BM25 keyword search** retrieves keyword-relevant chunks.
5. Results are combined using **Reciprocal Rank Fusion (RRF)**.
6. A **cross-encoder reranker** ranks the retrieved chunks by relevance.
7. A **confidence check** determines whether sufficient evidence exists.
8. If sufficient evidence is found, relevant context is sent to the LLM.
9. The LLM generates an answer grounded in the retrieved documents.
10. The frontend displays the answer with document sources and page numbers.

If sufficient evidence is not found, the assistant returns a safe response instead of generating an unsupported answer.

---

# 📄 Uploaded Document Pipeline

Users can also upload a PDF directly through the UI.

The uploaded document follows this flow:

```text
PDF Upload
    ↓
Text Extraction
    ↓
Document Chunking
    ↓
Quality Filtering
    ↓
Embedding Generation
    ↓
Separate ChromaDB Collection
    +
BM25 Index
    ↓
Hybrid Retrieval
    ↓
Reranking
    ↓
Confidence Validation
    ↓
Grounded Answer
```

Each uploaded document receives its own vector collection, allowing questions to be answered specifically from that document.

---

# 🛠️ Tech Stack

## Frontend

* Next.js 14
* React
* TypeScript
* CSS

## Backend

* FastAPI
* Python
* Pydantic

## Retrieval & AI

* ChromaDB
* Sentence Transformers
* BM25
* Cross-Encoder Reranking
* Hybrid Retrieval
* Reciprocal Rank Fusion (RRF)
* OpenRouter LLM API

## Infrastructure

* Docker
* Docker Compose

---

# 📂 Project Structure

```text
ai-knowledge-assistant/
│
├── frontend/                     # Next.js frontend
│   ├── app/
│   │   ├── api/
│   │   ├── globals.css
│   │   └── page.tsx
│
├── retrieval-service/            # FastAPI backend
│   └── app/
│       ├── embeddings/           # Embedding model
│       ├── generation/           # LLM generation
│       ├── indexing/             # Index quality checks
│       ├── ingestion/            # PDF extraction and chunking
│       ├── keyword_search/       # BM25 retrieval
│       ├── pipeline/             # RAG pipelines
│       ├── reranking/            # Cross-encoder reranking
│       ├── retrieval/            # Retrieval and confidence logic
│       └── vector_store/         # ChromaDB integration
│
├── data/                         # Knowledge base documents
├── config/
├── eval/
│
├── docker-compose.yml
└── README.md
```

---

# 🚀 Running the Project

## Prerequisites

Make sure you have installed:

* Docker
* Docker Compose

---

## Clone the Repository

```bash
git clone <your-repository-url>
cd ai-knowledge-assistant
```

---

## Configure Environment Variables

Create the environment file for the retrieval service:

```bash
cp retrieval-service/.env.example retrieval-service/.env
```

Add your OpenRouter API credentials:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct
```

Configure the frontend environment if required:

```env
RETRIEVAL_SERVICE_URL=http://localhost:8000
```

---

## Start the Application

```bash
docker compose up --build
```

Once running:

* Frontend: `http://localhost:3000`
* Retrieval API: `http://localhost:8000`
* API Docs: `http://localhost:8000/docs`

---

# 💬 Example Questions

You can ask questions such as:

* What is sequential search?
* Explain Euclid's algorithm for finding GCD.
* What is Big O notation?
* What are the types of algorithms?
* Explain bubble sort.

You can also upload a PDF and ask questions specifically about its contents.

---

# 🛡️ Source Grounding and Confidence Validation

The assistant is designed to generate answers based on retrieved document evidence.

After retrieval and reranking, the system evaluates whether the retrieved chunks provide sufficient evidence.

### 🟢 Grounded Answer

When relevant evidence is available, the assistant generates an answer and displays the supporting sources.

### 🔴 Not Enough Information

When the retrieval evidence is insufficient, the system avoids generating an unsupported answer.

This helps reduce hallucinations and makes the system's behavior more transparent.

---

# 🐳 Docker Services

The application consists of two main services.

## Frontend

* Next.js application
* Interactive chat interface
* PDF upload interface
* Runs on port `3000`

## Retrieval Service

* FastAPI application
* Handles PDF processing
* Semantic retrieval
* BM25 retrieval
* Hybrid search
* Reranking
* Confidence validation
* LLM answer generation
* Runs on port `8000`

Docker Compose manages communication between the services.

---

# 🎯 Current Capabilities

* ✅ PDF document processing
* ✅ Dynamic PDF uploads
* ✅ Document chunking
* ✅ Vector embeddings
* ✅ ChromaDB vector storage
* ✅ Semantic retrieval
* ✅ BM25 keyword retrieval
* ✅ Hybrid search
* ✅ Reciprocal Rank Fusion
* ✅ Cross-encoder reranking
* ✅ Retrieval confidence validation
* ✅ Grounded answer generation
* ✅ Safe refusal for insufficient evidence
* ✅ Source citations
* ✅ Original PDF filename preservation
* ✅ Grouped document sources
* ✅ Copy answer functionality
* ✅ Interactive Next.js chat interface
* ✅ FastAPI REST API
* ✅ Dockerized application

---

# 🔮 Future Improvements

* Conversation memory
* Streaming responses
* Support for multiple uploaded documents
* Retrieval evaluation metrics
* Authentication and user accounts
* Persistent user knowledge bases
* Improved citation highlighting
* Support for additional document formats

---

## 👩‍💻 Author

**Inchara N K**

---

⭐ If you found this project interesting, consider giving the repository a star!




