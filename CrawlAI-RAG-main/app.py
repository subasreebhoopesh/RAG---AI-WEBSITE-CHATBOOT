import streamlit as st
import requests
import time
import threading

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Crawl AI RAG",
    layout="centered"
)

# ---------- Button font styling ----------
st.markdown(
    """
    <style>
    div.stButton > button {
        font-size: 0.85rem;
        padding: 0.5rem 0.5rem;
        text-align: left;
        white-space: normal;
        line-height: 1.2;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("CrawlAI RAG")
st.caption("Crawl websites, index content, and ask questions")

# =====================================================
# 1. INDEX WEBSITE
# =====================================================
st.subheader("1. Index a Website")

with st.form("ingest_form"):
    website_url = st.text_input(
        "Enter website URL",
        placeholder="https://example.com"
    )
    submit_ingest = st.form_submit_button("Index Website")

if submit_ingest:
    if not website_url:
        st.warning("Please enter a website URL")
    elif not website_url.startswith("http://") and not website_url.startswith("https://"):
        st.error("❌ Invalid URL! Must start with `http://` or `https://`")
        st.info("✅ Example: `https://quotes.toscrape.com`")
    elif "google.com/search" in website_url:
        st.error("❌ Google Search URLs cannot be crawled!")
        st.info("✅ Enter a direct website URL like `https://www.geeksforgeeks.org`")
    else:
        progress = st.progress(0.0)
        percent = st.empty()
        status = st.empty()

        state = {"done": False, "response": None, "error": None}

        def update(p, msg):
            progress.progress(min(p / 100.0, 1.0))
            percent.markdown(f"**Progress: {p:.2f}%**")
            status.text(msg)

        def run_backend():
            try:
                state["response"] = requests.post(
                    f"{BACKEND_URL}/ingest",
                    params={"url": website_url},
                    timeout=300
                )
            except Exception as e:
                state["error"] = str(e)
            state["done"] = True

        threading.Thread(target=run_backend, daemon=True).start()

        update(5, "🚀 Launching headless browser...")
        time.sleep(0.3)
        update(15, "🌐 Rendering website with JavaScript...")
        time.sleep(0.3)
        update(28, "🔍 Crawling internal pages...")
        time.sleep(0.3)
        update(42, "📄 Extracting visible content...")
        time.sleep(0.3)
        update(55, "✂️ Chunking text content...")
        time.sleep(0.3)

        current = 60.0
        stages = [
            (68, "🧠 Generating embeddings..."),
            (75, "💾 Saving to vector store..."),
            (82, "🔗 Indexing chunks..."),
            (88, "⚡ Finalizing index..."),
            (93, "🔄 Almost done..."),
        ]
        stage_idx = 0

        while not state["done"]:
            if stage_idx < len(stages):
                target, msg = stages[stage_idx]
                if current < target:
                    current = min(current + 2.5, target)
                    update(current, msg)
                else:
                    stage_idx += 1
            else:
                # Slowly inch toward 97 after all stages
                if current < 97:
                    current = min(current + 0.5, 97)
                update(current, "⏳ Processing, please wait...")
            time.sleep(0.2)

        if state["error"]:
            update(100, "❌ Indexing failed")
            st.error(state["error"])
        elif state["response"] and state["response"].status_code == 200:
            update(100, "✅ Indexing complete!")
            st.success("✅ Website indexed successfully!")
        else:
            update(100, "Indexing failed")
            error_msg = "Indexing failed"
            if state["response"]:
                try:
                    error_msg = state["response"].json().get("error", error_msg)
                except Exception:
                    pass
            st.error(error_msg)

st.divider()

# =====================================================
# STATE FOR ANSWER
# =====================================================
if "answer" not in st.session_state:
    st.session_state.answer = None

def ask_backend(question: str):
    with st.spinner("Generating answer"):
        try:
            res = requests.post(
                f"{BACKEND_URL}/ask",
                params={"question": question},
                timeout=120
            )
            if res.status_code == 200:
                st.session_state.answer = res.json().get("answer", "")
            else:
                st.session_state.answer = "Failed to get answer from backend"
        except Exception as e:
            st.session_state.answer = str(e)

# =====================================================
# 2. QUICK QUESTIONS
# =====================================================
st.subheader("2. Quick Questions")

common_questions = [
    "What is this website about and what is its primary purpose?",
    "Who is the primary owner or creator of this website?",
]

cols = st.columns(2)

for idx, q in enumerate(common_questions):
    with cols[idx % 2]:
        with st.container(border=True):
            if st.button(q, use_container_width=True, key=f"q_{idx}"):
                ask_backend(q)

st.divider()

# =====================================================
# 3. ASK YOUR OWN QUESTION
# =====================================================
st.subheader("3. Ask Your Own Question")

with st.form("ask_form"):
    user_question = st.text_input(
        "Ask something about the website",
        placeholder="Type your question here"
    )
    submit_ask = st.form_submit_button("Ask")

if submit_ask:
    if not user_question:
        st.warning("Please enter a question")
    else:
        ask_backend(user_question)

st.divider()

# =====================================================
# 4. ANSWER (ALWAYS AT BOTTOM)
# =====================================================
if st.session_state.answer:
    st.markdown("### Answer")
    st.write(st.session_state.answer)
