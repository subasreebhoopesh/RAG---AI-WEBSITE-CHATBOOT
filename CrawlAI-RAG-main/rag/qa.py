# rag/qa.py

from urllib.parse import urlparse
from langchain_groq import ChatGroq
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from flashrank import Ranker, RerankRequest


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

    # FlashRank reranker — re-orders retrieved docs by relevance
    ranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2", cache_dir=".cache")

    class RerankedRetriever:
        def __init__(self, vectordb, ranker, k=25, top_n=8):
            self.vectordb = vectordb
            self.ranker = ranker
            self.k = k
            self.top_n = top_n

        def get_relevant_documents(self, query):
            docs = self.vectordb.similarity_search(query, k=self.k)
            passages = [{"id": i, "text": d.page_content} for i, d in enumerate(docs)]
            rerank_req = RerankRequest(query=query, passages=passages)
            results = self.ranker.rerank(rerank_req)
            top_ids = [r["id"] for r in results[:self.top_n]]
            return [docs[i] for i in top_ids]

        def invoke(self, query):
            return self.get_relevant_documents(query)

    retriever = RerankedRetriever(vectordb, ranker)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are CrawlAI — an intelligent web research assistant. Your job is to read crawled website content and answer user questions accurately, clearly, and helpfully.

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
4. If the question asks about projects or portfolio, look for sections like "Featured Projects", "PERSONAL PROJECT", or project cards — prioritize those over casual mentions.
5. If the answer is NOT found in the content, say: "I couldn't find that information on this website."
6. Never repeat the question in your answer.
7. Format your answer cleanly:
   - Use bullet points if listing multiple items.
   - Use plain sentences for single answers.
   - Bold key terms if helpful.
8. If the user greets (hi, hello, hey), respond warmly and tell them what they can ask about this website.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ANSWER:"""
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )

    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.2
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are CrawlAI — an intelligent web research assistant. Your job is to read crawled website content and answer user questions accurately, clearly, and helpfully.

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
4. If the question asks about projects or portfolio, look for sections like "Featured Projects", "PERSONAL PROJECT", or project cards — prioritize those over casual mentions.
5. If the answer is NOT found in the content, say: "I couldn't find that information on this website."
6. Never repeat the question in your answer.
7. Format your answer cleanly:
   - Use bullet points if listing multiple items.
   - Use plain sentences for single answers.
   - Bold key terms if helpful.
8. If the user greets (hi, hello, hey), respond warmly and tell them what they can ask about this website.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ANSWER:"""
    )

    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(search_kwargs={"k": 25}),
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
        return_source_documents=True
    )
