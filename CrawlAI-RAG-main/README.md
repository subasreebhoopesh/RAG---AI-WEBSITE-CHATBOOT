# 🤖 SiteGPT — AI-Powered Website Chatbot

> Crawl any website and ask questions using RAG, Groq LLaMA3, and ChromaDB

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.138-green)
![ChromaDB](https://img.shields.io/badge/ChromaDB-1.5-purple)
![LangChain](https://img.shields.io/badge/LangChain-1.3-orange)

---

## 📌 Project Description

**SiteGPT** is an AI-powered web chatbot that:
1. **Crawls** any website using Playwright (headless browser)
2. **Indexes** the content into ChromaDB vector store
3. **Answers** questions about the website using Groq LLaMA3 + RAG pipeline

---

## 🚀 Features

- 🌐 **Website Indexing** — Crawl any JS-rendered website
- 💬 **AI Chat** — Ask anything about the indexed website
- ⚡ **Quick Questions** — One-click common queries
- 📊 **Stats Dashboard** — Pages scraped, chunks, overview
- 🌍 **Multi-language** — Get answers in Tamil, Hindi, French, etc.
- 🔔 **Browser Notifications** — Alert when indexing completes
- 🎨 **Custom Avatar** — Personalize your profile
- 📋 **Website Summary** — Auto-generated site summary
- 💡 **Follow-up Questions** — AI-suggested next questions
- 🖼️ **Export Chat** — Download as PDF or Image
- 🎤 **Voice Input** — Ask questions by voice
- 🕐 **History** — Track all indexed sites
- 🌙 **Dark/Light Mode** — Toggle themes

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, Vanilla JS |
| Backend | FastAPI + Uvicorn |
| Web Scraping | Playwright (headless browser) |
| Vector Store | ChromaDB |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| LLM | Groq LLaMA3 (llama-3.3-70b-versatile) |
| RAG Framework | LangChain + LangChain-Classic |
| Reranking | FlashRank (ms-marco-MiniLM-L-12-v2) |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10+
- pip
- A free [Groq API Key](https://console.groq.com)

### 1. Clone the repository
```bash
git clone https://github.com/subasreebhoopesh/RAG---AI-WEBSITE-CHATBOOT.git
cd RAG---AI-WEBSITE-CHATBOOT/CrawlAI-RAG-main
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Playwright browsers
```bash
playwright install chromium
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 5. Run the backend server
```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

### 6. Open the UI
```
http://127.0.0.1:8000/ui
```

---

## 📖 Usage

1. **Enter a website URL** in the Index tab (e.g. `https://quotes.toscrape.com`)
2. Click **Index** — wait for crawling & indexing to complete
3. Go to **Chat** tab and ask any question about the website
4. Use **Quick Questions** for one-click queries
5. Switch between multiple indexed sites using **Switch Site**

---

## 🔑 Dependencies

```
fastapi
uvicorn
langchain
langchain-community
langchain-classic
chromadb
beautifulsoup4
requests
sentence-transformers
streamlit
python-dotenv
playwright
langchain-groq
flashrank
```

---

## 💡 Solution Approach

```
User provides URL
      ↓
Playwright crawls website (JS-rendered)
      ↓
Text extracted → Chunked (400 chars, 50 overlap)
      ↓
HuggingFace Embeddings → ChromaDB vector store
      ↓
User asks question
      ↓
ChromaDB similarity search (top 25 chunks)
      ↓
FlashRank reranking (top 8 chunks)
      ↓
Groq LLaMA3 generates answer via RetrievalQA
      ↓
Answer displayed with typewriter effect
```

### Key Design Decisions:
- **Playwright** over BeautifulSoup for JS-rendered sites
- **FlashRank reranking** for better answer relevance
- **Per-domain vector stores** so multiple sites can be indexed independently
- **Groq LLaMA3** for fast, free LLM inference

---

## 📁 Project Structure

```
CrawlAI-RAG-main/
├── main.py              # FastAPI backend (API endpoints)
├── app.py               # Streamlit UI (alternative)
├── index.html           # Main frontend UI
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── scraper/
│   └── crawler.py       # Playwright web crawler
├── rag/
│   ├── chunker.py       # Text chunking
│   ├── vectorstore.py   # ChromaDB vector store
│   └── qa.py            # RAG QA chain with reranking
└── vector_db/           # Persisted vector stores (gitignored)
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/ui` | Serve frontend UI |
| POST | `/ingest?url=` | Crawl & index a website |
| POST | `/ask?question=` | Ask a question |
| POST | `/summary?url=` | Get website summary |
| POST | `/followup?answer=` | Get follow-up questions |
| GET | `/db-info` | View indexed sites info |

---

## 👤 Author

**Subasree Bhoopesh**
- GitHub: [@subasreebhoopesh](https://github.com/subasreebhoopesh)

---

*© 2025 SiteGPT. Built with ❤️ using RAG + Groq + ChromaDB*
