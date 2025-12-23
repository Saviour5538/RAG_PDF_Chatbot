from backend.vector_store import load_or_create_faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class RAG:
    def __init__(self):
        self.index, self.docs = load_or_create_faiss()

        self.embed_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")
        self.gen_model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")

        self.device = torch.device("cpu")
        self.gen_model.to(self.device)

    def retrieve(self, query, top_k=3):
        query_emb = self.embed_model.encode([query])
        scores, ids = self.index.search(query_emb, top_k)

        return [self.docs[i] for i in ids[0] if i < len(self.docs)]

    def ask(self, question, history=None):
        if history is None:
            history = []

        retrieved_docs = self.retrieve(question)
        if not retrieved_docs:
            retrieved_docs = ["No relevant documents found."]

        history_text = "\n".join(history[-6:])

        prompt = f"""
You are a helpful assistant.

Conversation so far:
{history_text}

Context from documents:
{' '.join(retrieved_docs)[:1500]}

User question:
{question}

Answer clearly and concisely:
"""

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True).to(self.device)

        with torch.no_grad():
            outputs = self.gen_model.generate(inputs["input_ids"], max_length=250)

        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def stream_answer(self, question, history=None):
        if history is None:
            history = []

        retrieved_docs = self.retrieve(question)
        if not retrieved_docs:
            retrieved_docs = ["No relevant documents found."]

        history_text = "\n".join(history[-6:])

        prompt = f"""
You are a helpful assistant.

Conversation so far:
{history_text}

Context from documents:
{' '.join(retrieved_docs)[:1500]}

User question:
{question}

Answer:
"""

        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True).to(self.device)

        with torch.no_grad():
            outputs = self.gen_model.generate(
                inputs["input_ids"],
                max_length=300,
                do_sample=False
            )

        decoded_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        for word in decoded_text.split():
            yield word + " "
