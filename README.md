# 🌊 Blue Ocean

An autonomous pipeline that discovers underexploited, high-intent search queries and ranks them by estimated profit opportunity — built as a scoped, deployable MVP.

---

## 🚀 Status & Roadmap

| Step | Task | Status | Details |
| :--- | :--- | :---: | :--- |
| **1** | Scaffold & Deployment | ✅ Done | Streamlit app deployed on GitHub / Streamlit Community Cloud |
| **2** | Query Expansion | ✅ Done | 5-stage autonomous expansion (Autocomplete + PAA) yielding 50–150+ queries |
| **3** | SERP Ad Density Scraper | ⏳ Pending | Live commercial intent filter (paid ad slot counter) |
| **4** | Google Trends Demand Signal | ⏳ Pending | Relative search volume via `pytrends` (0–100) |
| **5** | Opportunity Scoring & Ranking | ⏳ Pending | Transparent heuristic ranking formula |
| **6** | UI Polish & Error Handling | ⏳ Pending | Robust rate-limiting, partial failure handling |
| **7** | Production Documentation | ⏳ Pending | Full deployment & architecture retrospective |

---

## 🔍 Step 2: Query Expansion Architecture

The query expansion engine ([expansion.py](expansion.py)) harvests candidate keywords across 5 distinct channels:

1. **Direct Google Autocomplete:** Base query suggestions directly from Google's completion API.
2. **People Also Ask (PAA) & Question-Intent:** Questions answering buying intent (`"how to choose"`, `"is it worth buying"`, `"what is the best"`).
3. **High-Intent Commercial Modifiers:** Buyer keyword patterns (`"best"`, `"budget"`, `"top rated"`, `"compact"`, `"commercial vs home"`).
4. **Contextual Prepositions:** Long-tail combinations (`"for"`, `"with"`, `"under"`, `"vs"`, `"without"`).
5. **Alphabet Permutations:** Recursive suffix probing (`"seed a"`, `"seed b"`, ...) until target count is reached.

---

## 💻 Running Locally

1. Clone repository:
   ```bash
   git clone https://github.com/bryanmsh/blue-ocean.git
   cd blue-ocean
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the Streamlit dashboard:
   ```bash
   streamlit run app.py
   ```
