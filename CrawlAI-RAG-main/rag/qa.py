# rag/qa.py

from urllib.parse import urlparse
from typing import List
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from flashrank import Ranker, RerankRequest
from pydantic import Field


class RerankedRetriever(BaseRetriever):
    vectordb: object = Field(exclude=True)
    ranker: object = Field(exclude=True)
    k: int = 25
    top_n: int = 8

    class Config:
        arbitrary_types_allowed = True

    def _get_relevant_documents(self, query: str) -> List[Document]:
        docs = self.vectordb.similarity_search(query, k=self.k)
        passages = [{"id": i, "text": d.page_content} for i, d in enumerate(docs)]
        rerank_req = RerankRequest(query=query, passages=passages)
        results = self.ranker.rerank(rerank_req)
        top_ids = [r["id"] for r in results[:self.top_n]]
        return [docs[i] for i in top_ids]


PROMPT_TEMPLATE = """You are SiteGPT — an intelligent web research assistant. Your job is to read crawled website content and answer user questions accurately, clearly, and helpfully.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CRAWLED WEBSITE CONTENT:
{context}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

USER QUESTION: {question}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INSTRUCTIONS:
1. Answer ONLY using the crawled content above — never use outside knowledge.
2. Be concise but complete (3–6 sentences ideal).
3. If the question asks for a link or URL, find it in the "Links Found" section and include it directly.
4. If the question asks about projects or portfolio, look for sections like "Featured Projects", "PERSONAL PROJECT", or project cards.
5. If the answer is NOT found in the content, say: "I couldn't find that information on this website."
6. Never repeat the question in your answer.
7. Format your answer cleanly — use bullet points for lists, bold key terms.
8. If the user greets (hi, hello, hey), respond warmly and tell them what they can ask about this website.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ANSWER:"""


def get_qa_chain(website_url: str, base_dir="vector_db"):
    domain = urlparse(website_url).netloc.replace(".", "_")
    persist_dir = f"{base_dir}/{domain}"

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )

    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.2
    )

    ranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2", cache_dir=".cache")
    retriever = RerankedRetriever(vectordb=vectordb, ranker=ranker)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=PROMPT_TEMPLATE
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
