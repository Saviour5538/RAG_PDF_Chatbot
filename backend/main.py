from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from backend.rag import RAG
from backend.pdf_loader import extract_text_from_pdf
from backend.text_splitter import split_text
from backend.vector_store import add_documents
from backend.database import log_chat
from pydantic import BaseModel
import shutil
import os
import json

# -------------------------
# App + RAG Init
# -------------------------
app = FastAPI()
rag = RAG()

UPLOAD_DIR = "backend/data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------------
# Request Schema
# -------------------------
class ChatRequest(BaseModel):
    question: str
    history: list[str] = []

# -------------------------
# NORMAL CHAT (Non-Streaming)
# -------------------------
@app.post("/ask")
def ask_question(payload: ChatRequest):
    answer = rag.ask(payload.question, payload.history)

    # 🧠 Log to Neon PostgreSQL
    log_chat(
        question=payload.question,
        answer=answer,
        context="\n".join(payload.history)
    )

    return {"answer": answer}

# -------------------------
# STREAMING CHAT (SSE)
# -------------------------
@app.post("/ask_stream")
def ask_stream(payload: ChatRequest):
    def event_generator():
        full_answer = ""

        for token in rag.stream_answer(payload.question, payload.history):
            full_answer += token
            yield f"data: {json.dumps({'token': token})}\n\n"

        # 🧠 Log full response after stream completes
        log_chat(
            question=payload.question,
            answer=full_answer,
            context="\n".join(payload.history)
        )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )

# -------------------------
# PDF UPLOAD + INGESTION
# -------------------------
@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)
    chunks = split_text(text)

    add_documents(chunks)

    return {
        "status": "success",
        "filename": file.filename,
        "chunks_added": len(chunks)
    }
