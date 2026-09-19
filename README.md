# 🌊 Blue Ocean

An autonomous pipeline that discovers underexploited, high-intent search queries and ranks them by estimated profit opportunity — built as a scoped, deployable MVP.

---

## 🚀 Status & Roadmap

| Stage | Focus Area | Status | Details |
| :--- | :--- | :---: | :--- |
| **Infrastructure** | Scaffold & Deployment | ✅ Live | Streamlit app deployed on GitHub / Streamlit Community Cloud |
| **Expansion** | Query Expansion | ✅ Live | 5-stage autonomous expansion (Autocomplete + PAA) yielding 50–150+ queries |
| **Commercial Filter** | SERP Ad Density Scraper | ✅ Live | Dual-layer ad slot counter & commercial intent gatekeeper (0–4 ads) |
| **Demand Signal** | Google Trends Signal | ⏳ Pending | Relative search volume via `pytrends` (0–100) |
| **Scoring** | Opportunity Ranking Formula | ⏳ Pending | Heuristic score calculation |
| **Polish** | UI Polish & Error Handling | ⏳ Pending | Robust rate-limiting & partial failure handling |
| **Documentation** | Production Documentation | ⏳ Pending | Architecture retrospective |

---

## 🔍 Core Architecture

### 1. Query Expansion Engine (`expansion.py`)
Harvests long-tail keywords across 5 channels:
* Direct Google Autocomplete
* People Also Ask (PAA) question-intent patterns (`"how to choose"`, `"is it worth"`, `"what is the best"`)
* High-intent commercial modifiers (`"best"`, `"budget"`, `"top rated"`, `"compact"`)
* Contextual prepositions (`"for"`, `"with"`, `"under"`, `"vs"`)
* Recursive alphabetical suffix probing

### 2. Commercial Intent & SERP Ad Scraper (`serp_ad_scraper.py`)
Acts as the commercial gatekeeper:
* **Intent Gatekeeper:** Queries with **0 paid ad slots** are identified as purely informational/educational and disqualified from the opportunity pool.
* **Blue Ocean Detection:** Queries with **1–2 ad slots** are prioritized as uncontested commercial opportunities.
* **Dual-Layer Architecture:** Combines live SERP ad container scraping (`data-text-ad`, `class="uEierd"`, `aria-label="Sponsored"`) with a semantic auction proxy classifier to gracefully handle search engine bot-blocking and rate limits without failing.

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
