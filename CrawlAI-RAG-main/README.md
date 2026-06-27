# 🕷️ CrawlAI RAG — AI Website Chatbot

> Crawl any website and ask questions using AI — powered by RAG (Retrieval Augmented Generation)

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![LangChain](https://img.shields.io/badge/LangChain-RAG-orange)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-purple)

---

## ✨ Features

- 🌐 Crawl any website using Playwright (JS rendering supported)
- 🧠 Embed content using HuggingFace sentence-transformers
- 💾 Store vectors in ChromaDB
- 💬 Ask questions in a chat-style UI
- ⚡ Answers powered by Groq LLaMA 3.3 70B
- 📱 Mobile + Desktop friendly HTML/CSS/JS frontend
- 🕐 Recent sites history (localStorage)
- 📋 Copy answer button
- 📊 Pages scraped & chunks created stats

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/subasreebhoopesh/RAG-AI-WEBSITE-CHATBOT.git
cd RAG-AI-WEBSITE-CHATBOT
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 4. Setup environment variables
```bash
# Create .env file and add your Groq API key
# Get free API key from https://console.groq.com
GROQ_API_KEY=your_groq_api_key_here
```

### 5. Run the backend
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### 6. Open the UI
Open your browser and go to:
```
http://127.0.0.1:8000/ui
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | FastAPI (Python) |
| Crawler | Playwright |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Vector DB | ChromaDB |
| LLM | Groq — LLaMA 3.3 70B |
| RAG Pipeline | LangChain |

---

## 📁 Project Structure

```
CrawlAI-RAG/
├── main.py              # FastAPI backend
├── app.py               # Streamlit frontend (legacy)
├── index.html           # HTML/CSS/JS frontend (main)
├── requirements.txt
├── .env.example
├── scraper/
│   └── crawler.py       # Playwright web crawler
└── rag/
    ├── chunker.py        # Text chunking
    ├── vectorstore.py    # ChromaDB vector store
    └── qa.py             # QA chain with Groq LLM
```

---

## 💡 Usage

1. Open `http://127.0.0.1:8000/ui`
2. Enter any website URL (e.g. `https://quotes.toscrape.com`)
3. Click **Index** and wait for crawling to complete
4. Go to **Ask** tab
5. Ask anything about the website!

---

## ⚠️ Notes

- `.env` file is gitignored — never commit your API key
- Google Search URLs cannot be crawled
- Large websites may take 1-2 minutes to index
- Free Groq API key available at [console.groq.com](https://console.groq.com)

---

Made with ❤️ for Hackathon
