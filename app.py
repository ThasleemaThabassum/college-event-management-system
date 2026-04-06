# ============================================================
#  CEMS — College Event Management System
#  Student Dashboard — Streamlit App
#  File: app.py
#  Run: streamlit run app.py
# ============================================================

import streamlit as st
import pandas as pd
from datetime import datetime

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
/* Overall background */
.stApp { background-color: #0a0e1a; color: #e2e8f0; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1e2d45;
}

/* Stat cards */
.stat-card {
    background: #131c2e;
    border: 1px solid #1e2d45;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
    margin-bottom: 10px;
    transition: border-color 0.2s;
}
.stat-card:hover { border-color: #3b82f6; }
.stat-number {
    font-size: 2.2rem;
    font-weight: 800;
    color: #e2e8f0;
    line-height: 1;
}
.stat-label {
    font-size: 0.75rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 6px;
}
.stat-delta { font-size: 0.75rem; color: #10b981; margin-top: 4px; }

/* Event cards */
.event-card {
    background: #131c2e;
    border: 1px solid #1e2d45;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
    transition: border-color 0.2s, transform 0.2s;
}
.event-card:hover { border-color: #3b82f6; transform: translateY(-2px); }
.event-title { font-size: 1.05rem; font-weight: 700; color: #e2e8f0; margin-bottom: 6px; }
.event-meta { font-size: 0.82rem; color: #64748b; margin-bottom: 4px; }

/* Tags */
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

/* Progress bar custom */
.progress-wrap {
    background: #1e2d45;
    border-radius: 4px;
    height: 6px;
    margin-top: 8px;
    overflow: hidden;
}
.progress-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, #3b82f6, #06b6d4);
}

/* AI banner */
.ai-banner {
    background: linear-gradient(135deg, rgba(6,182,212,0.1), rgba(59,130,246,0.07));
    border: 1px solid rgba(6,182,212,0.3);
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}

/* Certificate card */
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
.cert-divider {
    width: 60%; height: 1px; margin: 10px auto;
    background: linear-gradient(90deg, transparent, #3b82f6, transparent);
}

/* Notification items */
.notif-item {
    background: #131c2e;
    border: 1px solid #1e2d45;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 10px;
    display: flex;
    gap: 12px;
    align-items: flex-start;
}
.notif-dot {
    width: 10px; height: 10px; border-radius: 50%;
    margin-top: 4px; flex-shrink: 0;
}
.notif-msg  { font-size: 0.87rem; color: #e2e8f0; line-height: 1.5; }
.notif-time { font-size: 0.72rem; color: #64748b; margin-top: 3px; }

/* Badge */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
}
.badge-green  { background: rgba(16,185,129,0.15); color: #10b981; }
.badge-blue   { background: rgba(59,130,246,0.15); color: #3b82f6; }
.badge-orange { background: rgba(245,158,11,0.15); color: #f59e0b; }
.badge-purple { background: rgba(139,92,246,0.15); color: #8b5cf6; }
.badge-red    { background: rgba(239,68,68,0.15);  color: #ef4444; }

/* Page section headers */
.section-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: #e2e8f0;
    margin-bottom: 4px;
}
.section-sub { font-size: 0.88rem; color: #64748b; margin-bottom: 20px; }

/* Hide Streamlit default elements */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ── LOAD DATA ─────────────────────────────────────────────────
@st.cache_data
def load_events():
    return pd.read_csv("events.csv")

@st.cache_data
def load_registrations():
    return pd.read_csv("my_registrations.csv")

@st.cache_data
def load_certificates():
    return pd.read_csv("certificates.csv")

@st.cache_data
def load_notifications():
    return pd.read_csv("notifications.csv")

events_df        = load_events()
registrations_df = load_registrations()
certificates_df  = load_certificates()
notifications_df = load_notifications()


# ── SESSION STATE ─────────────────────────────────────────────
# Track which events the student has registered for (by ID)
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
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════
def show_login():
    st.markdown("""
    <div style='text-align:center; margin-top: 60px; margin-bottom: 30px;'>
        <div style='font-size:2.5rem; font-weight:900; color:#e2e8f0; letter-spacing:-0.03em;'>
            CE<span style='color:#3b82f6;'>MS</span>
        </div>
        <div style='color:#64748b; font-size:1rem; margin-top:6px;'>
            College Event Management System
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("#### 🎓 Student Login")
        name  = st.text_input("Full Name", placeholder="e.g. Alex Johnson")
        email = st.text_input("Email", placeholder="you@college.edu")
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
                st.session_state.logged_in        = True
                st.session_state.student_name     = name
                st.session_state.student_interests = interests if interests else ["Tech"]
                st.rerun()
            else:
                st.error("Please enter your name and email.")

        st.markdown("""
        <div style='text-align:center; margin-top:12px; color:#64748b; font-size:0.82rem;'>
            Demo app — enter any name and email to login
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
def show_sidebar():
    with st.sidebar:
        # Brand
        st.markdown("""
        <div style='padding: 10px 0 16px;'>
            <div style='font-size:1.3rem; font-weight:900; color:#e2e8f0;'>
                CE<span style='color:#3b82f6;'>MS</span>
            </div>
            <div style='font-size:0.7rem; color:#64748b; text-transform:uppercase;
                        letter-spacing:0.08em; margin-top:2px;'>
                Student Portal
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Navigation
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
            if st.button(
                label,
                key=f"nav_{page_name}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.page = page_name
                st.rerun()

        st.divider()

        # User info at bottom
        initials = "".join([w[0].upper() for w in st.session_state.student_name.split()[:2]])
        st.markdown(f"""
        <div style='display:flex; align-items:center; gap:10px; padding:4px 0;'>
            <div style='width:36px; height:36px; border-radius:50%;
                        background:rgba(59,130,246,0.25); color:#3b82f6;
                        display:flex; align-items:center; justify-content:center;
                        font-weight:700; font-size:0.85rem; flex-shrink:0;'>
                {initials}
            </div>
            <div>
                <div style='font-size:0.88rem; font-weight:500; color:#e2e8f0;'>
                    {st.session_state.student_name}
                </div>
                <div style='font-size:0.72rem; color:#64748b;'>Student</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("⎋  Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.page      = "Dashboard"
            st.rerun()


# ══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════
def tag_html(category):
    return f'<span class="tag tag-{category}">{category}</span>'

def badge_html(text, color="blue"):
    return f'<span class="badge badge-{color}">{text}</span>'

def seats_bar(registered, capacity):
    pct = int((registered / capacity) * 100)
    color = "#ef4444" if pct >= 95 else "#f59e0b" if pct >= 80 else "#3b82f6"
    return f"""
    <div class='progress-wrap'>
        <div class='progress-fill' style='width:{pct}%; background:{color};'></div>
    </div>
    <div style='font-size:0.72rem; color:#64748b; margin-top:3px;'>
        {capacity - registered} seats left ({pct}% full)
    </div>
    """

def ai_recommendations(interests):
    """Return events matching student interests, not yet registered."""
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
    st.markdown(f"""
    <div class='section-title'>Good morning, {name} 👋</div>
    <div class='section-sub'>Here's what's happening on campus today.</div>
    """, unsafe_allow_html=True)

    # ── STAT CARDS ──
    c1, c2, c3, c4 = st.columns(4)
    reg_count  = len(st.session_state.registered_ids)
    cert_count = len(certificates_df)

    with c1:
        st.markdown(f"""
        <div class='stat-card'>
            <div style='font-size:1.6rem;'>🎉</div>
            <div class='stat-number'>{reg_count}</div>
            <div class='stat-label'>Registered Events</div>
            <div class='stat-delta'>↑ Active</div>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class='stat-card'>
            <div style='font-size:1.6rem;'>🏅</div>
            <div class='stat-number'>{cert_count}</div>
            <div class='stat-label'>Certificates</div>
            <div class='stat-delta'>↑ 1 new</div>
        </div>""", unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class='stat-card'>
            <div style='font-size:1.6rem;'>📬</div>
            <div class='stat-number'>{len(notifications_df)}</div>
            <div class='stat-label'>Notifications</div>
            <div class='stat-delta'>2 unread</div>
        </div>""", unsafe_allow_html=True)

    with c4:
        interests_str = " · ".join(st.session_state.student_interests[:3])
        st.markdown(f"""
        <div class='stat-card'>
            <div style='font-size:1.6rem;'>🤖</div>
            <div class='stat-number'>AI</div>
            <div class='stat-label'>Recommendations</div>
            <div class='stat-delta'>{interests_str}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── AI BANNER ──
    recs = ai_recommendations(st.session_state.student_interests)
    st.markdown(f"""
    <div class='ai-banner'>
        <div style='font-size:1.8rem;'>🤖</div>
        <div>
            <div style='font-weight:700; color:#06b6d4; font-size:0.95rem;'>
                AI Recommendations Active
            </div>
            <div style='font-size:0.82rem; color:#64748b; margin-top:2px;'>
                Based on your interests ({", ".join(st.session_state.student_interests)})
                — {len(recs)} events match your profile.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    # ── LEFT: Recommended Events ──
    with col_left:
        st.markdown("#### ✨ Recommended for You")
        if len(recs) == 0:
            st.info("No new recommendations. Update your interests in Profile.")
        else:
            for _, row in recs.iterrows():
                pct = int((row["registered"] / row["capacity"]) * 100)
                st.markdown(f"""
                <div class='event-card'>
                    <div style='display:flex; align-items:center; gap:12px;'>
                        <div style='font-size:1.8rem;'>{row['emoji']}</div>
                        <div style='flex:1;'>
                            {tag_html(row['category'])}
                            <div class='event-title'>{row['title']}</div>
                            <div class='event-meta'>📅 {row['date']} · {row['venue']}</div>
                            {seats_bar(row['registered'], row['capacity'])}
                        </div>
                        <div style='color:#64748b; font-size:0.85rem;'>✨ For You</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── RIGHT: Recent Notifications ──
    with col_right:
        st.markdown("#### 🔔 Recent Notifications")
        dot_colors = {
            "info": "#3b82f6",
            "success": "#10b981",
            "warning": "#f59e0b"
        }
        for _, row in notifications_df.head(4).iterrows():
            dot = dot_colors.get(row["type"], "#64748b")
            st.markdown(f"""
            <div class='notif-item'>
                <div class='notif-dot' style='background:{dot};'></div>
                <div>
                    <div class='notif-msg'>{row['message']}</div>
                    <div class='notif-time'>{row['time']} &nbsp;
                        <span class='badge badge-blue'>📧 Email</span> &nbsp;
                        <span class='badge badge-green'>💬 WhatsApp</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Upcoming Registered Events Table ──
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
    st.markdown("""
    <div class='section-title'>Browse Events</div>
    <div class='section-sub'>Discover and register for upcoming campus events.</div>
    """, unsafe_allow_html=True)

    # AI Banner
    st.markdown("""
    <div class='ai-banner'>
        <div style='font-size:1.4rem;'>✨</div>
        <div>
            <div style='font-weight:700; color:#06b6d4; font-size:0.88rem;'>
                AI Recommendations Active
            </div>
            <div style='font-size:0.78rem; color:#64748b;'>
                Events marked ✨ match your interest tags.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Search and Filters
    col_search, col_filter = st.columns([2, 1])
    with col_search:
        search = st.text_input("🔍 Search events", placeholder="Search by name or category...")
    with col_filter:
        categories = ["All"] + list(events_df["category"].unique())
        selected_cat = st.selectbox("Filter by Category", categories)

    # Filter data
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

    # Display events in 2 columns
    cols = st.columns(2)
    for idx, (_, row) in enumerate(filtered.iterrows()):
        pct        = int((row["registered"] / row["capacity"]) * 100)
        is_reg     = row["id"] in st.session_state.registered_ids
        is_rec     = row["category"] in st.session_state.student_interests
        is_full    = row["registered"] >= row["capacity"]

        with cols[idx % 2]:
            rec_label = "✨ For You" if is_rec else ""
            st.markdown(f"""
            <div class='event-card'>
                <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                    <div>
                        {tag_html(row['category'])}
                        {'<span style="color:#06b6d4; font-size:0.72rem; font-weight:600; margin-left:6px;">' + rec_label + '</span>' if rec_label else ''}
                    </div>
                    <div style='font-size:1.8rem;'>{row['emoji']}</div>
                </div>
                <div class='event-title'>{row['title']}</div>
                <div class='event-meta'>📅 {row['date']} · {row['time']}</div>
                <div class='event-meta'>📍 {row['venue']}</div>
                <div class='event-meta'>👤 {row['organizer']}</div>
                <div style='font-size:0.8rem; color:#64748b; margin:8px 0;'>{row['description'][:80]}...</div>
                {seats_bar(row['registered'], row['capacity'])}
            </div>
            """, unsafe_allow_html=True)

            # Register button
            if is_reg:
                st.success("✓ Already Registered")
            elif is_full:
                st.error("Event Full")
            else:
                if st.button(
                    f"Register for {row['title'][:20]}...",
                    key=f"reg_{row['id']}",
                    use_container_width=True,
                    type="primary"
                ):
                    st.session_state.registered_ids.append(row["id"])
                    st.success(f"✅ Registered for {row['title']}! Confirmation sent via Email & WhatsApp.")
                    st.rerun()


# ══════════════════════════════════════════════════════════════
# PAGE 3 — MY REGISTRATIONS
# ══════════════════════════════════════════════════════════════
def page_my_registrations():
    st.markdown("""
    <div class='section-title'>My Registrations</div>
    <div class='section-sub'>Track all your event registrations and status.</div>
    """, unsafe_allow_html=True)

    my_events = events_df[events_df["id"].isin(st.session_state.registered_ids)]
    total     = len(my_events)

    # Stats row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class='stat-card'>
            <div style='font-size:1.4rem;'>📋</div>
            <div class='stat-number'>{total}</div>
            <div class='stat-label'>Registered</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='stat-card'>
            <div style='font-size:1.4rem;'>⏳</div>
            <div class='stat-number'>{total}</div>
            <div class='stat-label'>Upcoming</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='stat-card'>
            <div style='font-size:1.4rem;'>✅</div>
            <div class='stat-number'>2</div>
            <div class='stat-label'>Attended</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class='stat-card'>
            <div style='font-size:1.4rem;'>🏆</div>
            <div class='stat-number'>1</div>
            <div class='stat-label'>Prize Won</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Registered events
    st.markdown("#### Active Registrations")
    if len(my_events) == 0:
        st.info("You have not registered for any events yet.")
    else:
        for _, row in my_events.iterrows():
            col_info, col_btn = st.columns([4, 1])
            with col_info:
                pct = int((row["registered"] / row["capacity"]) * 100)
                st.markdown(f"""
                <div class='event-card'>
                    <div style='display:flex; gap:14px; align-items:center;'>
                        <div style='font-size:2rem;'>{row['emoji']}</div>
                        <div style='flex:1;'>
                            {tag_html(row['category'])}
                            <div class='event-title'>{row['title']}</div>
                            <div class='event-meta'>📅 {row['date']} &nbsp;|&nbsp; 📍 {row['venue']}</div>
                        </div>
                        <div>{badge_html('● Registered', 'green')}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                st.markdown("<br><br>", unsafe_allow_html=True)
                if st.button("Cancel", key=f"cancel_{row['id']}", type="secondary"):
                    st.session_state.registered_ids.remove(row["id"])
                    st.warning(f"Registration for {row['title']} cancelled.")
                    st.rerun()

    # Past events
    st.markdown("#### Past Events")
    past_data = {
        "Event": ["⚡ CodeSprint 2024", "💻 HackFest 2024", "🎭 Cultural Night 2024"],
        "Date":  ["Nov 15, 2024",       "Dec 10, 2024",     "Dec 20, 2024"],
        "Result":["2nd Place 🥈",        "Participant 🏅",    "Participant 🏅"],
        "Status":["Completed",           "Completed",         "Completed"],
    }
    st.dataframe(pd.DataFrame(past_data), use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# PAGE 4 — MY CERTIFICATES
# ══════════════════════════════════════════════════════════════
def page_certificates():
    st.markdown("""
    <div class='section-title'>My Certificates</div>
    <div class='section-sub'>Download your participation and achievement certificates.</div>
    """, unsafe_allow_html=True)

    prize_emojis = {
        "1st Place": "🥇", "2nd Place": "🥈",
        "3rd Place": "🥉", "Participant": "🏅"
    }

    cols = st.columns(2)
    for idx, (_, row) in enumerate(certificates_df.iterrows()):
        with cols[idx % 2]:
            prize_emoji = prize_emojis.get(row["prize"], "🏅")
            st.markdown(f"""
            <div class='cert-card'>
                <div class='cert-title'>Certificate of Achievement</div>
                <div style='font-size:0.72rem; color:#64748b; letter-spacing:0.15em; margin-top:4px;'>
                    This is to certify that
                </div>
                <div class='cert-name'>{st.session_state.student_name}</div>
                <div class='cert-divider'></div>
                <div style='font-size:0.85rem; color:#64748b;'>has been awarded</div>
                <div class='cert-prize'>{prize_emoji} {row['prize']}</div>
                <div class='cert-event'>{row['event_title']}</div>
                <div style='font-size:0.75rem; color:#64748b; margin-top:10px;'>
                    {row['date']} &nbsp;|&nbsp; Issued: {row['issued_date']}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Download button (generates a text-based certificate)
            cert_text = f"""
CERTIFICATE OF ACHIEVEMENT
===========================
This is to certify that

{st.session_state.student_name}

has been awarded

{row['prize']}

in

{row['event_title']}

Date: {row['date']}
Issued: {row['issued_date']}

- CEMS, College Event Management System
            """.strip()

            st.download_button(
                label=f"⬇ Download Certificate",
                data=cert_text,
                file_name=f"certificate_{row['event_title'].replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
                key=f"dl_cert_{idx}"
            )
            st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 5 — NOTIFICATIONS
# ══════════════════════════════════════════════════════════════
def page_notifications():
    st.markdown("""
    <div class='section-title'>Notifications</div>
    <div class='section-sub'>Your complete Email & WhatsApp notification history.</div>
    """, unsafe_allow_html=True)

    dot_colors = {
        "info":    "#3b82f6",
        "success": "#10b981",
        "warning": "#f59e0b",
        "error":   "#ef4444"
    }

    # Filter
    filter_type = st.selectbox(
        "Filter",
        ["All", "Registration", "Reminder", "Result", "Certificate"],
        label_visibility="collapsed"
    )

    filtered_notifs = notifications_df.copy()
    if filter_type != "All":
        filtered_notifs = filtered_notifs[
            filtered_notifs["trigger"].str.contains(filter_type, case=False)
        ]

    st.markdown(f"**{len(filtered_notifs)} notifications**")
    st.markdown("<br>", unsafe_allow_html=True)

    for _, row in filtered_notifs.iterrows():
        dot = dot_colors.get(row["type"], "#64748b")
        email_badge    = badge_html("📧 Email", "blue")    if row["email_sent"]    == "Yes" else ""
        whatsapp_badge = badge_html("💬 WhatsApp", "green") if row["whatsapp_sent"] == "Yes" else ""
        st.markdown(f"""
        <div class='notif-item'>
            <div class='notif-dot' style='background:{dot}; width:12px; height:12px;'></div>
            <div style='flex:1;'>
                <div class='notif-msg'>{row['message']}</div>
                <div class='notif-time' style='margin-top:6px;'>
                    {row['time']} &nbsp; {email_badge} &nbsp; {whatsapp_badge}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 6 — PROFILE
# ══════════════════════════════════════════════════════════════
def page_profile():
    st.markdown("""
    <div class='section-title'>My Profile</div>
    <div class='section-sub'>Manage your account and AI interest preferences.</div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("#### 👤 Personal Information")
        name  = st.text_input("Full Name",  value=st.session_state.student_name)
        email = st.text_input("Email",      value="student@college.edu")
        phone = st.text_input("Phone (WhatsApp)", value="+91 98765 43210")
        dept  = st.text_input("Department", value="Computer Science")
        year  = st.selectbox("Year", ["1st Year","2nd Year","3rd Year","4th Year"], index=2)

        if st.button("💾 Save Profile", use_container_width=True, type="primary"):
            st.session_state.student_name = name
            st.success("✅ Profile updated successfully!")

    with col_right:
        st.markdown("#### 🤖 AI Interest Tags")
        st.markdown(
            "<div style='font-size:0.85rem; color:#64748b; margin-bottom:12px;'>"
            "Select topics you are interested in. The AI engine will recommend "
            "matching events on your dashboard."
            "</div>",
            unsafe_allow_html=True
        )

        all_interests = ["Tech", "Cultural", "Sports", "Academic", "Arts", "Finance"]
        selected = st.multiselect(
            "Your Interests",
            all_interests,
            default=st.session_state.student_interests,
            label_visibility="collapsed"
        )

        if st.button("🤖 Update AI Preferences", use_container_width=True):
            st.session_state.student_interests = selected
            st.success(f"✅ AI engine updated! Now tracking: {', '.join(selected)}")

        # Show AI status box
        st.markdown(f"""
        <div style='background:#1a2235; border-radius:12px; padding:16px; margin-top:14px;
                    border: 1px solid #1e2d45;'>
            <div style='font-weight:700; color:#06b6d4; margin-bottom:8px; font-size:0.9rem;'>
                🤖 AI Engine Status
            </div>
            <div style='color:#64748b; font-size:0.82rem; margin-bottom:10px;'>
                Active · Matching events to your {len(selected)} selected interests
            </div>
            <div style='display:flex; flex-wrap:wrap; gap:6px;'>
                {"".join([f"<span class='badge badge-blue'>{i}</span>" for i in selected])}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Stats
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("#### 📊 My Stats")
        stats_data = {
            "Metric": [
                "Events Registered",
                "Events Attended",
                "Certificates Earned",
                "Prizes Won",
                "Notifications Received"
            ],
            "Count": [
                len(st.session_state.registered_ids),
                2, 3, 1,
                len(notifications_df)
            ]
        }
        st.dataframe(
            pd.DataFrame(stats_data),
            use_container_width=True,
            hide_index=True
        )


# ══════════════════════════════════════════════════════════════
# MAIN APP ROUTER
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
