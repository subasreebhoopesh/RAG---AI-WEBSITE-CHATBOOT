# rag/vectorstore.py

import os
import time
from urllib.parse import urlparse
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


def create_vectorstore(chunks, website_url: str, base_dir="vector_db"):
    domain = urlparse(website_url).netloc.replace(".", "_")
    persist_dir = os.path.join(base_dir, domain)
    
    # Clean up existing vector store to avoid duplicates/stale data
    if os.path.exists(persist_dir):
        import shutil
        try:
            shutil.rmtree(persist_dir)
        except PermissionError:
            # File might be locked by another process, wait and retry
            time.sleep(2)
            try:
                shutil.rmtree(persist_dir)
            except PermissionError:
                pass  # Continue anyway, Chroma will handle existing data

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=persist_dir
    )

    return persist_dir
