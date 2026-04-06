import streamlit as st
import pandas as pd
from io import BytesIO

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ── PAGE CONFIG ─────────────────────────────────────
st.set_page_config(page_title="CEMS Dashboard", layout="wide")

# ── SAMPLE DATA (NO CSV NEEDED) ─────────────────────
events_df = pd.DataFrame([
    {"id":1,"title":"HackFest","category":"Tech","date":"Apr 12","venue":"Lab","capacity":100,"registered":60},
    {"id":2,"title":"Cultural Night","category":"Cultural","date":"Apr 18","venue":"Hall","capacity":200,"registered":150},
])

certificates_df = pd.DataFrame([
    {"event_title":"HackFest","prize":"1st Place","date":"Apr 12","issued_date":"Apr 13"},
])

# ── SESSION STATE ───────────────────────────────────
if "registered" not in st.session_state:
    st.session_state.registered = []

if "name" not in st.session_state:
    st.session_state.name = ""

if "page" not in st.session_state:
    st.session_state.page = "Login"

# ── PDF FUNCTION ────────────────────────────────────
def generate_pdf(name, event, prize, date, issued):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("<b>CERTIFICATE OF ACHIEVEMENT</b>", styles['Title']))
    content.append(Spacer(1, 20))
    content.append(Paragraph(f"This is to certify that <b>{name}</b>", styles['Normal']))
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"has won <b>{prize}</b>", styles['Normal']))
    content.append(Spacer(1, 10))
    content.append(Paragraph(f"in <b>{event}</b>", styles['Normal']))
    content.append(Spacer(1, 20))
    content.append(Paragraph(f"Date: {date}", styles['Normal']))
    content.append(Paragraph(f"Issued: {issued}", styles['Normal']))

    doc.build(content)
    buffer.seek(0)
    return buffer

# ── LOGIN ───────────────────────────────────────────
def login():
    st.title("🎓 CEMS Login")

    name = st.text_input("Enter Name")

    if st.button("Login"):
        if name:
            st.session_state.name = name
            st.session_state.page = "Dashboard"
            st.rerun()
        else:
            st.error("Enter name")

# ── SIDEBAR ─────────────────────────────────────────
def sidebar():
    st.sidebar.title("CEMS")

    if st.sidebar.button("Dashboard"):
        st.session_state.page = "Dashboard"

    if st.sidebar.button("Events"):
        st.session_state.page = "Events"

    if st.sidebar.button("Certificates"):
        st.session_state.page = "Certificates"

    if st.sidebar.button("Logout"):
        st.session_state.page = "Login"

# ── DASHBOARD ───────────────────────────────────────
def dashboard():
    st.title(f"Welcome {st.session_state.name} 👋")

    col1, col2 = st.columns(2)

    col1.metric("Registered Events", len(st.session_state.registered))
    col2.metric("Certificates", len(certificates_df))

# ── EVENTS PAGE ─────────────────────────────────────
def events():
    st.title("🎉 Events")

    for _, row in events_df.iterrows():
        st.subheader(row["title"])
        st.write(f"{row['category']} | {row['date']} | {row['venue']}")

        if row["id"] in st.session_state.registered:
            st.success("Registered")
        else:
            if st.button(f"Register {row['id']}"):
                st.session_state.registered.append(row["id"])
                st.success("Registered!")

# ── CERTIFICATES PAGE ───────────────────────────────
def certificates():
    st.title("🏅 Certificates")

    for i, row in certificates_df.iterrows():
        st.subheader(row["event_title"])
        st.write(f"{row['prize']} | {row['date']}")

        pdf = generate_pdf(
            st.session_state.name,
            row['event_title'],
            row['prize'],
            row['date'],
            row['issued_date']
        )

        st.download_button(
            "Download PDF",
            data=pdf,
            file_name=f"{row['event_title']}.pdf",
            mime="application/pdf"
        )

# ── MAIN ROUTER ─────────────────────────────────────
if st.session_state.page == "Login":
    login()
else:
    sidebar()

    if st.session_state.page == "Dashboard":
        dashboard()
    elif st.session_state.page == "Events":
        events()
    elif st.session_state.page == "Certificates":
        certificates()
