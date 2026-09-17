import streamlit as st
import pandas as pd
import time

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

# Sidebar - Pipeline Status & Info
with st.sidebar:
    st.header("Pipeline Configuration")
    st.info("**Current Phase:** Step 1 (Scaffold & Mock Output)")
    st.markdown(
        """
        **Pipeline Steps:**
        1. ✅ Scaffold & Cloud Deployment
        2. ⏳ Query Expansion (Autocomplete & PAA)
        3. ⏳ Commercial Intent Filter (SERP Ad Slots)
        4. ⏳ Demand Signal (Google Trends)
        5. ⏳ Opportunity Scoring & Ranking
        """
    )
    st.markdown("---")
    st.markdown(
        "[GitHub Repository](https://github.com/bryanmsh/blue-ocean)"
    )

# Step 1: Input Box
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

# Mock Data Generator (Hardcoded fake output per Step 1 PRD)
def get_mock_results(query: str) -> pd.DataFrame:
    data = [
        {
            "Rank": 1,
            "Keyword": f"best compact {query} for small apartments",
            "Google Trends Interest": 78,
            "Ad Slots": 1,
            "Commercial Intent": "High (1 Ad)",
            "Opportunity Score": 89.2,
        },
        {
            "Rank": 2,
            "Keyword": f"quietest {query} grinder combo",
            "Google Trends Interest": 65,
            "Ad Slots": 1,
            "Commercial Intent": "High (1 Ad)",
            "Opportunity Score": 82.5,
        },
        {
            "Rank": 3,
            "Keyword": f"{query} cleaning tablet alternatives",
            "Google Trends Interest": 52,
            "Ad Slots": 2,
            "Commercial Intent": "Medium (2 Ads)",
            "Opportunity Score": 71.0,
        },
        {
            "Rank": 4,
            "Keyword": f"budget dual boiler {query} under $1000",
            "Google Trends Interest": 84,
            "Ad Slots": 4,
            "Commercial Intent": "Saturated (4 Ads)",
            "Opportunity Score": 55.4,
        },
        {
            "Rank": 5,
            "Keyword": f"how to descale {query} vinegar",
            "Google Trends Interest": 91,
            "Ad Slots": 0,
            "Commercial Intent": "Filtered Out (0 Ads)",
            "Opportunity Score": 0.0,
        },
    ]
    return pd.DataFrame(data)

# Results Display
st.markdown("### Opportunity Discovery Results")

if run_pipeline or niche_query:
    if run_pipeline:
        with st.spinner("Simulating pipeline (Scaffolding Phase)..."):
            time.sleep(0.6)

    # Metrics Summary
    metric1, metric2, metric3, metric4 = st.columns(4)
    with metric1:
        st.metric(label="Candidates Evaluated", value="74")
    with metric2:
        st.metric(label="Commercial Intent Survived", value="18")
    with metric3:
        st.metric(label="Zero-Ad Filtered", value="56")
    with metric4:
        st.metric(label="Top Opportunity Score", value="89.2 / 100")

    df = get_mock_results(niche_query.strip() or "home espresso machines")

    # Filter out 0 ad slots for surviving ranked view
    surviving_df = df[df["Opportunity Score"] > 0].reset_index(drop=True)

    st.subheader(f"Ranked Long-Tail Opportunities for: *{niche_query}*")
    st.dataframe(
        surviving_df,
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
                "Paid Ad Density",
                help="Number of search ads present on SERP",
            ),
        },
    )

    with st.expander("Filtered Out Candidates (Non-Commercial)", expanded=False):
        filtered_df = df[df["Opportunity Score"] == 0].reset_index(drop=True)
        st.write("These queries have search volume but 0 paid ad slots, indicating lack of commercial buying intent:")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

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
