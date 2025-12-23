import faiss
import os
import pickle
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
INDEX_PATH = os.path.join(DATA_DIR, "faiss.index")
DOCS_PATH = os.path.join(DATA_DIR, "docs.pkl")

# 🔒 Load embedding model ONCE
model = SentenceTransformer("all-MiniLM-L6-v2")

# 🔒 Cache index globally
_index = None
_docs = None

def load_or_create_faiss():
    global _index, _docs

    if _index is not None and _docs is not None:
        return _index, _docs

    os.makedirs(DATA_DIR, exist_ok=True)

    if os.path.exists(INDEX_PATH):
        _index = faiss.read_index(INDEX_PATH)
        with open(DOCS_PATH, "rb") as f:
            _docs = pickle.load(f)
    else:
        _index = faiss.IndexFlatL2(384)
        _docs = []

    return _index, _docs

def save_faiss(index, docs):
    faiss.write_index(index, INDEX_PATH)
    with open(DOCS_PATH, "wb") as f:
        pickle.dump(docs, f)

def add_documents(text_chunks):
    index, docs = load_or_create_faiss()

    embeddings = model.encode(text_chunks)
    index.add(embeddings)
    docs.extend(text_chunks)

    save_faiss(index, docs)
