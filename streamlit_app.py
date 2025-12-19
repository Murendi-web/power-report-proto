import streamlit as st
import os

st.set_page_config(page_title="AI Stock Dashboard")

st.title("AI Stock Reporting – Murendi")

reports = sorted(os.listdir("outputs/reports"), reverse=True)
for r in reports:
    st.markdown(f"- {r}")
