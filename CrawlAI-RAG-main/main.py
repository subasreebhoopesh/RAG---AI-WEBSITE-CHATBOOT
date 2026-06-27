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
