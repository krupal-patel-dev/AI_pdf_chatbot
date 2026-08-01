# 📄 AI PDF Chatbot (Mini RAG)

This is a simple AI PDF Chatbot built using Python, Streamlit, LangChain, FAISS, and OpenAI.

The application allows users to upload a PDF file and ask questions about its content. Instead of sending the entire PDF to the LLM, it uses the RAG (Retrieval-Augmented Generation) approach to retrieve only the most relevant information before generating the answer.

---

## Features

- Upload PDF documents
- Extract text from PDF pages
- Split text into smaller chunks
- Generate OpenAI embeddings
- Store embeddings using FAISS
- Ask questions in natural language
- Retrieve the most relevant chunks
- Generate answers using OpenAI GPT
- Display source references
- Simple Streamlit chat interface

---

## Tech Stack

- Python
- Streamlit
- LangChain
- OpenAI
- FAISS
- PyPDF
- Python Dotenv

---

## Project Flow

```
Upload PDF
      ↓
Read PDF
      ↓
Extract Text
      ↓
Split into Chunks
      ↓
Generate Embeddings
      ↓
Store in FAISS
      ↓
Ask Question
      ↓
Similarity Search
      ↓
Retrieve Relevant Chunks
      ↓
Send Context + Question to GPT
      ↓
Generate Answer
      ↓
Show Answer + Sources
```

---

## Project Structure

```
ai-pdf-study-assistant/
│
├── app.py
├── .env
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── vector_store.py
│   └── rag_chain.py
│
├── data/
├── faiss_indexes/
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
```

Go to the project folder

```bash
cd ai-pdf-study-assistant
```

Create virtual environment

```bash
python3.12 -m venv .venv
```

Activate virtual environment

macOS / Linux

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

Install all dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variable

Create a `.env` file.


```

---

## Run the Project

```bash
streamlit run app.py
```

Open your browser:

```
http://localhost:8501
```

---

## How It Works

1. Upload a PDF document.
2. The application extracts text from all pages.
3. The text is divided into smaller chunks.
4. OpenAI creates embeddings for each chunk.
5. Embeddings are stored in a FAISS vector database.
6. User asks a question.
7. FAISS finds the most relevant chunks.
8. The retrieved chunks are sent to the OpenAI model.
9. The chatbot generates an answer with source references.

---

## Future Improvements

- Support multiple PDFs
- Save chat history
- OCR support for scanned PDFs
- Better UI
- Docker deployment
- Cloud deployment

---

## Screenshots

### Home Page

(Add screenshot)

### PDF Uploaded

(Add screenshot)

### Chat Interface

(Add screenshot)

### Answer with Sources

(Add screenshot)

---

## Author

**Krupal Patel**

MS Computer Science Student

Interested in AI, LLMs, RAG, LangChain, and AI Agents.