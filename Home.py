import streamlit as st
from sidebar import render_sidebar

st.set_page_config(
    page_title="Option Pricing Dashboard",
    layout="wide"
)

st.title("Option Pricing Dashboard")

# 🔹 Organisation en colonnes
col1, col2 = st.columns(2)

with col1:
    st.markdown("- **European Options** (BS, MC, CRR)")
    st.markdown("- **American Options** (CRR only)")
    st.markdown("- **Asian Options** (MC avg. arithmetic/geometric)")
    st.markdown("- **Digital Options** (MC binary payout)")

with col2:
    st.markdown("- **Greeks Visualizer**")
    st.markdown("- **Theoretical Recap**: Definitions, assumptions")

st.markdown("---")

# 🔹 Navigation par boutons
nav_cols = st.columns(3)

with nav_cols[0]:
    if st.button("European Options"):
        st.switch_page("pages/1_European_Options.py")
    if st.button("American Options"):
        st.switch_page("pages/2_American_Options.py")

with nav_cols[1]:
    if st.button("Asian Options"):
        st.switch_page("pages/3_Asian_Options.py")
    if st.button("Digital Options"):
        st.switch_page("pages/4_Digital_Options.py")

with nav_cols[2]:
    if st.button("Greeks Visualizer"):
        st.switch_page("pages/5_Greeks_Visualizer.py")
    if st.button("Theoretical Recap"):
        st.switch_page("pages/6_Technical_Recap.py")


st.markdown("---")

render_sidebar()