import streamlit as st
from core.email_fetcher import fetch_emails, is_connected, get_user_email
from core.analyzer import analyze_email
import pandas as pd
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from config.settings import load_settings, save_settings
from datetime import datetime


st.set_page_config(
    page_title="AI Email Application Tracker",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    [data-testid="stSidebar"] ul {display: none;}
    </style>
    """, unsafe_allow_html=True)

def render_screen():

    load_css()

    if "gmail_connected" not in st.session_state:
        st.session_state.gmail_connected = False

    header_left, header_right = st.columns([5,1])

    with header_left:

        st.markdown("""
        <h1 class='main-title'>
            AI Job Email Analyzer
        </h1>

        <p class='subtitle'>
            Detect interviews, rejections and track your job search automatically.
        </p>
        """, unsafe_allow_html=True)


    with header_right:

        if is_connected():

            st.markdown("""
            <div class="connected">
                🟢 Connected
            </div>
            """, unsafe_allow_html=True)

        else:
            st.markdown("""
            <div class="disconnected">
                🔴 Not Connected
            </div>
            """, unsafe_allow_html=True)



    col1, col2 = st.columns([2, 5])

    with col1:
        analyze_email_btn = st.button(
            "✨ Analyze latest emails",
            use_container_width=True
        )
    
    if analyze_email_btn:  
        with st.spinner("Analyzing emails..."):
            
            try:
                emails = fetch_emails()
                st.session_state.gmail_connected = True

            except Exception:
                st.session_state.gmail_connected = False
                st.error("Unable to connect Gmail.")
                return

            st.session_state.data = []

            for e in emails:
                result = analyze_email(e["subject"] + "\n" + e["body"])
                # SHOW ONLY JOB RELATED
                if result.get("is_job_related") is True:
                    st.session_state.data.append(result)

            st.success("Analysis complete!")
        
            if "data" not in st.session_state:
                st.session_state.data = []

    st.write("")

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
    
    with st.sidebar:

        st.markdown("""
        <div class="sidebar-logo">
            📧 AI Job Email Analyzer
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

        if st.button("🇬 Connect Gmail", use_container_width=True):

            try:
                fetch_emails()
                st.session_state.gmail_connected = True
                st.rerun()

            except Exception as e:
                st.error(str(e))

        if st.button("⚙ Logout", use_container_width=True):
        

            # Delete OAuth token
            if os.path.exists("token.json"):
                os.remove("token.json")

            # Reset connection state
            st.session_state.gmail_connected = False

            # Clear analyzed data
            st.session_state["data"] = []

            # Clear all other session variables
            for key in list(st.session_state.keys()):
                if key not in ["gmail_connected"]:
                    del st.session_state[key]

            st.session_state.clear()

            st.rerun()

        if st.button("🗑 Delete data", use_container_width=True):
            st.session_state["data"] = []
            st.rerun()

        #SETTINGS

        settings = load_settings()

        enabled = st.checkbox(
            "Enable monthly report",
            value=settings["monthly_report"]
        )

        recipient_email = st.text_input(
            "Recipient email",
            value=settings["email"]
        )

        send_time = st.time_input(
            "Send time",
            value=datetime.strptime(
                settings["time"],
                "%H:%M"
            ).time()
        )

        if st.button("Save settings"):

            save_settings({
                "monthly_report": enabled,
                "email": recipient_email,
                "time": send_time.strftime("%H:%M")
            })

            st.success("Settings saved")

        st.markdown("<div class='sidebar-spacer'></div>", unsafe_allow_html=True)

        if is_connected():
            email = get_user_email()

            if email:
                st.divider()

                with st.container(border=True):
                    st.markdown("### 👤 Connected account")
                    st.write(email)

    left,right = st.columns([5,1.2])
    controls = st.columns([2,2,1])


    left, right = st.columns([4, 1])
            
    with left:
        search = st.text_input(
            "",
            placeholder="🔍 Search company..."
        )

    st.markdown("##### Categories")

    category_filter = st.radio(
        "",
        [
            "All",
            "Interview",
            "Offer",
            "Assessment",
            "Rejection",
            "Networking",
        ],
        horizontal=True,
        label_visibility="collapsed",
    )

 
    with controls[2]:
        st.write("")

    #create_table(search, category_filter)

    if st.session_state.get("data"):

        df = pd.DataFrame(st.session_state.data)

        # Filters
        if search:
            df = df[df["company"].str.contains(search, case=False, na=False)]

        if category_filter != "All":
            df = df[df["category"].str.contains(category_filter.lower(), na=False)]

        render_metrics()

        st.markdown("<br>", unsafe_allow_html=True)

        left, right = st.columns([6, 1])

        with right:
            pdf_file = create_pdf(df)

            with open(pdf_file, "rb") as f:
                st.download_button(
                    "📄 Export as PDF",
                    data=f,
                    file_name="job_emails.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                )

        create_table(df)

def metric_card(title,value,color):

    st.markdown(f"""
    <div class="metric">

    <div class="metric-value">

    {value}

    </div>

    <div class="metric-title">

    {title}

    </div>

    </div>

    """,unsafe_allow_html=True)

def render_metrics():

    data = st.session_state.get("data", [])

    total = len(data)

    interviews = sum(
        1 for x in data
        if "interview" in x["category"]
    )

    offers = sum(
        1 for x in data
        if x["category"] == "offer"
    )

    rejections = sum(
        1 for x in data
        if x["category"] == "rejection"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric">
            <div class="metric-value">{total}</div>
            <div class="metric-title">Total Emails</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric">
            <div class="metric-value">{interviews}</div>
            <div class="metric-title">Interviews</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric">
            <div class="metric-value">{offers}</div>
            <div class="metric-title">Offers</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric">
            <div class="metric-value">{rejections}</div>
            <div class="metric-title">Rejections</div>
        </div>
        """, unsafe_allow_html=True)

def create_table(df):

    if df.empty:
        st.info("No job related emails found.")
        return

    df = df.rename(columns={
        "is_job_related": "Job Related",
        "category": "Category",
        "company": "Company",
        "date": "Date",
        "summary": "Summary",
        "language": "Language",
    })
    

    df = df.drop(columns=["Job Related"])
    df = df.sort_values(by="Date", ascending=False)

    for _, row in df.iterrows():
        render_email_card(row)

def render_email_card(row):

    category = row["Category"]

    colors = {
        "interview_invitation": ("🟢 Interview", "#22c55e"),
        "interview_followup": ("🟢 Follow-up", "#22c55e"),
        "offer": ("🟣 Offer", "#8b5cf6"),
        "assessment": ("🟠 Assessment", "#f59e0b"),
        "rejection": ("🔴 Rejection", "#ef4444"),
        "application_received": ("🔵 Applied", "#3b82f6"),
        "networking": ("🟡 Networking", "#eab308"),
        "other_job_related": ("⚪ Other", "#64748b"),
    }

    badge, color = colors.get(
        category,
        ("⚪ Other", "#64748b")
    )

    st.markdown(
        f"""
        <div class="email-card">
        <div class="left-bar" style="background:{color};"></div>
        <div class="content">
        <div class="top">
        <div>

        <h3>{row["Company"]}</h3>

        <span class="badge" style="background:{color};">
        {badge}
        </span>

        </div>
        <div class="date">
        📅 {row["Date"]}
        </div>

        </div>

        <p class="summary">

        {row["Summary"]}

        </p>

        <div class="bottom">
    

        <span class="language">

        🌍 {row["Language"].upper()}

        </span>

        </div>

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )

def create_pdf(df):
    file_path = "job_emails.pdf"
    doc = SimpleDocTemplate(file_path)

    styles = getSampleStyleSheet()
    elements = []

    for _, row in df.iterrows():
        elements.append(Paragraph(f"<b>Company:</b> {row['company']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Category:</b> {row['category']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Date:</b> {row['date']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Summary:</b> {row['summary']}", styles["Normal"]))
        elements.append(Paragraph(f"<b>Language:</b> {row['language']}", styles["Normal"]))
        elements.append(Spacer(1, 15))

    doc.build(elements)

    return file_path


if __name__ == "__main__":
    render_screen()
