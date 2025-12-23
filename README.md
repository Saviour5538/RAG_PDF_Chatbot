# 📄 RAG PDF Chatbot

An end-to-end **Retrieval-Augmented Generation (RAG) PDF Chatbot** that allows users to upload PDFs and ask intelligent questions using modern NLP techniques.

Built using **FastAPI, FAISS, Sentence Transformers, HuggingFace Transformers, Streamlit**, and **PostgreSQL (Neon)**.

---

## 🚀 Features

- 📤 Upload PDFs and extract text automatically
- 🔍 Semantic search using FAISS vector database
- 🧠 Context-aware answers with RAG
- 💬 Chat memory (conversation-aware)
- ⚡ Streaming responses (token-by-token)
- 🗄️ PostgreSQL (Neon) integration (optional)
- 🎨 Interactive Streamlit UI

---

## 🧱 Tech Stack

- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Embeddings**: Sentence-Transformers (MiniLM)
- **LLM**: FLAN-T5 (HuggingFace)
- **Vector DB**: FAISS
- **Database**: PostgreSQL (Neon)
- **PDF Parsing**: pdfplumber / PyPDF2

---
RAG_project/
│
├── backend/
│ ├── rag.py
│ ├── main.py
│ ├── vector_store.py
│ ├── pdf_loader.py
│ ├── text_splitter.py
│ └── data/
│
├── frontend/
│ └── app.py
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md

⚙️ Setup Instructions

 1️⃣ Clone the repository
 
git clone https://github.com/Saviour5538/RAG_PDF_Chatbot.git
cd RAG_PDF_Chatbot

2️⃣ Create virtual environment

python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Configure environment variables

cp .env.example .env
Fill in your Neon PostgreSQL DATABASE_URL.

## 📂 Project Structure

