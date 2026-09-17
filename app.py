import streamlit as st

st.set_page_config(
    page_title="Blue Ocean",
    page_icon="🌊",
    layout="wide",
)

st.title("🌊 Blue Ocean")
st.subheader("Step 1 — Hello World Streamlit App")

st.success("App successfully deployed and operational!")

with st.expander("System & Environment Info", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Status", value="Healthy")
    with col2:
        st.metric(label="Stage", value="Step 1: Scaffolding")
    with col3:
        st.metric(label="Scraping Engine", value="Pending PRD Review")

st.markdown("---")
st.info("Ready for scraping logic and PRD feature implementation.")
