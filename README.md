# 🤖 AI Knowledge Assistant

A full-stack, production-deployed **Retrieval-Augmented Generation (RAG)** application that allows users to upload PDF documents and ask AI-powered questions grounded strictly in the uploaded content.

The system combines **semantic search**, **BM25 keyword search**, **Reciprocal Rank Fusion (RRF)**, **cross-encoder reranking**, and **retrieval confidence validation** to produce reliable answers with document sources and page citations.

---

## 🚀 Live Demo

🌐 **Try the application:**

https://airy-purpose-production-8884.up.railway.app/

---

## ✨ Features

### 📄 Dynamic PDF Upload

- Upload PDF documents directly through the UI
- Extract text dynamically from uploaded PDFs
- Automatically chunk document content
- Create embeddings for semantic retrieval
- Ask questions specifically about the uploaded document

### 🔍 Advanced Retrieval Pipeline

- 🧠 Semantic vector search using embeddings
- 🔎 BM25 keyword search
- 🔀 Reciprocal Rank Fusion (RRF)
- 🎯 Cross-encoder reranking
- 📊 Retrieval confidence validation

### 🤖 Grounded AI Answers

- Answers generated only from retrieved document context
- Refuses questions when sufficient evidence is unavailable
- Reduces hallucinated responses
- Displays document sources and page numbers

### 💻 Full-Stack Application

- Interactive chat interface
- PDF upload interface
- Active document indicator
- Source citations
- Copy answer functionality
- Clear chat functionality

### 🚀 Deployment

- Dockerized services
- Docker Compose support
- Railway cloud deployment
- Separate frontend and backend services
- Private service networking
- Health monitoring

---

# 🏗️ Architecture

```text
                        ┌──────────────────────┐
                        │      Next.js UI      │
                        │                      │
                        │  Upload PDF / Ask    │
                        │      Question        │
                        └──────────┬───────────┘
                                   │
                                   ▼
                        ┌──────────────────────┐
                        │      FastAPI         │
                        │  Retrieval Service   │
                        └──────────┬───────────┘
                                   │
                  ┌────────────────┴────────────────┐
                  │                                 │
                  ▼                                 ▼
        ┌──────────────────┐              ┌──────────────────┐
        │   PDF Upload     │              │ Knowledge Base   │
        │                  │              │                  │
        │ Extract → Chunk  │              │ Existing Docs    │
        │ → Embed          │              │                  │
        └────────┬─────────┘              └────────┬─────────┘
                 │                                 │
                 └────────────────┬────────────────┘
                                  ▼
                     ┌────────────────────────┐
                     │   Hybrid Retrieval     │
                     │                        │
                     │ Semantic Search        │
                     │          +             │
                     │ BM25 Keyword Search    │
                     └────────────┬───────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │      RRF Fusion        │
                     └────────────┬───────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │ Cross-Encoder Reranker │
                     └────────────┬───────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │ Retrieval Confidence   │
                     └────────────┬───────────┘
                                  │
                         Sufficient Evidence?
                           │             │
                         YES             NO
                           │             │
                           ▼             ▼
                    ┌─────────────┐   Refuse
                    │     LLM     │   Answer
                    │ Generation  │
                    └──────┬──────┘
                           │
                           ▼
                 Answer + Sources + Pages
````

---

# 🔄 Retrieval Pipeline

When a user asks a question about a document, the application follows this process:

1. **User uploads a PDF** or uses the existing knowledge base.
2. The document text is extracted and divided into chunks.
3. Embeddings are generated for semantic search.
4. The user submits a question.
5. **Semantic retrieval** finds conceptually relevant chunks.
6. **BM25 retrieval** finds keyword-relevant chunks.
7. Results are combined using **Reciprocal Rank Fusion (RRF)**.
8. A **cross-encoder reranker** ranks the most relevant chunks.
9. **Retrieval confidence validation** checks whether enough evidence exists.
10. If confidence is insufficient, the assistant refuses to answer.
11. If sufficient evidence exists, the retrieved context is sent to the LLM.
12. The application displays a grounded answer with **sources and page numbers**.

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
* Uvicorn

## AI & Retrieval

* ChromaDB
* Sentence Transformers
* BM25
* Cross-Encoder Reranking
* Reciprocal Rank Fusion (RRF)
* OpenRouter LLM API

## Document Processing

* PyMuPDF
* Tiktoken

## Infrastructure

* Docker
* Docker Compose
* Railway

---

# 📂 Project Structure

```text
ai-knowledge-assistant/
│
├── frontend/                     # Next.js frontend
│   ├── app/
│   └── Dockerfile
│
├── retrieval-service/            # FastAPI backend
│   ├── app/
│   │   ├── embeddings/
│   │   ├── generation/
│   │   ├── indexing/
│   │   ├── ingestion/
│   │   ├── keyword_search/
│   │   ├── pipeline/
│   │   ├── reranking/
│   │   ├── retrieval/
│   │   └── vector_store/
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── data/                         # Knowledge base documents
├── assets/                       # Application screenshots
├── config/
├── eval/
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

# 🚀 Running Locally

## Prerequisites

Make sure you have installed:

* Docker
* Docker Compose

---

## Clone the Repository

```bash
git clone <https://github.com/IncharaX/ai-knowledge-assistant>
cd ai-knowledge-assistant
```

---

## Configure Environment Variables

Create the environment file:

```bash
cp retrieval-service/.env.example retrieval-service/.env
```

Add your OpenRouter API credentials:

```env
OPENROUTER_API_KEY=your_actual_openrouter_api_key
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct
```

---

## Start the Application

```bash
docker compose up --build
```

Once running:

* 🌐 Frontend: `http://localhost:3000`
* ⚙️ Retrieval API: `http://localhost:8000`

---

# 💬 Example Questions

Depending on the uploaded document, you can ask questions such as:

* What are the main topics discussed in this document?
* Explain the concept mentioned on page 5.
* What are the different types of flag registers?
* What does YSL stand for?
* Summarize the key points of this document.

The assistant retrieves relevant information before generating an answer.

---

# 📚 Source Grounding

The assistant is designed to answer questions using evidence retrieved from the selected document or knowledge base.

Each grounded answer includes:

* 📄 Document name
* 📖 Relevant page numbers
* 🟢 Grounded answer indicator

If the system cannot find sufficient evidence, it returns:

> **Not enough information**

This prevents the system from confidently answering questions that are unsupported by the available document.

---

# 🐳 Docker Services

The application consists of two services.

## Frontend

* Next.js application
* Runs on port `3000`

## Retrieval Service

* FastAPI application
* Handles PDF processing
* Document chunking
* Embeddings
* Retrieval
* Reranking
* Confidence validation
* LLM answer generation
* Runs on port `8000`

Docker Compose manages communication between the services.

---

# 🌐 Deployment

The application is deployed on **Railway** using separate frontend and backend services.

### Frontend

* Next.js
* Public Railway deployment

### Backend

* FastAPI retrieval service
* PDF processing and RAG pipeline

### Infrastructure

* Docker-based deployment
* Railway private networking between services
* Health monitoring

---

## 🎯 Current Capabilities

- ✅ Dynamic PDF upload
- ✅ PDF text extraction
- ✅ Document chunking
- ✅ Vector embeddings
- ✅ ChromaDB vector storage
- ✅ Semantic retrieval
- ✅ BM25 keyword retrieval
- ✅ Hybrid search
- ✅ Reciprocal Rank Fusion
- ✅ Cross-encoder reranking
- ✅ Retrieval confidence validation
- ✅ Grounded LLM generation
- ✅ Hallucination/refusal handling
- ✅ Source citations
- ✅ Page number citations
- ✅ Interactive chat interface
- ✅ Copy answer functionality
- ✅ Clear chat functionality
- ✅ Dockerized application
- ✅ Railway cloud deployment
- ✅ Production-tested PDF RAG pipeline

---

# 🔮 Future Improvements

* 💬 Conversation memory
* ⚡ Streaming responses
* 📊 Retrieval evaluation metrics
* 🔐 Authentication and user accounts
* 📚 Multiple document collections
* 🔍 Clickable citation highlighting
* 📈 Usage analytics

---

## 👩‍💻 Author

**Inchara N K**

---

⭐ If you found this project interesting, consider giving the repository a star!
