# CrawlAI RAG

<p align="center">
  <img 
    src="https://github.com/user-attachments/assets/4a7ead5e-cf4a-427d-b225-5b853966e0da"
    width="320"
    style="border-radius: 50%;"
  />
</p>


**CrawlAI RAG** is an AI-powered website intelligence platform that allows users to **crawl entire websites, index their content, and ask natural-language questions** using **Retrieval-Augmented Generation (RAG)**.

It transforms static websites into **queryable knowledge bases**.

---

## Key Features

### Website Crawling
- Crawls all internal pages of a website  
- Extracts clean, readable text  

### RAG-Based Question Answering
- Uses vector embeddings + LLM  
- Answers are grounded in website content  
- Minimizes hallucinations  

### Multi-Website Indexing
- Index multiple websites  
- All content stored in a shared vector database  

### Fast & Scalable Backend
- Built with FastAPI  
- ChromaDB for vector storage  

### Modern Frontend
- Built with React + Vite  
- Styled with Tailwind CSS  
- Responsive design with glassmorphism effects  
- Smooth animations with Framer Motion  
- Component-based architecture  

### Secure Configuration
- Environment variables via `.env`  
- API keys are never committed to GitHub  

---

## Tech Stack

| Layer | Technology |
|------|-----------|
| Backend | FastAPI |
| Frontend | React + Vite + Tailwind CSS |
| UI Library | Framer Motion, Lucide Icons |
| HTTP Client | Axios |
| Routing | React Router |
| AI / RAG | LangChain |
| Vector Database | ChromaDB |
| Embeddings | Sentence-Transformers |
| LLM | Groq (LLaMA 3.3 70B) |
| Web Scraping | BeautifulSoup4 & Playwright |
| Configuration | python-dotenv |

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- Groq API key

### Backend Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd CrawlAI-RAG-main
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables**
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

4. **Start the backend server**
```bash
python main.py
```
The backend will run on `http://127.0.0.1:8000`

### Frontend Setup

1. **Navigate to the frontend directory**
```bash
cd frontend
```

2. **Install Node dependencies**
```bash
npm install
```

3. **Start the development server**
```bash
npm run dev
```
The frontend will run on `http://localhost:5173`

## Usage Guide

### 1. Index a Website
1. Navigate to the **Index Website** page
2. Enter a website URL (e.g., `https://example.com`)
3. Click **Index Website**
4. Wait for the indexing process to complete
5. Website content is crawled, chunked, and embedded

### 2. Ask Questions
1. Navigate to the **Ask Questions** page
2. Use quick questions or type your own question
3. Click **Send** or press Enter
4. Get AI-powered answers based on indexed content

Example questions:
- What is this website about?
- List all services mentioned
- Who is the author?

The system returns **accurate, grounded answers** based only on the indexed website content.

---

## How It Works

1. Website is crawled and text is extracted  
2. Text is split into manageable chunks  
3. Embeddings are generated and stored in ChromaDB  
4. User query retrieves the most relevant chunks  
5. LLM generates an answer using retrieved context  

This is **true Retrieval-Augmented Generation (RAG)**.

---

## Use Cases

- Website documentation Q&A  
- Internal knowledge bases  
- Research and analysis  
- Client website intelligence  
- Portfolio / demo RAG application  

---

## Author

**CrawlAI RAG**  
Built by **Ankit Kumar Nayak**

---

## Support

If you like this project:
- Give it a **star**
- Fork it
- Contribute or suggest improvements
