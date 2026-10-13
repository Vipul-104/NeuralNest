# 🧠 NeuralNest - Your Personal Knowledge Graph

> Feed it your notes, voice memos, podcasts, and WhatsApp chats. Ask it anything. It answers from *your* brain — not the internet.

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Streamlit](https://img.shields.io/badge/UI-Streamlit-red) ![spaCy](https://img.shields.io/badge/NLP-spaCy-09A3D5) ![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 What is MemoryOS?

MemoryOS is a **multimodal personal knowledge graph engine** that ingests everything you learn — gym notes, podcast insights, study material, WhatsApp conversations — and builds a living, queryable graph of your knowledge.

Unlike ChatGPT or Notion AI, MemoryOS only answers from **your own data**. It knows what *you* know, not what the internet knows.

**Ask it:**
- *"Progressive overload ke baare mein mujhe kya pata hai?"*
- *"What did I learn about transformers last week?"*
- *"Connect my podcast notes on discipline with my fitness notes"*

It finds cross-domain connections you'd never notice manually — your gym notes linking to a stoicism podcast linking to your ML study notes, all under the concept of *consistent effort*.

---

## ✨ Features

- **Multimodal ingestion** — voice memos, text notes, WhatsApp exports, article URLs
- **Auto knowledge graph** — NLP extracts concepts and relationships automatically, no manual linking
- **Hindi / English / Hinglish queries** — ask in whatever language you think in
- **Cross-domain insight detection** — surfaces connections across fitness, learning, podcasts, work
- **Visual graph explorer** — see your knowledge as an interactive node graph
- **100% local & private** — your data never leaves your machine
- **Grows smarter over time** — more inputs = richer connections = better answers

---

## 🛠️ Tech Stack

| Layer | Tech |
|---|---|
| NLP extraction | spaCy (`en_core_web_sm`) |
| Semantic embeddings | `sentence-transformers` (all-MiniLM-L6-v2) |
| Speech transcription | OpenAI Whisper |
| Knowledge graph | NetworkX |
| LLM query layer | Google Gemini 2.5 Flash (free tier) |
| UI | Streamlit |
| Visualisation | Plotly |
| Web scraping | BeautifulSoup4 |

---

## 📁 Project Structure

```
memoryos/
├── app.py                  # Streamlit UI — main entry point
├── ingest.py               # Input pipeline (audio/text/URL/WhatsApp → raw text)
├── extractor.py            # NLP → concept nodes + relationship edges
├── graph_store.py          # NetworkX graph CRUD + pickle persistence
├── query_engine.py         # Semantic search + Gemini LLM answer generation
├── requirements.txt
├── .env                    # API keys (never commit this)
├── data/
│   ├── graph.pkl           # Persisted knowledge graph
│   └── raw/                # Original uploaded files
└── utils/
    └── whisper_helper.py   # Audio transcription helpers
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11
- `ffmpeg` installed on system (for audio transcription)
  - Windows: download from [ffmpeg.org](https://ffmpeg.org/download.html), add to PATH
  - Mac: `brew install ffmpeg`
  - Linux: `sudo apt install ffmpeg`

### 1. Clone the repo
```bash
git clone https://github.com/your-username/memoryos.git
cd memoryos
```

### 2. Create virtual environment
```bash
py -3.11 -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
pip install --no-cache-dir openai-whisper
pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu
python -m spacy download en_core_web_sm
```

### 4. Add your Gemini API key
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your-key-here
```
Get a free key (no credit card) at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

### 5. Run
```bash
streamlit run app.py
```
Opens at `http://localhost:8501`

---

## 🧪 How to Use

### Step 1 — Feed your learning (sidebar)
Choose input type and add a label (e.g. `gym_june14`, `huberman_podcast`):

| Input type | What to provide |
|---|---|
| Text / Notes | Paste directly in the text area |
| Voice memo | Upload `.mp3` / `.wav` / `.m4a` |
| Article URL | Paste any article link |
| WhatsApp export | Upload `_chat.txt` from WhatsApp export |

### Step 2 — Watch the graph grow
Every input extracts concept nodes and relationship edges automatically. Nodes get stronger (bigger on graph) each time a concept reappears across different sources.

### Step 3 — Ask your brain
Type any question in Hindi, English, or Hinglish. MemoryOS searches your personal graph and generates an answer citing which source each insight came from.

### Step 4 — Explore the visual graph
Switch to graph view to see your entire knowledge map — every concept you've ever learned, connected by relationships.

---

## 💡 Example Queries

```
"What do I know about progressive overload?"
"Connect my podcast notes with my gym notes"
"What topics have I studied most this month?"
"Discipline ke baare mein maine kya seekha?"
"What was that thing I read about attention mechanisms?"
```

---

## 🔭 Future Scope

- [ ] Chrome extension — auto-capture every article you read
- [ ] Mobile app — voice notes on the go
- [ ] Knowledge gap detector — "you know X and Y but have a blind spot in Z"
- [ ] Team knowledge graph — shared institutional memory for startups
- [ ] Notion / Obsidian / Gmail integration
- [ ] Offline mode with local LLM (Ollama)

---

## 🤔 How is this different from ChatGPT / Notion AI?

| Feature | MemoryOS | ChatGPT / Notion AI |
|---|---|---|
| Answers from YOUR notes | ✅ | ❌ |
| Remembers across sessions | ✅ | ❌ |
| Visual knowledge graph | ✅ | ❌ |
| Works in Hinglish | ✅ | Partially |
| Detects cross-domain patterns | ✅ | ❌ |
| 100% local / private | ✅ | ❌ |
| Grows smarter over time | ✅ | ❌ |

---

## 📄 License

MIT License - free to use, modify, and distribute.

---

## 🙋‍♂️ Author

Built by **Vipul Barmukh** — Final year engineering student passionate about AI/ML, NLP, and building products that solve real problems.

- GitHub: [@Vipul-104](https://github.com/Vipul-104)
- LinkedIn: [Vipul Barmukh](https://linkedin.com/in/vipul-barmukh-b44aa9311)

---

> *"The best second brain is one built from your own first brain."*
