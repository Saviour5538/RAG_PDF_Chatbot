import os
from sqlalchemy import create_engine, Column, Integer, Text, TIMESTAMP
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
from dotenv import load_dotenv

# Load env vars
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Engine (Neon-compatible)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class
Base = declarative_base()

# -----------------------------
# 📦 Chat Logs Table
# -----------------------------
class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    context = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

# -----------------------------
# 🛠️ Create tables (run once)
# -----------------------------
def init_db():
    Base.metadata.create_all(bind=engine)

# -----------------------------
# 🧠 Log chat interaction
# -----------------------------
def log_chat(question, answer, context):
    db = SessionLocal()
    try:
        chat = ChatLog(
            question=question,
            answer=answer,
            context=context
        )
        db.add(chat)
        db.commit()
    finally:
        db.close()
