# Research-Agent
AI-powered research assistant using Gemini to autonomously filter, score, and summarize Arxiv papers based on custom research goals.

An intelligent research assistant powered by Gemini. This agent automates the tedious process of literature review by fetching the latest papers from Arxiv and evaluating them against your specific research objectives.

## 🚀 Key Features
- **Autonomous Filtering:** Scores papers from 0-100 based on their relevance to your specific research goals.
- **Real-time Reasoning Logs:** Watch the agent's "thought process" as it evaluates each paper's abstract with detailed justifications.
- **Top-N Curation:** Automatically sorts and promotes the most relevant papers to a "Top Picks" dashboard at the top of the page.
- **Efficiency Optimized:** Uses a single-pass prompt architecture to handle scoring, reasoning, and summarization in one API call, saving your quota.
- **Streamlit UI:** A clean, interactive dashboard for seamless research exploration.

## 🛠 Tech Stack
- **LLM:** Google Gemini 2.5 Flash
- **Backend:** Python 3.9+
- **Frontend:** Streamlit
- **Data Source:** Arxiv API

## 📋 Prerequisites
- Python 3.9 or higher
- A Google Gemini API Key

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Research-Agent.git](https://github.com/YOUR_USERNAME/Research-Agent.git)
   cd Research-Agent
