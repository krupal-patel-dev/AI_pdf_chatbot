# 📄 AI PDF Chatbot (Mini RAG)

A simple AI-powered PDF Question Answering application built using **Python, Streamlit, LangChain, FAISS, and Google Gemini**.

The application allows users to upload a PDF document and ask questions about its content. Instead of sending the entire PDF to the LLM, it follows the **Retrieval-Augmented Generation (RAG)** approach to retrieve only the most relevant information before generating an answer.

---

# 1. Features

- Upload PDF documents
- Extract text from PDF pages
- Split text into smaller chunks
- Generate Gemini embeddings
- Store embeddings in FAISS Vector Database
- Ask questions in natural language
- Retrieve the most relevant document chunks
- Generate answers using Google Gemini
- Display source references
- Simple Streamlit chat interface

---

# 2. Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python |
| UI | Streamlit |
| Framework | LangChain |
| LLM | Google Gemini |
| Embeddings | Gemini Embeddings |
| Vector Database | FAISS |
| PDF Reader | PyPDF |
| Environment | Python Dotenv |

---

# 3. Project Flow

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
User Asks Question
      ↓
Similarity Search
      ↓
Retrieve Relevant Chunks
      ↓
Send Context + Question to Gemini
      ↓
Generate Answer
      ↓
Display Answer + Sources
```

---

# 4. Project Structure

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

# 5. Installation

### Step 1: Clone the repository

```bash
git clone <repository-url>
```

### Step 2: Open the project folder

```bash
cd ai-pdf-study-assistant
```

### Step 3: Create a virtual environment

```bash
python3.12 -m venv .venv
```

### Step 4: Activate the virtual environment

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### Step 5: Install dependencies

```bash
pip install -r requirements.txt
```

---

# 6. Environment Variables

Create a `.env` file in the project folder.

```env
GOOGLE_API_KEY=your_gemini_api_key
```

---

# 7. Run the Project

```bash
streamlit run app.py
```

Open your browser:

```
http://localhost:8501
```

---

# 8. How It Works

1. Upload a PDF document.
2. Read the PDF and extract text from every page.
3. Split the extracted text into smaller chunks.
4. Generate embeddings for every chunk using Gemini.
5. Store embeddings in the FAISS vector database.
6. Ask a question about the uploaded PDF.
7. Perform semantic similarity search.
8. Retrieve the most relevant document chunks.
9. Send the retrieved context and question to Gemini.
10. Generate the final answer.
11. Display the answer along with source references.

---

# 9. Future Improvements

- Support multiple PDF documents
- Save chat history
- OCR support for scanned PDFs
- Better UI/UX
- Docker support
- Cloud deployment
- Conversation memory
- Persistent FAISS database

---

# 10. Screenshots

### Home Page

_Add screenshot here_

---

### PDF Upload

_Add screenshot here_

---

### Chat Interface

_Add screenshot here_

---

### Answer with Sources

_Add screenshot here_

---

# 11. Requirements

- Python 3.12+
- Streamlit
- LangChain
- LangChain Community
- LangChain Google GenAI
- LangChain Text Splitters
- FAISS
- PyPDF
- Python Dotenv

---

# 12. Author

**Krupal Patel**

MS in Computer Science

Interested in Artificial Intelligence, Generative AI, LLMs, RAG, LangChain, and AI Agent Development.