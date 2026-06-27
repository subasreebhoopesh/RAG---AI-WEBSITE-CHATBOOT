from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from scraper.crawler import crawl_website
from rag.chunker import chunk_text
from rag.vectorstore import create_vectorstore
from rag.qa import get_qa_chain

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ui")
def serve_ui():
    return FileResponse("index.html")

LAST_WEBSITE_FILE = "last_website.txt"


def load_last_website():
    if os.path.exists(LAST_WEBSITE_FILE):
        with open(LAST_WEBSITE_FILE, "r") as f:
            url = f.read().strip()
            return url if url else None
    return None


def save_last_website(url: str):
    with open(LAST_WEBSITE_FILE, "w") as f:
        f.write(url)


LAST_WEBSITE = load_last_website()


@app.get("/db-info")
def db_info():
    import os
    base = "vector_db"
    info = []
    if os.path.exists(base):
        for domain in os.listdir(base):
            domain_path = os.path.join(base, domain)
            if os.path.isdir(domain_path):
                size = sum(
                    os.path.getsize(os.path.join(dp, f))
                    for dp, dn, filenames in os.walk(domain_path)
                    for f in filenames
                )
                info.append({
                    "domain": domain,
                    "path": domain_path,
                    "size_kb": round(size / 1024, 2)
                })
    return {
        "vector_database": "ChromaDB",
        "storage_location": os.path.abspath(base),
        "indexed_sites": info,
        "total_sites": len(info),
        "current_site": LAST_WEBSITE
    }


@app.get("/")
def root():
    return {"status": "Backend running"}


@app.post("/ingest")
def ingest(url: str):
    global LAST_WEBSITE

    # Validate URL
    if not url.startswith("http://") and not url.startswith("https://"):
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid URL. Please provide a full URL starting with http:// or https://"}
        )

    try:
        pages = crawl_website(url)
        
        if not pages:
            return JSONResponse(
                status_code=400,
                content={"error": "No content could be crawled from this website. The site may be blocking crawlers or took too long to load."}
            )
        
        chunks = chunk_text(pages)
        
        if not chunks:
            return JSONResponse(
                status_code=400,
                content={"error": "No text chunks could be created from the crawled content."}
            )
        
        create_vectorstore(chunks, url)
        LAST_WEBSITE = url
        save_last_website(url)

        return {
            "pages_scraped": len(pages),
            "chunks_created": len(chunks),
            "status": "Website indexed"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Indexing failed: {str(e)}"}
        )


@app.post("/ask")
def ask(question: str):
    if not LAST_WEBSITE:
        return {"answer": "No website indexed yet."}

    qa_chain = get_qa_chain(LAST_WEBSITE)
    result = qa_chain.invoke(question)

    if isinstance(result, dict) and "result" in result:
        return {"answer": result["result"]}

    return {"answer": str(result)}


@app.post("/summary")
def summary(url: str = None):
    site = url or LAST_WEBSITE
    if not site:
        return JSONResponse(status_code=400, content={"error": "No website indexed yet."})
    try:
        qa_chain = get_qa_chain(site)
        result = qa_chain.invoke(
            "Give a structured summary of this website. Include: 1) Website name and purpose, 2) Main topics covered, 3) Key features or services, 4) Target audience. Format clearly with bullet points."
        )
        answer = result["result"] if isinstance(result, dict) and "result" in result else str(result)
        return {"summary": answer, "url": site}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/followup")
def followup(answer: str):
    from langchain_groq import ChatGroq
    try:
        llm = ChatGroq(model_name="llama-3.3-70b-versatile", temperature=0.5)
        prompt = f"""Based on this AI answer about a website, suggest exactly 3 short follow-up questions a user might want to ask next.

Answer: {answer}

Rules:
- Each question must be short (under 10 words)
- Questions must be directly related to the answer
- Return ONLY the 3 questions, one per line, no numbering, no extra text

Questions:"""
        result = llm.invoke(prompt)
        lines = [l.strip() for l in result.content.strip().split("\n") if l.strip()][:3]
        return {"questions": lines}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.post("/compare")
def compare(url1: str, url2: str, question: str = "What is this website about and what are its main features?"):
    try:
        qa1 = get_qa_chain(url1)
        qa2 = get_qa_chain(url2)
        r1 = qa1.invoke(question)
        r2 = qa2.invoke(question)
        a1 = r1["result"] if isinstance(r1, dict) and "result" in r1 else str(r1)
        a2 = r2["result"] if isinstance(r2, dict) and "result" in r2 else str(r2)
        return {
            "question": question,
            "site1": {"url": url1, "answer": a1},
            "site2": {"url": url2, "answer": a2}
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
