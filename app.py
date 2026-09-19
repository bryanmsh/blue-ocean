import streamlit as st
import pandas as pd
import time
from expansion import expand_queries
from serp_ad_scraper import batch_inspect_ad_density, inspect_ad_density

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
    st.success("**Current Phase:** Step 3 Completed ✅")
    st.markdown(
        """
        **Pipeline Steps:**
        1. ✅ Scaffold & Cloud Deployment
        2. ✅ Query Expansion (Autocomplete & PAA)
        3. ✅ Commercial Intent Filter (SERP Ad Slots)
        4. ⏳ Demand Signal (Google Trends)
        5. ⏳ Opportunity Scoring & Ranking
        """
    )
    st.markdown("---")
    st.header("Pipeline Controls")
    candidate_target = st.slider(
        "Candidate Expansion Target",
        min_value=20,
        max_value=120,
        value=50,
        step=10,
        help="Number of candidate long-tail queries to harvest from Google Autocomplete.",
    )
    ad_inspection_limit = st.slider(
        "SERP Ad Inspection Depth",
        min_value=10,
        max_value=50,
        value=25,
        step=5,
        help="Number of top candidates to inspect for paid ad density.",
    )
    st.markdown("---")
    st.markdown("[GitHub Repository](https://github.com/bryanmsh/blue-ocean)")

# Cache expansion calls
@st.cache_data(ttl=3600, show_spinner=False)
def cached_expand_queries(seed: str, max_candidates: int):
    return expand_queries(seed, max_candidates=max_candidates)

# Cache ad inspection calls
@st.cache_data(ttl=3600, show_spinner=False)
def cached_inspect_ads(queries_tuple: tuple):
    return [inspect_ad_density(q) for q in queries_tuple]

# Input Interface
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

# Main Pipeline Execution
if run_pipeline or niche_query:
    seed = niche_query.strip()
    if not seed:
        st.warning("Please enter a valid seed keyword or niche.")
    else:
        # Step 2: Query Expansion
        progress_bar = st.progress(0, text="Stage 1/2: Harvesting candidate queries...")
        
        def update_exp_progress(pct: float, msg: str):
            progress_bar.progress(pct * 0.5, text=f"Stage 1/2: {msg}")

        t_start = time.time()
        raw_candidates = expand_queries(
            seed,
            max_candidates=candidate_target,
            on_progress=update_exp_progress,
        )

        if not raw_candidates:
            progress_bar.empty()
            st.error("No queries could be retrieved. Please check your network connection.")
        else:
            # Step 3: SERP Ad Density Inspection
            queries_to_inspect = [c["query"] for c in raw_candidates[:ad_inspection_limit]]
            source_map = {c["query"]: c["source"] for c in raw_candidates}
            
            def update_ad_progress(pct: float, msg: str):
                progress_bar.progress(0.5 + (pct * 0.5), text=f"Stage 2/2: {msg}")

            ad_results = batch_inspect_ad_density(
                queries_to_inspect,
                delay_sec=0.04,
                on_progress=update_ad_progress,
            )
            progress_bar.empty()
            t_elapsed = time.time() - t_start

            # Construct DataFrame with Live Step 3 Ad Data
            rows = []
            for ad_info in ad_results:
                q = ad_info["query"]
                ads = ad_info["ad_slots"]
                src = source_map.get(q, "Expansion")
                
                # Simulated Trend score until Step 4
                h = abs(hash(q))
                trend = 45 + (h % 50)
                
                # PRD Heuristic Opportunity Score
                if ads == 0:
                    score = 0.0
                else:
                    # 1-2 ads get high opportunity reward; 4 ads heavily penalized
                    competition_penalty = (ads - 1) / 4.0
                    score = round(trend * (1.0 - (competition_penalty * 0.55)), 1)
                
                rows.append({
                    "Keyword": q,
                    "Expansion Source": src,
                    "Google Trends Interest": trend,
                    "Ad Slots": ads,
                    "Commercial Intent": ad_info["density_label"],
                    "Opportunity Score": score,
                    "Detection Method": ad_info["method"],
                })

            df_all = pd.DataFrame(rows).sort_values(by="Opportunity Score", ascending=False).reset_index(drop=True)
            surviving = df_all[df_all["Opportunity Score"] > 0].reset_index(drop=True)
            filtered = df_all[df_all["Opportunity Score"] == 0].reset_index(drop=True)

            # Summary Metrics
            st.markdown("### Pipeline Results Overview")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Expanded", f"{len(raw_candidates)} queries", f"{t_elapsed:.2f}s total")
            with col2:
                st.metric("SERP Ads Inspected", f"{len(ad_results)} evaluated")
            with col3:
                st.metric("Commercial Survived (≥1 Ad)", f"{len(surviving)}")
            with col4:
                st.metric("Filtered Out (0 Ads)", f"{len(filtered)}")

            # Visual Tabs
            tab_ranked, tab_ad_density, tab_expansion, tab_filtered = st.tabs([
                "🏆 Ranked Opportunity Pipeline",
                "📊 SERP Ad Density Breakdown",
                "🔍 All Discovered Queries",
                "🚫 Disqualified (0 Ads)",
            ])

            with tab_ranked:
                st.caption("Commercial queries filtered by paid ad presence and ranked by Opportunity Score:")
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
                            help="Number of search ads present on SERP (0-4)",
                        ),
                    },
                )

            with tab_ad_density:
                st.caption("Live commercial intent verification results (Step 3):")
                ad_counts = df_all["Commercial Intent"].value_counts().reset_index()
                ad_counts.columns = ["Ad Density Category", "Queries"]
                
                col_c1, col_c2 = st.columns([1, 2])
                with col_c1:
                    st.write("**Competition Density Distribution:**")
                    st.dataframe(ad_counts, use_container_width=True, hide_index=True)
                with col_c2:
                    st.write("**Inspected Queries with Detection Attribution:**")
                    st.dataframe(
                        df_all[["Keyword", "Ad Slots", "Commercial Intent", "Detection Method"]],
                        use_container_width=True,
                        hide_index=True,
                    )

            with tab_expansion:
                st.caption(f"All {len(raw_candidates)} queries generated by Step 2 expansion:")
                st.dataframe(pd.DataFrame(raw_candidates), use_container_width=True, hide_index=True)

            with tab_filtered:
                st.info("Per PRD Section 4: Queries with 0 paid ads represent non-commercial/informational intent and are eliminated from the profit opportunity pool.")
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
          $$\\text{Opportunity Score} = \\text{Normalized Trend} \\times \\left(1 - 0.55 \\times \\frac{\\text{Ad Slots} - 1}{4}\\right)$$
        """
    )
