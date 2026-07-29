import streamlit as st
import json
from core.email_fetcher import fetch_emails
from core.analyzer import analyze_email
import pandas as pd


#TITLE
st.markdown("""
    <h1 style='text-align: center;'>AI Job Email Analyzer</h1>
    <p style='text-align: center; color: gray;'>
    Detect interviews, rejections, and track your job search automatically
    </p>
    """, unsafe_allow_html=True)    

def render_screen():
    if "data" not in st.session_state:
        st.session_state.data = []

    st.markdown("""
    <style>
    .big-button button {
        width: 100%;
        height: 70px;
        font-size: 22px;
        font-weight: bold;
        border-radius: 12px;
        background: linear-gradient(90deg, #4CAF50, #2E7D32);
        color: white;
        border: none;
        transition: 0.3s;
    }

    .big-button button:hover {
        background: linear-gradient(90deg, #66BB6A, #388E3C);
        transform: scale(1.03);
    }
    </style>
    """, unsafe_allow_html=True)

    #CREDENTIALS INPUT IN SIDEBAR
    with st.sidebar:
        st.header("Credentials")

        email_input = st.text_input("Email")
        password_input = st.text_input("App Password", type="password")

        if st.button("Save credentials"):
            st.session_state.email = email_input
            st.session_state.password = password_input
            st.success("Saved")

        #DELETE CREDENTIALS 
        if st.button("Delete all data"):
            st.session_state.clear()
            st.warning("All data removed")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown('<div class="big-button">', unsafe_allow_html=True)
        check = st.button("Analyze Emails")
        st.markdown('</div>', unsafe_allow_html=True)

    if check:
        with st.spinner("Analyzing emails..."):
            if "email" not in st.session_state:
                st.error("Please enter credentials first")
                return

            emails = fetch_emails(
                st.session_state.email,
                st.session_state.password
            )

            st.session_state.data = []

            for e in emails:
                result = analyze_email(e["body"])
                parsed = json.loads(result)
                st.session_state.data.append(parsed)

            st.success("Analysis complete!")

    if st.session_state.data:
        create_table()

def create_table():
    #st.dataframe(st.session_state.data)
    df = pd.DataFrame(st.session_state.data)

    df = df.rename(columns={
        "is_job_related": "Job Related",
        "category": "Category",
        "company": "Company",
        "date": "Date",
        "summary": "Summary"
    })

    st.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    render_screen()
