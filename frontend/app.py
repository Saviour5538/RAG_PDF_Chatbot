import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="RAG PDF Chatbot",
    page_icon="📄",
    layout="wide"
)

st.title("📄 RAG PDF Chatbot")

# -----------------------------
# Sidebar: PDF Upload
# -----------------------------
st.sidebar.header("📤 Upload PDF")

uploaded_file = st.sidebar.file_uploader(
    "Upload a PDF file",
    type=["pdf"]
)

if uploaded_file:
    with st.spinner("Uploading & processing PDF..."):
        response = requests.post(
            f"{API_URL}/upload_pdf",
            files={"file": uploaded_file}
        )

    if response.status_code == 200:
        data = response.json()
        st.sidebar.success(
            f"✅ Uploaded {data['filename']}\nChunks added: {data['chunks_added']}"
        )
    else:
        st.sidebar.error("❌ PDF upload failed")

# -----------------------------
# Chat UI
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask questions about your PDFs...")

if user_input:
    # Store user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Assistant response (STREAMING)
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        streamed_answer = ""

        history = [
            f"{m['role']}: {m['content']}"
            for m in st.session_state.messages[:-1]
        ]

        # 🔴 STREAM REQUEST
        with requests.post(
            f"{API_URL}/ask_stream",
            json={
                "question": user_input,
                "history": history
            },
            stream=True
        ) as response:

            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        decoded = line.decode("utf-8")
                        if decoded.startswith("data:"):
                            token = json.loads(decoded[5:])["token"]
                            streamed_answer += token
                            response_placeholder.markdown(streamed_answer)
            else:
                streamed_answer = "❌ Streaming error"
                response_placeholder.markdown(streamed_answer)

    # Store assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": streamed_answer}
    )
