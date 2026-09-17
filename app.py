import streamlit as st
import pandas as pd
import time
from expansion import expand_queries

st.set_page_config(
    page_title="Blue Ocean — Keyword Opportunity Pipeline",
    page_icon="🌊",
    layout="wide",
)

st.title("🌊 Blue Ocean")
st.caption(
    "Autonomous discovery of underexploited, high-intent search queries ranked by profit opportunity."
)

st.markdown("---")

# Sidebar - Pipeline Status & Configuration
with st.sidebar:
    st.header("Pipeline Status")
    st.success("**Current Phase:** Step 2 Completed ✅")
    st.markdown(
        """
        **Pipeline Steps:**
        1. ✅ Scaffold & Cloud Deployment
        2. ✅ Query Expansion (Autocomplete & PAA)
        3. ⏳ Commercial Intent Filter (SERP Ad Slots)
        4. ⏳ Demand Signal (Google Trends)
        5. ⏳ Opportunity Scoring & Ranking
        """
    )
    st.markdown("---")
    st.header("Expansion Controls")
    candidate_target = st.slider(
        "Candidate Target Count",
        min_value=30,
        max_value=150,
        value=75,
        step=15,
        help="Target number of candidate long-tail queries to discover.",
    )
    st.markdown("---")
    st.markdown("[GitHub Repository](https://github.com/bryanmsh/blue-ocean)")

# Cache expansion calls to prevent redundant network requests and respect Google rate limits
@st.cache_data(ttl=3600, show_spinner=False)
def cached_expand_queries(seed: str, max_candidates: int):
    return expand_queries(seed, max_candidates=max_candidates)

# Step 1 & 2: Input Box
col_input, col_btn = st.columns([4, 1])
with col_input:
    niche_query = st.text_input(
        "Enter a topic or seed niche:",
        value="home espresso machines",
        placeholder="e.g. ergonomic office chairs, portable power stations...",
        help="Broad topic used to generate long-tail keyword candidates.",
    )
with col_btn:
    st.write("")  # alignment spacer
    st.write("")
    run_pipeline = st.button("Find Opportunities", type="primary", use_container_width=True)

# Generate scoring heuristic for discovered candidates (Placeholder until Steps 3 & 4 are built)
def synthesize_mock_signals(candidates_list: list) -> pd.DataFrame:
    rows = []
    for i, item in enumerate(candidates_list):
        q = item["query"]
        src = item["source"]
        
        # Deterministic pseudo-metrics based on query length and hash for stable demo
        h = abs(hash(q))
        ads = (h % 5)  # 0 to 4 ads
        trend = 40 + (h % 55)  # 40 to 95
        
        # PRD Opportunity formula: if ads == 0 -> score = 0, else Trend * (1 - (ads-1)/4)
        if ads == 0:
            score = 0.0
            intent_label = "Filtered Out (0 Ads)"
        else:
            competition_penalty = (ads - 1) / 4.0
            score = round(trend * (1.0 - competition_penalty * 0.5), 1)
            intent_label = f"Commercial ({ads} Ad{'s' if ads > 1 else ''})"
            
        rows.append({
            "Keyword": q,
            "Expansion Source": src,
            "Google Trends Interest": trend,
            "Ad Slots": ads,
            "Commercial Intent": intent_label,
            "Opportunity Score": score,
        })
    
    df = pd.DataFrame(rows)
    return df.sort_values(by="Opportunity Score", ascending=False).reset_index(drop=True)

# Main Processing & Display
if run_pipeline or niche_query:
    seed = niche_query.strip()
    if not seed:
        st.warning("Please enter a valid seed keyword or niche.")
    else:
        progress_bar = st.progress(0, text="Initializing query expansion...")
        
        def update_progress(pct: float, msg: str):
            progress_bar.progress(pct, text=msg)

        t_start = time.time()
        # Step 2: Live Expansion
        candidates = expand_queries(
            seed,
            max_candidates=candidate_target,
            on_progress=update_progress,
        )
        t_elapsed = time.time() - t_start
        progress_bar.empty()

        if not candidates:
            st.error("No queries could be retrieved. Please check your network connection.")
        else:
            # Metrics Summary
            total_found = len(candidates)
            df_all = synthesize_mock_signals(candidates)
            surviving = df_all[df_all["Opportunity Score"] > 0]
            filtered = df_all[df_all["Opportunity Score"] == 0]

            st.markdown("### Step 2: Discovered Long-Tail Candidates")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Candidates Discovered", f"{total_found}", f"{t_elapsed:.2f}s latency")
            with col2:
                sources_count = len(set(c["source"].split(" (")[0] for c in candidates))
                st.metric("Expansion Channels", f"{sources_count} Strategies")
            with col3:
                st.metric("Commercial Survived (Simulated)", f"{len(surviving)}")
            with col4:
                top_score = surviving["Opportunity Score"].max() if not surviving.empty else 0.0
                st.metric("Top Opportunity Score", f"{top_score} / 100")

            # Tabs for viewing Step 2 Expansion breakdown vs Ranked Pipeline
            tab_ranked, tab_expansion, tab_filtered = st.tabs([
                "🏆 Ranked Opportunity Pipeline",
                "🔍 Live Discovered Queries (Step 2)",
                "🚫 Filtered (Zero-Ad Gatekeeper)",
            ])

            with tab_ranked:
                st.caption("Live discovered queries ranked with simulated signals (awaiting Step 3 & Step 4 scrapers):")
                st.dataframe(
                    surviving,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Opportunity Score": st.column_config.ProgressColumn(
                            "Opportunity Score",
                            help="Heuristic score balancing search demand vs ad competition",
                            format="%.1f",
                            min_value=0,
                            max_value=100,
                        ),
                        "Google Trends Interest": st.column_config.NumberColumn(
                            "Trend Interest (0-100)",
                            format="%d",
                        ),
                        "Ad Slots": st.column_config.NumberColumn(
                            "Paid Ad Slots",
                            help="Number of search ads present on SERP",
                        ),
                    },
                )

            with tab_expansion:
                st.caption("Every raw query harvested in real-time from Google Autocomplete & PAA channels:")
                expansion_df = pd.DataFrame(candidates)
                source_counts = expansion_df["source"].value_counts().reset_index()
                source_counts.columns = ["Strategy", "Queries Generated"]
                
                col_chart, col_list = st.columns([1, 2])
                with col_chart:
                    st.write("**Queries by Expansion Strategy:**")
                    st.dataframe(source_counts, use_container_width=True, hide_index=True)
                with col_list:
                    search_term = st.text_input("Filter discovered queries:", placeholder="Type to filter...")
                    filtered_candidates = expansion_df
                    if search_term:
                        filtered_candidates = filtered_candidates[
                            filtered_candidates["query"].str.contains(search_term.lower(), na=False)
                        ]
                    st.dataframe(filtered_candidates, use_container_width=True, hide_index=True)

            with tab_filtered:
                st.write("Candidates with zero commercial ad slots (filtered out per PRD Section 4):")
                st.dataframe(filtered, use_container_width=True, hide_index=True)

# Methodology Expander
with st.expander("📐 Opportunity Score Methodology (PRD Section 4 & 6)"):
    st.markdown(
        """
        The **Blue Ocean Opportunity Score** is a transparent heuristic:
        - **Demand Signal ($D$):** Google Trends relative search interest ($0 - 100$).
        - **Competition Proxy ($C$):** Number of paid ads on SERP ($1 - 4$). Lower ad count with at least 1 ad represents underexploited commercial intent.
        - **Intent Gatekeeper:** Queries with $0$ ads are filtered out ($Score = 0$).
        - **Heuristic Formula:** 
          $$\\text{Opportunity Score} = \\text{Normalized Trend} \\times \\left(1 - \\frac{\\text{Ad Slots} - 1}{4}\\right)$$
        """
    )
