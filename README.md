# 🤖 Resume Matcher with LLM-Powered Semantic Search

This project implements a resume matching engine using **LLMs and vector similarity search**, enabling recruiters or job platforms to semantically match resumes with job descriptions. It uses `spaCy` for text parsing, `qdrant` for vector storage, and supports natural language queries.

---

## 🔍 Features

- ✅ Extracts key sections from resumes using NLP
- ✅ Embeds both job descriptions and resumes
- ✅ Stores vectors in **Qdrant** for fast similarity search
- ✅ Supports semantic queries like:
  > "Find resumes with fraud detection and time-series modeling"

---

## 🧠 Tech Stack

- Python 3.10+
- `spaCy` (NLP pipeline)
- `qdrant-client` (vector DB)
- `scikit-learn`, `pandas`, `tqdm`
- Optional: `streamlit` or `Flask` (for UI/API)

---

## 📂 File Overview

| File | Description |
|------|-------------|
| `resume_parser.py` | Extracts structured info from resumes |
| `qdrant_store.py` | Stores and retrieves embeddings from Qdrant |
| `utils.py` | Preprocessing and helper functions |
| `main.ipynb` | Development notebook for testing embedding + matching |

---

## 🚀 How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
