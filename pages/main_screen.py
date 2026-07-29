import streamlit as st
import json
from core.email_fetcher import fetch_emails
from core.analyzer import analyze_email


st.title("Job Email Analyzer")

if "data" not in st.session_state:
    st.session_state.data = []

if st.button("Check emails"):
    emails = fetch_emails()
    st.session_state.data = []

    for e in emails:
        result = analyze_email(e["body"])
        parsed = json.loads(result)
        st.session_state.data.append(parsed)

if st.session_state.data:
    st.dataframe(st.session_state.data)

