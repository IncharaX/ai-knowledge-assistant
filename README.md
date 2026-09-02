# 🤖 AI Knowledge Assistant

An intelligent **Retrieval-Augmented Generation (RAG)** application that allows users to upload PDF documents and ask questions based on their content.

The assistant retrieves relevant information from the uploaded document and generates **grounded answers with source and page citations**, helping reduce hallucinations.

---

## 🚀 Live Demo

🔗 **Live Application:** https://airy-purpose-production-8884.up.railway.app/

---

## ✨ Features

- 📄 Dynamic PDF upload
- 🔍 PDF text extraction
- ✂️ Intelligent document chunking
- 🧠 Vector embeddings using Sentence Transformers
- 🗄️ ChromaDB vector storage
- 🔎 Semantic search
- 🔤 BM25 keyword retrieval
- 🔀 Hybrid search
- 📊 Reciprocal Rank Fusion (RRF)
- 🎯 Cross-encoder reranking
- ✅ Retrieval confidence validation
- 🤖 Grounded LLM answer generation
- 🛡️ Hallucination and refusal handling
- 📚 Source citations
- 📄 Page number citations
- 💬 Interactive chat interface
- 📋 Copy answer functionality
- 🧹 Clear chat functionality
- 🐳 Dockerized application
- ☁️ Deployed on Railway

---

## 🏗️ Architecture

```text
                ┌──────────────────┐
                │   User Uploads   │
                │       PDF        │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │  PDF Extraction  │
                │     PyMuPDF      │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Document Chunking│
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Vector Embeddings│
                │SentenceTransformers│
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │     ChromaDB     │
                │  Vector Storage  │
                └────────┬─────────┘
                         │
                         ▼
        ┌────────────────┴────────────────┐
        ▼                                 ▼
┌─────────────────┐              ┌─────────────────┐
│ Semantic Search │              │  BM25 Search    │
└────────┬────────┘              └────────┬────────┘
         └──────────────┬─────────────────┘
                        ▼
              ┌──────────────────┐
              │  Hybrid Search   │
              │       RRF        │
              └────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │ Cross-Encoder    │
              │    Reranking     │
              └────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │ Confidence Check │
              └────────┬─────────┘
                       ▼
              ┌──────────────────┐
              │ Grounded Answer  │
              │       +          │
              │ Source Citations │
              └──────────────────┘
````

---

## 🛠️ Tech Stack

### Frontend

* Next.js
* React
* TypeScript

### Backend / Retrieval Service

* FastAPI
* Python
* Uvicorn

### AI & Retrieval

* Sentence Transformers
* ChromaDB
* BM25
* Cross-Encoder Reranking

### Document Processing

* PyMuPDF

### Deployment

* Docker
* Railway

---

## 📂 Project Structure

```text
ai-knowledge-assistant/
│
├── frontend/
│   ├── app/
│   ├── public/
│   └── ...
│
├── retrieval-service/
│   ├── app/
│   │   ├── ingestion/
│   │   ├── retrieval/
│   │   └── ...
│   │
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
└── README.md
```

---

## 🔄 How It Works

### 1. Upload a PDF

The user uploads a PDF document through the web interface.

### 2. Extract Text

The application extracts text from the PDF while preserving page information.

### 3. Chunk the Document

The extracted content is divided into smaller chunks for efficient retrieval.

### 4. Generate Embeddings

Each document chunk is converted into vector embeddings using Sentence Transformers.

### 5. Store in ChromaDB

The embeddings and document metadata are stored in ChromaDB.

### 6. Ask a Question

The user asks a question about the uploaded document.

### 7. Hybrid Retrieval

The system performs:

* Semantic vector search
* BM25 keyword search

The results are combined using **Reciprocal Rank Fusion (RRF)**.

### 8. Reranking

A Cross-Encoder reranks the retrieved results to identify the most relevant context.

### 9. Confidence Validation

The system checks whether enough relevant information exists before generating an answer.

### 10. Grounded Answer Generation

The final answer is generated only from the retrieved document context.

The response includes:

* Source document
* Relevant page numbers

---

## 🛡️ Hallucination Handling

The AI Knowledge Assistant is designed to avoid answering questions that are not sufficiently supported by the uploaded document.

If relevant information cannot be retrieved, the system responds appropriately instead of generating unsupported information.

---

## 💻 Running Locally

### Clone the repository

```bash
git clone <https://github.com/IncharaX/ai-knowledge-assistant>
cd ai-knowledge-assistant
```

### Start using Docker

```bash
docker compose up --build
```

Then open the application in your browser.

---

## ☁️ Deployment

The application is containerized using Docker and deployed on **Railway**.

🔗 **Live Demo:** [https://airy-purpose-production-8884.up.railway.app/](https://airy-purpose-production-8884.up.railway.app/)

---

## 🎯 Key Concepts Demonstrated

This project demonstrates practical implementation of:

* Retrieval-Augmented Generation (RAG)
* Vector databases
* Embeddings
* Semantic search
* Keyword search
* Hybrid retrieval
* Reciprocal Rank Fusion
* Cross-Encoder reranking
* Grounded AI responses
* Source attribution
* Confidence-based retrieval
* Docker containerization
* Cloud deployment

---

## 👩‍💻 Author

**Inchara N K**

---

⭐ If you found this project interesting, feel free to star the repository!


