# ============================================================
#  CEMS — College Event Management System
#  Student Dashboard — Streamlit App
#  File: app.py
#  Run: streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
from datetime import datetime
import io

# PDF generation
try:
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import mm, cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

# ── PAGE CONFIG ──────────────────────────────────────────────
st.set_page_config(
    page_title="CEMS — Student Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ───────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background-color: #0a0e1a; color: #e2e8f0; }
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1e2d45;
}
.stat-card {
    background: #131c2e;
    border: 1px solid #1e2d45;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    margin-bottom: 10px;
}
.stat-number { font-size: 2.2rem; font-weight: 800; color: #e2e8f0; line-height: 1; }
.stat-label { font-size: 0.75rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 6px; }
.stat-delta { font-size: 0.75rem; color: #10b981; margin-top: 4px; }
.event-card {
    background: #131c2e;
    border: 1px solid #1e2d45;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
}
.event-title { font-size: 1.05rem; font-weight: 700; color: #e2e8f0; margin-bottom: 6px; }
.event-meta { font-size: 0.82rem; color: #64748b; margin-bottom: 4px; }
.tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}
.tag-Tech     { background: rgba(59,130,246,0.15); color: #3b82f6; }
.tag-Cultural { background: rgba(139,92,246,0.15); color: #8b5cf6; }
.tag-Sports   { background: rgba(16,185,129,0.15); color: #10b981; }
.tag-Academic { background: rgba(245,158,11,0.15); color: #f59e0b; }
.tag-Arts     { background: rgba(6,182,212,0.15);  color: #06b6d4; }
.progress-wrap { background: #1e2d45; border-radius: 4px; height: 6px; margin-top: 8px; overflow: hidden; }
.progress-fill { height: 100%; border-radius: 4px; background: linear-gradient(90deg, #3b82f6, #06b6d4); }
.ai-banner {
    background: linear-gradient(135deg, rgba(6,182,212,0.1), rgba(59,130,246,0.07));
    border: 1px solid rgba(6,182,212,0.3);
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 20px;
}
.cert-card {
    background: linear-gradient(135deg, #0d1b2e, #1a2744);
    border: 2px solid rgba(59,130,246,0.3);
    border-radius: 14px;
    padding: 28px;
    text-align: center;
    margin-bottom: 16px;
}
.cert-title { font-size: 1rem; font-weight: 800; color: #06b6d4; letter-spacing: 0.1em; text-transform: uppercase; }
.cert-name  { font-size: 1.5rem; font-weight: 800; color: #e2e8f0; margin: 10px 0; }
.cert-event { font-size: 0.9rem; color: #3b82f6; margin-top: 6px; }
.cert-prize { font-size: 1rem; font-weight: 700; color: #f59e0b; margin: 6px 0; }
.notif-item {
    background: #131c2e;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 10px;
}
.notif-msg  { font-size: 0.87rem; color: #e2e8f0; line-height: 1.5; }
.notif-time { font-size: 0.72rem; color: #64748b; margin-top: 3px; }
.badge { display: inline-block; padding: 3px 10px; border-radius: 20px; font-size: 0.72rem; font-weight: 600; }
.badge-green  { background: rgba(16,185,129,0.15); color: #10b981; }
.badge-blue   { background: rgba(59,130,246,0.15); color: #3b82f6; }
.badge-orange { background: rgba(245,158,11,0.15); color: #f59e0b; }
.badge-purple { background: rgba(139,92,246,0.15); color: #8b5cf6; }
.badge-red    { background: rgba(239,68,68,0.15);  color: #ef4444; }
.section-title { font-size: 1.5rem; font-weight: 800; color: #e2e8f0; margin-bottom: 4px; }
.section-sub { font-size: 0.88rem; color: #64748b; margin-bottom: 20px; }
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── SAMPLE DATA (replace with CSV loading in production) ─────
@st.cache_data
def load_events():
    try:
        return pd.read_csv("events.csv")
    except FileNotFoundError:
        return pd.DataFrame([
            {"id": 1, "emoji": "⚡", "title": "CodeSprint 2025", "category": "Tech",
             "date": "Apr 20, 2025", "time": "10:00 AM", "venue": "CS Lab", "organizer": "CSE Dept",
             "description": "A fast-paced coding competition for all skill levels.", "registered": 45, "capacity": 60, "status": "Published"},
            {"id": 2, "emoji": "🎭", "title": "Cultural Fest 2025", "category": "Cultural",
             "date": "Apr 25, 2025", "time": "5:00 PM", "venue": "Auditorium", "organizer": "Cultural Club",
             "description": "Annual cultural extravaganza with dance, music and drama.", "registered": 120, "capacity": 200, "status": "Published"},
            {"id": 3, "emoji": "🏆", "title": "Inter-College Cricket", "category": "Sports",
             "date": "May 1, 2025", "time": "9:00 AM", "venue": "Sports Ground", "organizer": "Sports Dept",
             "description": "Inter-college cricket tournament. Register your team now.", "registered": 30, "capacity": 40, "status": "Published"},
            {"id": 4, "emoji": "🎨", "title": "Art Exhibition", "category": "Arts",
             "date": "May 5, 2025", "time": "11:00 AM", "venue": "Gallery Hall", "organizer": "Arts Club",
             "description": "Showcase your artwork and win exciting prizes.", "registered": 20, "capacity": 50, "status": "Published"},
            {"id": 5, "emoji": "📚", "title": "Research Paper Presentation", "category": "Academic",
             "date": "May 10, 2025", "time": "10:00 AM", "venue": "Seminar Hall", "organizer": "Research Cell",
             "description": "Present your research paper to faculty and industry experts.", "registered": 15, "capacity": 30, "status": "Published"},
        ])

@st.cache_data
def load_registrations():
    try:
        return pd.read_csv("my_registrations.csv")
    except FileNotFoundError:
        return pd.DataFrame([{"event_id": 1}, {"event_id": 2}])

@st.cache_data
def load_certificates():
    try:
        return pd.read_csv("certificates.csv")
    except FileNotFoundError:
        return pd.DataFrame([
            {"event_title": "CodeSprint 2024", "prize": "2nd Place", "date": "Nov 15, 2024", "issued_date": "Nov 20, 2024"},
            {"event_title": "HackFest 2024",   "prize": "Participant", "date": "Dec 10, 2024", "issued_date": "Dec 15, 2024"},
            {"event_title": "Cultural Night",  "prize": "1st Place",  "date": "Dec 20, 2024", "issued_date": "Dec 25, 2024"},
        ])

@st.cache_data
def load_notifications():
    try:
        return pd.read_csv("notifications.csv")
    except FileNotFoundError:
        return pd.DataFrame([
            {"message": "You have successfully registered for CodeSprint 2025.", "time": "2 hrs ago", "type": "success", "trigger": "Registration", "email_sent": "Yes", "whatsapp_sent": "Yes"},
            {"message": "Reminder: Cultural Fest 2025 starts in 3 days!", "time": "1 day ago", "type": "warning", "trigger": "Reminder", "email_sent": "Yes", "whatsapp_sent": "No"},
            {"message": "Your certificate for CodeSprint 2024 is ready to download.", "time": "3 days ago", "type": "info", "trigger": "Certificate", "email_sent": "Yes", "whatsapp_sent": "Yes"},
            {"message": "Results declared: You won 2nd Place in HackFest 2024!", "time": "1 week ago", "type": "success", "trigger": "Result", "email_sent": "Yes", "whatsapp_sent": "Yes"},
        ])

events_df        = load_events()
registrations_df = load_registrations()
certificates_df  = load_certificates()
notifications_df = load_notifications()


# ── SESSION STATE ─────────────────────────────────────────────
if "registered_ids" not in st.session_state:
    st.session_state.registered_ids = list(registrations_df["event_id"])
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "student_interests" not in st.session_state:
    st.session_state.student_interests = ["Tech", "Cultural", "Sports"]
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student_name" not in st.session_state:
    st.session_state.student_name = ""


# ══════════════════════════════════════════════════════════════
# PDF CERTIFICATE GENERATOR
# ══════════════════════════════════════════════════════════════
COLLEGE_NAME = "Mallareddy Engineering College for Women"
COLLEGE_TAGLINE = "Affiliated to JNTUH | NAAC Accredited | Hyderabad"

def generate_pdf_certificate(student_name, event_title, prize, date, issued_date):
    """Generate a professional PDF certificate using ReportLab canvas for full control."""
    buffer = io.BytesIO()
    
    # Landscape A4
    page_w, page_h = landscape(A4)  # 842 x 595 pts
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    
    # ── BACKGROUND ──────────────────────────────────────────
    c.setFillColor(colors.HexColor("#0a0e1a"))
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    
    # ── OUTER BORDER (double) ────────────────────────────────
    border_margin = 18
    # Outer gold border
    c.setStrokeColor(colors.HexColor("#b8860b"))
    c.setLineWidth(3)
    c.rect(border_margin, border_margin, page_w - 2*border_margin, page_h - 2*border_margin, fill=0, stroke=1)
    # Inner blue border
    c.setStrokeColor(colors.HexColor("#3b82f6"))
    c.setLineWidth(1.2)
    inner_m = border_margin + 8
    c.rect(inner_m, inner_m, page_w - 2*inner_m, page_h - 2*inner_m, fill=0, stroke=1)
    
    # ── CORNER ORNAMENTS ────────────────────────────────────
    ornament_size = 22
    corners = [
        (border_margin, border_margin),                          # bottom-left
        (page_w - border_margin, border_margin),                 # bottom-right
        (border_margin, page_h - border_margin),                 # top-left
        (page_w - border_margin, page_h - border_margin),        # top-right
    ]
    c.setFillColor(colors.HexColor("#b8860b"))
    for cx, cy in corners:
        c.circle(cx, cy, 5, fill=1, stroke=0)

    # ── TOP HEADER BAND ──────────────────────────────────────
    c.setFillColor(colors.HexColor("#0d1b2e"))
    c.rect(inner_m + 1, page_h - inner_m - 70, page_w - 2*inner_m - 2, 68, fill=1, stroke=0)

    # College name in header
    c.setFont("Times-Bold", 16)
    c.setFillColor(colors.HexColor("#3b82f6"))
    c.drawCentredString(page_w / 2, page_h - inner_m - 25, COLLEGE_NAME.upper())

    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawCentredString(page_w / 2, page_h - inner_m - 42, COLLEGE_TAGLINE)

    # Divider below header
    c.setStrokeColor(colors.HexColor("#b8860b"))
    c.setLineWidth(1)
    c.line(inner_m + 20, page_h - inner_m - 72, page_w - inner_m - 20, page_h - inner_m - 72)

    # ── TITLE "CERTIFICATE OF ACHIEVEMENT" ──────────────────
    c.setFont("Times-Bold", 28)
    c.setFillColor(colors.HexColor("#e2e8f0"))
    c.drawCentredString(page_w / 2, page_h - inner_m - 115, "CERTIFICATE OF ACHIEVEMENT")

    # Decorative line under title
    line_y = page_h - inner_m - 124
    c.setStrokeColor(colors.HexColor("#06b6d4"))
    c.setLineWidth(1.5)
    c.line(page_w/2 - 180, line_y, page_w/2 + 180, line_y)

    # ── "This is to certify that" ────────────────────────────
    c.setFont("Helvetica-Oblique", 13)
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.drawCentredString(page_w / 2, page_h - inner_m - 152, "This is to certify that")

    # ── STUDENT NAME ─────────────────────────────────────────
    c.setFont("Times-BoldItalic", 34)
    c.setFillColor(colors.HexColor("#06b6d4"))
    c.drawCentredString(page_w / 2, page_h - inner_m - 195, student_name)

    # Underline for name
    name_y = page_h - inner_m - 202
    c.setStrokeColor(colors.HexColor("#b8860b"))
    c.setLineWidth(0.8)
    c.line(page_w/2 - 140, name_y, page_w/2 + 140, name_y)

    # ── "has been awarded" ───────────────────────────────────
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.drawCentredString(page_w / 2, page_h - inner_m - 228, "has been awarded")

    # ── PRIZE ────────────────────────────────────────────────
    prize_emojis = {"1st Place": "🥇", "2nd Place": "🥈", "3rd Place": "🥉", "Participant": "🏅"}
    prize_label = f"{prize_emojis.get(prize, '🏅')}  {prize}"
    c.setFont("Times-Bold", 22)
    c.setFillColor(colors.HexColor("#f59e0b"))
    c.drawCentredString(page_w / 2, page_h - inner_m - 262, prize)

    # ── "in the event" ───────────────────────────────────────
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.HexColor("#94a3b8"))
    c.drawCentredString(page_w / 2, page_h - inner_m - 290, "in the event")

    # ── EVENT TITLE ──────────────────────────────────────────
    c.setFont("Times-Bold", 19)
    c.setFillColor(colors.HexColor("#3b82f6"))
    c.drawCentredString(page_w / 2, page_h - inner_m - 318, event_title)

    # ── HORIZONTAL GOLD DIVIDER ──────────────────────────────
    div_y = page_h - inner_m - 340
    c.setStrokeColor(colors.HexColor("#b8860b"))
    c.setLineWidth(0.8)
    c.line(inner_m + 40, div_y, page_w - inner_m - 40, div_y)

    # ── BOTTOM ROW: Date | Seal placeholder | Signature ──────
    bottom_y = page_h - inner_m - 390

    # Left: Event Date
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawCentredString(page_w * 0.22, bottom_y + 18, "DATE OF EVENT")
    c.setFont("Times-Bold", 13)
    c.setFillColor(colors.HexColor("#e2e8f0"))
    c.drawCentredString(page_w * 0.22, bottom_y, date)

    # Center: Circular seal
    seal_x, seal_y = page_w / 2, bottom_y + 5
    c.setFillColor(colors.HexColor("#0d1b2e"))
    c.setStrokeColor(colors.HexColor("#b8860b"))
    c.setLineWidth(2)
    c.circle(seal_x, seal_y, 38, fill=1, stroke=1)
    c.setStrokeColor(colors.HexColor("#3b82f6"))
    c.setLineWidth(1)
    c.circle(seal_x, seal_y, 32, fill=0, stroke=1)
    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(colors.HexColor("#b8860b"))
    c.drawCentredString(seal_x, seal_y + 10, "MRECW")
    c.setFont("Helvetica", 6)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawCentredString(seal_x, seal_y - 2, "OFFICIAL")
    c.drawCentredString(seal_x, seal_y - 12, "SEAL")

    # Right: Issued date / Principal signature line
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawCentredString(page_w * 0.78, bottom_y + 18, "ISSUED DATE")
    c.setFont("Times-Bold", 13)
    c.setFillColor(colors.HexColor("#e2e8f0"))
    c.drawCentredString(page_w * 0.78, bottom_y, issued_date)

    # Signature line under right column
    sig_y = bottom_y - 22
    c.setStrokeColor(colors.HexColor("#3b82f6"))
    c.setLineWidth(0.8)
    c.line(page_w * 0.64, sig_y, page_w * 0.91, sig_y)
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#64748b"))
    c.drawCentredString(page_w * 0.78, sig_y - 12, "Principal / Event Coordinator")

    # ── FOOTER ───────────────────────────────────────────────
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor("#334155"))
    c.drawCentredString(page_w / 2, inner_m + 12,
        f"Issued by CEMS — College Event Management System  |  {COLLEGE_NAME}")

    c.save()
    buffer.seek(0)
    return buffer.read()


# ══════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════
def show_login():
    st.markdown(
        "<div style='text-align:center; margin-top:60px; margin-bottom:30px;'>"
        "<div style='font-size:2.5rem; font-weight:900; color:#e2e8f0; letter-spacing:-0.03em;'>"
        "CE<span style='color:#3b82f6;'>MS</span></div>"
        "<div style='color:#64748b; font-size:1rem; margin-top:6px;'>College Event Management System</div>"
        f"<div style='color:#3b82f6; font-size:0.85rem; margin-top:4px;'>{COLLEGE_NAME}</div>"
        "</div>",
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("#### 🎓 Student Login")
        name  = st.text_input("Full Name", placeholder="e.g. Priya Sharma")
        email = st.text_input("Email", placeholder="you@mrecw.edu.in")
        _     = st.text_input("Password", type="password", placeholder="••••••••")
        st.markdown("**Select your interests** (for AI recommendations)")
        interests = st.multiselect(
            "Interests",
            ["Tech", "Cultural", "Sports", "Academic", "Arts", "Finance"],
            default=["Tech", "Cultural"],
            label_visibility="collapsed"
        )
        if st.button("🚀 Sign In", use_container_width=True, type="primary"):
            if name and email:
                st.session_state.logged_in         = True
                st.session_state.student_name      = name
                st.session_state.student_interests = interests if interests else ["Tech"]
                st.rerun()
            else:
                st.error("Please enter your name and email.")
        st.markdown(
            "<div style='text-align:center; margin-top:12px; color:#64748b; font-size:0.82rem;'>"
            "Demo app — enter any name and email to login</div>",
            unsafe_allow_html=True
        )


# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
def show_sidebar():
    with st.sidebar:
        st.markdown(
            "<div style='padding:10px 0 16px;'>"
            "<div style='font-size:1.3rem; font-weight:900; color:#e2e8f0;'>"
            "CE<span style='color:#3b82f6;'>MS</span></div>"
            "<div style='font-size:0.7rem; color:#64748b; text-transform:uppercase; "
            "letter-spacing:0.08em; margin-top:2px;'>Student Portal</div></div>",
            unsafe_allow_html=True
        )
        st.divider()
        pages = {
            "🏠  Dashboard":        "Dashboard",
            "🎉  Browse Events":    "Browse Events",
            "📋  My Registrations": "My Registrations",
            "🏅  My Certificates":  "My Certificates",
            "🔔  Notifications":    "Notifications",
            "👤  Profile":          "Profile",
        }
        for label, page_name in pages.items():
            is_active = st.session_state.page == page_name
            if st.button(label, key=f"nav_{page_name}", use_container_width=True,
                         type="primary" if is_active else "secondary"):
                st.session_state.page = page_name
                st.rerun()
        st.divider()
        initials = "".join([w[0].upper() for w in st.session_state.student_name.split()[:2]])
        st.markdown(
            f"<div style='display:flex; align-items:center; gap:10px; padding:4px 0;'>"
            f"<div style='width:36px; height:36px; border-radius:50%; background:rgba(59,130,246,0.25); "
            f"color:#3b82f6; display:flex; align-items:center; justify-content:center; "
            f"font-weight:700; font-size:0.85rem;'>{initials}</div>"
            f"<div><div style='font-size:0.88rem; font-weight:500; color:#e2e8f0;'>"
            f"{st.session_state.student_name}</div>"
            f"<div style='font-size:0.72rem; color:#64748b;'>Student</div></div></div>",
            unsafe_allow_html=True
        )
        if st.button("⎋  Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page      = "Dashboard"
            st.rerun()


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
def tag_html(category):
    return f'<span class="tag tag-{category}">{category}</span>'

def badge_html(text, color="blue"):
    return f'<span class="badge badge-{color}">{text}</span>'

def seats_bar(registered, capacity):
    pct   = int((registered / capacity) * 100)
    color = "#ef4444" if pct >= 95 else "#f59e0b" if pct >= 80 else "#3b82f6"
    return (
        f"<div class='progress-wrap'>"
        f"<div class='progress-fill' style='width:{pct}%; background:{color};'></div></div>"
        f"<div style='font-size:0.72rem; color:#64748b; margin-top:3px;'>"
        f"{capacity - registered} seats left ({pct}% full)</div>"
    )

def ai_recommendations(interests):
    rec = events_df[
        (events_df["category"].isin(interests)) &
        (~events_df["id"].isin(st.session_state.registered_ids)) &
        (events_df["status"] == "Published")
    ]
    return rec.head(3)


# ══════════════════════════════════════════════════════════════
# PAGE 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════
def page_dashboard():
    name = st.session_state.student_name.split()[0]
    st.markdown(
        f"<div class='section-title'>Good morning, {name} 👋</div>"
        "<div class='section-sub'>Here's what's happening on campus today.</div>",
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)
    reg_count  = len(st.session_state.registered_ids)
    cert_count = len(certificates_df)
    interests_str = " · ".join(st.session_state.student_interests[:3])

    for col, emoji, number, label, delta in [
        (c1, "🎉", reg_count,  "Registered Events", "↑ Active"),
        (c2, "🏅", cert_count, "Certificates",      "↑ 1 new"),
        (c3, "📬", len(notifications_df), "Notifications", "2 unread"),
        (c4, "🤖", "AI",      "Recommendations",   interests_str),
    ]:
        with col:
            st.markdown(
                f"<div class='stat-card'><div style='font-size:1.6rem;'>{emoji}</div>"
                f"<div class='stat-number'>{number}</div>"
                f"<div class='stat-label'>{label}</div>"
                f"<div class='stat-delta'>{delta}</div></div>",
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    recs = ai_recommendations(st.session_state.student_interests)
    st.markdown(
        f"<div class='ai-banner'><b style='color:#06b6d4;'>🤖 AI Recommendations Active</b><br>"
        f"<span style='font-size:0.82rem; color:#64748b;'>Based on your interests "
        f"({', '.join(st.session_state.student_interests)}) — {len(recs)} events match your profile.</span></div>",
        unsafe_allow_html=True
    )

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### ✨ Recommended for You")
        if len(recs) == 0:
            st.info("No new recommendations. Update your interests in Profile.")
        else:
            for _, row in recs.iterrows():
                st.markdown(
                    f"<div class='event-card'>"
                    f"<div style='display:flex; align-items:center; gap:12px;'>"
                    f"<div style='font-size:1.8rem;'>{row['emoji']}</div>"
                    f"<div style='flex:1;'>{tag_html(row['category'])}"
                    f"<div class='event-title'>{row['title']}</div>"
                    f"<div class='event-meta'>📅 {row['date']} · {row['venue']}</div>"
                    f"{seats_bar(row['registered'], row['capacity'])}</div>"
                    f"<div style='color:#64748b; font-size:0.85rem;'>✨ For You</div>"
                    f"</div></div>",
                    unsafe_allow_html=True
                )

    with col_right:
        st.markdown("#### 🔔 Recent Notifications")
        dot_colors = {"info": "#3b82f6", "success": "#10b981", "warning": "#f59e0b"}
        for _, row in notifications_df.head(4).iterrows():
            dot = dot_colors.get(row["type"], "#64748b")
            st.markdown(
                f"<div class='notif-item'>"
                f"<div style='display:flex; gap:10px; align-items:flex-start;'>"
                f"<div style='width:10px; height:10px; border-radius:50%; background:{dot}; "
                f"margin-top:5px; flex-shrink:0;'></div>"
                f"<div><div class='notif-msg'>{row['message']}</div>"
                f"<div class='notif-time'>{row['time']} &nbsp;"
                f"<span class='badge badge-blue'>📧 Email</span> &nbsp;"
                f"<span class='badge badge-green'>💬 WhatsApp</span></div>"
                f"</div></div></div>",
                unsafe_allow_html=True
            )

    st.markdown("#### 📋 My Upcoming Events")
    my_events = events_df[events_df["id"].isin(st.session_state.registered_ids)]
    if len(my_events) == 0:
        st.info("You have no registered events. Browse events to register!")
    else:
        display_df = my_events[["emoji","title","category","date","venue"]].copy()
        display_df.columns = ["","Event","Category","Date","Venue"]
        st.dataframe(display_df, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# PAGE 2 — BROWSE EVENTS
# ══════════════════════════════════════════════════════════════
def page_browse_events():
    st.markdown(
        "<div class='section-title'>Browse Events</div>"
        "<div class='section-sub'>Discover and register for upcoming campus events.</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='ai-banner'><b style='color:#06b6d4;'>✨ AI Recommendations Active</b><br>"
        "<span style='font-size:0.78rem; color:#64748b;'>Events marked ✨ match your interest tags.</span></div>",
        unsafe_allow_html=True
    )

    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search = st.text_input("🔍 Search events", placeholder="Search by name or category...")
    with col_filter:
        categories = ["All"] + list(events_df["category"].unique())
        selected_cat = st.selectbox("Filter by Category", categories)

    filtered = events_df[events_df["status"] == "Published"].copy()
    if search:
        filtered = filtered[
            filtered["title"].str.contains(search, case=False) |
            filtered["category"].str.contains(search, case=False)
        ]
    if selected_cat != "All":
        filtered = filtered[filtered["category"] == selected_cat]

    st.markdown(f"**{len(filtered)} events found**")
    st.markdown("<br>", unsafe_allow_html=True)

    cols = st.columns(2)
    for idx, (_, row) in enumerate(filtered.iterrows()):
        is_reg  = row["id"] in st.session_state.registered_ids
        is_rec  = row["category"] in st.session_state.student_interests
        is_full = row["registered"] >= row["capacity"]
        rec_label = '<span style="color:#06b6d4; font-size:0.72rem; font-weight:600; margin-left:6px;">✨ For You</span>' if is_rec else ""

        with cols[idx % 2]:
            st.markdown(
                f"<div class='event-card'>"
                f"<div style='display:flex; justify-content:space-between; align-items:flex-start;'>"
                f"<div>{tag_html(row['category'])}{rec_label}</div>"
                f"<div style='font-size:1.8rem;'>{row['emoji']}</div></div>"
                f"<div class='event-title'>{row['title']}</div>"
                f"<div class='event-meta'>📅 {row['date']} · {row['time']}</div>"
                f"<div class='event-meta'>📍 {row['venue']}</div>"
                f"<div class='event-meta'>👤 {row['organizer']}</div>"
                f"<div style='font-size:0.8rem; color:#64748b; margin:8px 0;'>{str(row['description'])[:90]}...</div>"
                f"{seats_bar(row['registered'], row['capacity'])}"
                f"</div>",
                unsafe_allow_html=True
            )
            if is_reg:
                st.success("✓ Already Registered")
            elif is_full:
                st.error("Event Full")
            else:
                if st.button(f"Register — {row['title'][:22]}", key=f"reg_{row['id']}",
                             use_container_width=True, type="primary"):
                    st.session_state.registered_ids.append(row["id"])
                    st.success(f"✅ Registered for {row['title']}! Confirmation sent via Email & WhatsApp.")
                    st.rerun()


# ══════════════════════════════════════════════════════════════
# PAGE 3 — MY REGISTRATIONS
# ══════════════════════════════════════════════════════════════
def page_my_registrations():
    st.markdown(
        "<div class='section-title'>My Registrations</div>"
        "<div class='section-sub'>Track all your event registrations and status.</div>",
        unsafe_allow_html=True
    )
    my_events = events_df[events_df["id"].isin(st.session_state.registered_ids)]
    total     = len(my_events)

    c1, c2, c3, c4 = st.columns(4)
    for col, emoji, number, label in [
        (c1, "📋", total, "Registered"),
        (c2, "⏳", total, "Upcoming"),
        (c3, "✅", 2,     "Attended"),
        (c4, "🏆", 1,     "Prize Won"),
    ]:
        with col:
            st.markdown(
                f"<div class='stat-card'><div style='font-size:1.4rem;'>{emoji}</div>"
                f"<div class='stat-number'>{number}</div>"
                f"<div class='stat-label'>{label}</div></div>",
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### Active Registrations")

    if len(my_events) == 0:
        st.info("You have not registered for any events yet.")
    else:
        for _, row in my_events.iterrows():
            col_info, col_btn = st.columns([4, 1])
            with col_info:
                st.markdown(
                    f"<div class='event-card'>"
                    f"<div style='display:flex; gap:14px; align-items:center;'>"
                    f"<div style='font-size:2rem;'>{row['emoji']}</div>"
                    f"<div style='flex:1;'>{tag_html(row['category'])}"
                    f"<div class='event-title'>{row['title']}</div>"
                    f"<div class='event-meta'>📅 {row['date']} &nbsp;|&nbsp; 📍 {row['venue']}</div></div>"
                    f"<div>{badge_html('● Registered', 'green')}</div>"
                    f"</div></div>",
                    unsafe_allow_html=True
                )
            with col_btn:
                st.markdown("<br><br>", unsafe_allow_html=True)
                if st.button("Cancel", key=f"cancel_{row['id']}", type="secondary"):
                    st.session_state.registered_ids.remove(row["id"])
                    st.warning(f"Registration for {row['title']} cancelled.")
                    st.rerun()

    st.markdown("#### Past Events")
    past_data = {
        "Event":  ["⚡ CodeSprint 2024", "💻 HackFest 2024", "🎭 Cultural Night 2024"],
        "Date":   ["Nov 15, 2024",       "Dec 10, 2024",      "Dec 20, 2024"],
        "Result": ["2nd Place 🥈",        "Participant 🏅",     "Participant 🏅"],
        "Status": ["Completed",           "Completed",          "Completed"],
    }
    st.dataframe(pd.DataFrame(past_data), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# PAGE 4 — MY CERTIFICATES
# ══════════════════════════════════════════════════════════════
def page_certificates():
    st.markdown(
        "<div class='section-title'>My Certificates</div>"
        "<div class='section-sub'>Download your professional PDF certificates.</div>",
        unsafe_allow_html=True
    )

    if not REPORTLAB_AVAILABLE:
        st.warning("⚠️ ReportLab is not installed. Run: `pip install reportlab` to enable PDF certificates.")

    prize_emojis = {"1st Place": "🥇", "2nd Place": "🥈", "3rd Place": "🥉", "Participant": "🏅"}
    cols = st.columns(2)

    for idx, (_, row) in enumerate(certificates_df.iterrows()):
        with cols[idx % 2]:
            prize_emoji = prize_emojis.get(row["prize"], "🏅")
            st.markdown(
                f"<div class='cert-card'>"
                f"<div class='cert-title'>Certificate of Achievement</div>"
                f"<div style='font-size:0.72rem; color:#64748b; letter-spacing:0.15em; margin-top:4px;'>"
                f"This is to certify that</div>"
                f"<div class='cert-name'>{st.session_state.student_name}</div>"
                f"<div style='width:60%; height:1px; margin:10px auto; "
                f"background:linear-gradient(90deg,transparent,#3b82f6,transparent);'></div>"
                f"<div style='font-size:0.85rem; color:#64748b;'>has been awarded</div>"
                f"<div class='cert-prize'>{prize_emoji} {row['prize']}</div>"
                f"<div class='cert-event'>{row['event_title']}</div>"
                f"<div style='font-size:0.75rem; color:#64748b; margin-top:10px;'>"
                f"{row['date']} &nbsp;|&nbsp; Issued: {row['issued_date']}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

            if REPORTLAB_AVAILABLE:
                pdf_bytes = generate_pdf_certificate(
                    student_name  = st.session_state.student_name,
                    event_title   = row["event_title"],
                    prize         = row["prize"],
                    date          = row["date"],
                    issued_date   = row["issued_date"]
                )
                safe_name = str(row["event_title"]).replace(" ", "_")
                st.download_button(
                    label=f"⬇ Download PDF Certificate",
                    data=pdf_bytes,
                    file_name=f"Certificate_{safe_name}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key=f"dl_cert_{idx}"
                )
            else:
                st.button("⬇ Download PDF (install reportlab)", disabled=True,
                          use_container_width=True, key=f"dl_cert_{idx}")

            st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 5 — NOTIFICATIONS
# ══════════════════════════════════════════════════════════════
def page_notifications():
    st.markdown(
        "<div class='section-title'>Notifications</div>"
        "<div class='section-sub'>Your complete Email &amp; WhatsApp notification history.</div>",
        unsafe_allow_html=True
    )
    dot_colors = {"info": "#3b82f6", "success": "#10b981", "warning": "#f59e0b", "error": "#ef4444"}
    filter_type = st.selectbox("Filter", ["All","Registration","Reminder","Result","Certificate"],
                               label_visibility="collapsed")

    filtered_notifs = notifications_df.copy()
    if filter_type != "All":
        filtered_notifs = filtered_notifs[
            filtered_notifs["trigger"].str.contains(filter_type, case=False)
        ]

    st.markdown(f"**{len(filtered_notifs)} notifications**")
    st.markdown("<br>", unsafe_allow_html=True)

    for _, row in filtered_notifs.iterrows():
        dot = dot_colors.get(row["type"], "#64748b")
        email_badge    = badge_html("📧 Email",    "blue")  if row["email_sent"]    == "Yes" else ""
        whatsapp_badge = badge_html("💬 WhatsApp", "green") if row["whatsapp_sent"] == "Yes" else ""
        st.markdown(
            f"<div class='notif-item'>"
            f"<div style='display:flex; gap:12px; align-items:flex-start;'>"
            f"<div style='width:12px; height:12px; border-radius:50%; background:{dot}; "
            f"margin-top:4px; flex-shrink:0;'></div>"
            f"<div style='flex:1;'>"
            f"<div class='notif-msg'>{row['message']}</div>"
            f"<div class='notif-time' style='margin-top:6px;'>"
            f"{row['time']} &nbsp; {email_badge} &nbsp; {whatsapp_badge}</div>"
            f"</div></div></div>",
            unsafe_allow_html=True
        )


# ══════════════════════════════════════════════════════════════
# PAGE 6 — PROFILE
# ══════════════════════════════════════════════════════════════
def page_profile():
    st.markdown(
        "<div class='section-title'>My Profile</div>"
        "<div class='section-sub'>Manage your account and AI interest preferences.</div>",
        unsafe_allow_html=True
    )
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 👤 Personal Information")
        name  = st.text_input("Full Name",  value=st.session_state.student_name)
        email = st.text_input("Email",      value="student@mrecw.edu.in")
        phone = st.text_input("Phone (WhatsApp)", value="+91 98765 43210")
        dept  = st.text_input("Department", value="Computer Science Engineering")
        year  = st.selectbox("Year", ["1st Year","2nd Year","3rd Year","4th Year"], index=2)
        if st.button("💾 Save Profile", use_container_width=True, type="primary"):
            st.session_state.student_name = name
            st.success("✅ Profile updated successfully!")

    with col_right:
        st.markdown("#### 🤖 AI Interest Tags")
        st.markdown(
            "<div style='font-size:0.85rem; color:#64748b; margin-bottom:12px;'>"
            "Select topics you are interested in. The AI engine will recommend "
            "matching events on your dashboard.</div>",
            unsafe_allow_html=True
        )
        all_interests = ["Tech", "Cultural", "Sports", "Academic", "Arts", "Finance"]
        selected = st.multiselect("Your Interests", all_interests,
                                  default=st.session_state.student_interests,
                                  label_visibility="collapsed")
        if st.button("🤖 Update AI Preferences", use_container_width=True):
            st.session_state.student_interests = selected
            st.success(f"✅ AI engine updated! Now tracking: {', '.join(selected)}")

        badge_str = "".join([f"<span class='badge badge-blue'>{i}</span> " for i in selected])
        st.markdown(
            f"<div style='background:#1a2235; border-radius:12px; padding:16px; margin-top:14px; border:1px solid #1e2d45;'>"
            f"<div style='font-weight:700; color:#06b6d4; margin-bottom:8px; font-size:0.9rem;'>🤖 AI Engine Status</div>"
            f"<div style='color:#64748b; font-size:0.82rem; margin-bottom:10px;'>"
            f"Active · Matching events to your {len(selected)} selected interests</div>"
            f"<div style='display:flex; flex-wrap:wrap; gap:6px;'>{badge_str}</div></div>",
            unsafe_allow_html=True
        )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📊 My Stats")
        stats_data = {
            "Metric": ["Events Registered","Events Attended","Certificates Earned","Prizes Won","Notifications"],
            "Count":  [len(st.session_state.registered_ids), 2, 3, 1, len(notifications_df)]
        }
        st.dataframe(pd.DataFrame(stats_data), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# MAIN ROUTER
# ══════════════════════════════════════════════════════════════
def main():
    if not st.session_state.logged_in:
        show_login()
        return
    show_sidebar()
    page = st.session_state.page
    if   page == "Dashboard":        page_dashboard()
    elif page == "Browse Events":    page_browse_events()
    elif page == "My Registrations": page_my_registrations()
    elif page == "My Certificates":  page_certificates()
    elif page == "Notifications":    page_notifications()
    elif page == "Profile":          page_profile()

if __name__ == "__main__":
    main()
