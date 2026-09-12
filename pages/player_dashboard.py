import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Player Dashboard | Clutch Tennis",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# LOGIN PROTECTION
# ============================================================

if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")

# ============================================================
# CURRENT USER
# ============================================================

user = st.session_state.get("user")
full_name = "Player"

if user and hasattr(user, "user_metadata"):
    full_name = user.user_metadata.get("full_name", "Player")

# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: #F7F8F5;
    color: #17201C;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1150px;
    padding-top: 1rem;
    padding-bottom: 4rem;
}

#MainMenu, footer {
    visibility: hidden;
}

/* FLOATING NAVBAR CONTAINER */
[data-testid="stHorizontalBlock"]:has(div.nav-logo-target) {
    background-color: #FFFFFF;
    border-radius: 40px;
    padding: 8px 16px 8px 30px;
    align-items: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    border: 1px solid #EFEFEF;
    margin-bottom: 30px;
}

.nav-logo-target {
    font-weight: 800;
    font-size: 1.3rem;
    color: #0B3D2E;
    letter-spacing: -0.5px;
    display: flex;
    align-items: center;
    white-space: nowrap;
}

.nav-logo-target span {
    color: #88C425;
    margin-left: 4px;
}

/* NAVBAR LINK BUTTONS */
div[data-testid="stColumn"]:has(div.nav-link-btn-marker) div.stButton > button {
    background: transparent !important;
    color: #3B82F6 !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border: none !important;
    padding: 0 !important;
    min-height: auto !important;
    box-shadow: none !important;
    text-decoration: underline !important;
}

div[data-testid="stColumn"]:has(div.nav-link-btn-marker) div.stButton > button:hover {
    color: #1D4ED8 !important;
    background: transparent !important;
}

/* NAVBAR CTA BUTTON */
div[data-testid="stColumn"]:has(div.nav-cta-marker) div.stButton > button {
    background-color: #0B3D2E !important;
    color: #FFFFFF !important;
    border-radius: 25px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 8px 20px !important;
    min-height: 42px !important;
    border: none !important;
    width: 100% !important;
}

div[data-testid="stColumn"]:has(div.nav-cta-marker) div.stButton > button:hover {
    background-color: #145A43 !important;
}

/* HERO */
.dashboard-hero {
    background: linear-gradient(
        135deg,
        #082D22 0%,
        #0B3D2E 55%,
        #145A43 100%
    );
    border-radius: 28px;
    padding: 45px 50px;
    color: white;
    position: relative;
    overflow: hidden;
    margin-bottom: 35px;
    box-shadow: 0 20px 50px rgba(11,61,46,0.16);
}

.dashboard-hero:after {
    content: "🎾";
    position: absolute;
    right: 50px;
    top: 15px;
    font-size: 140px;
    opacity: 0.08;
    transform: rotate(15deg);
    pointer-events: none;
}

.hero-small {
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.75rem;
    font-weight: 800;
    opacity: 0.7;
    margin-bottom: 12px;
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    margin: 0;
}

.hero-title span {
    color: #C9E86A;
}

.hero-description {
    margin-top: 12px;
    font-size: 1rem;
    line-height: 1.6;
    opacity: 0.85;
    max-width: 650px;
}

/* SECTION HEADERS */
.section-header {
    margin-top: 35px;
    margin-bottom: 18px;
}

.section-kicker {
    color: #0B3D2E;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.72rem;
    font-weight: 800;
}

.section-title {
    font-size: 1.8rem;
    font-weight: 800;
    margin-top: 4px;
    color: #17201C;
}

/* CARDS */
.dashboard-card {
    background: #FFFFFF;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 25px;
    min-height: 180px;
    box-shadow: 0 8px 25px rgba(23,32,28,0.04);
}

.card-icon {
    width: 45px;
    height: 45px;
    background: #EEF5D9;
    border-radius: 13px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.3rem;
    margin-bottom: 15px;
}

.card-title {
    color: #0B3D2E;
    font-size: 1.1rem;
    font-weight: 800;
    margin-bottom: 8px;
}

.card-text {
    color: #66706B;
    line-height: 1.5;
    font-size: 0.9rem;
}

/* FEEDBACK CARD */
.feedback-card {
    background: #FFFFFF;
    border: 1px solid #E4E9E4;
    border-left: 5px solid #88C425;
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 8px 25px rgba(23,32,28,0.04);
}

.feedback-coach {
    color: #0B3D2E;
    font-weight: 800;
    font-size: 1rem;
}

.feedback-date {
    color: #8A938E;
    font-size: 0.8rem;
    margin-top: 3px;
}

.feedback-text {
    color: #59635E;
    line-height: 1.6;
    margin-top: 15px;
}

/* PROGRESS */
.progress-card {
    background: #FFFFFF;
    border: 1px solid #E4E9E4;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 8px 25px rgba(23,32,28,0.04);
}

.progress-label {
    color: #59635E;
    font-size: 0.9rem;
    margin-bottom: 8px;
}

.progress-value {
    color: #0B3D2E;
    font-size: 1.4rem;
    font-weight: 800;
}

/* GLOBAL PAGE BUTTONS & LOGOUT */
div.stButton > button {
    background: #0B3D2E;
    color: white;
    border: 0;
    border-radius: 12px;
    min-height: 48px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# UNIFIED NAVBAR
# ============================================================

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6, nav_col7 = st.columns([2.5, 0.8, 1.0, 1.1, 0.8, 1.0, 2.2])

with nav_col1:
    st.markdown('<div class="nav-logo-target">🎾 CLUTCH<span>TENNIS</span></div>', unsafe_allow_html=True)

with nav_col2:
    st.markdown('<div class="nav-link-btn-marker"></div>', unsafe_allow_html=True)
    if st.button("Home", key="nav_home"):
        st.switch_page("app.py")

with nav_col3:
    st.markdown('<div class="nav-link-btn-marker"></div>', unsafe_allow_html=True)
    if st.button("Location", key="nav_loc"):
        st.switch_page("pages/location.py")

with nav_col4:
    st.markdown('<div class="nav-link-btn-marker"></div>', unsafe_allow_html=True)
    if st.button("About Us", key="nav_about"):
        st.switch_page("pages/about.py")

with nav_col5:
    st.markdown('<div class="nav-link-btn-marker"></div>', unsafe_allow_html=True)
    if st.button("FAQ", key="nav_faq"):
        st.switch_page("pages/faq.py")

with nav_col6:
    st.markdown('<div class="nav-link-btn-marker"></div>', unsafe_allow_html=True)
    if st.button("Contact", key="nav_contact"):
        st.switch_page("pages/contact.py")

with nav_col7:
    st.markdown('<div class="nav-cta-marker"></div>', unsafe_allow_html=True)
    if st.button("Book a Free Trial", key="nav_cta_btn", use_container_width=True):
        st.switch_page("pages/booking.py")


# ============================================================
# DASHBOARD HERO
# ============================================================

st.markdown(
    f"""
<div class="dashboard-hero">
    <div class="hero-small">
        Player Dashboard
    </div>

    <div class="hero-title">
        Welcome back, <span>{full_name}</span> 👋
    </div>

    <div class="hero-description">
        Track your training, review coach feedback, monitor your progress,
        and stay focused on your next level.
    </div>
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# QUICK OVERVIEW
# ============================================================

st.markdown("""
<div class="section-header">
    <div class="section-kicker">Your Training</div>
    <div class="section-title">Player Overview</div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-icon">🎾</div>
        <div class="card-title">My Coach</div>
        <div class="card-text">
            Your assigned coach will appear here.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-icon">📅</div>
        <div class="card-title">Next Session</div>
        <div class="card-text">
            Your upcoming training session will appear here.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-icon">📈</div>
        <div class="card-title">Progress</div>
        <div class="card-text">
            Track your tennis development over time.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-icon">🏆</div>
        <div class="card-title">Goals</div>
        <div class="card-text">
            Your current training goals will appear here.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# COACH FEEDBACK
# ============================================================

st.markdown("""
<div class="section-header">
    <div class="section-kicker">Coach Communication</div>
    <div class="section-title">Coach Feedback</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="feedback-card">
    <div class="feedback-coach">
        Coach Feedback
    </div>

    <div class="feedback-date">
        No feedback yet
    </div>

    <div class="feedback-text">
        Once your coach submits feedback, it will appear here.
        You'll be able to review notes about your technique,
        strategy, mindset, and areas to improve.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# PROGRESS
# ============================================================

st.markdown("""
<div class="section-header">
    <div class="section-kicker">Development</div>
    <div class="section-title">My Progress</div>
</div>
""", unsafe_allow_html=True)

progress_col1, progress_col2, progress_col3 = st.columns(3)

with progress_col1:
    st.markdown("""
    <div class="progress-card">
        <div class="progress-label">Technical Skills</div>
        <div class="progress-value">Not tracked yet</div>
    </div>
    """, unsafe_allow_html=True)

with progress_col2:
    st.markdown("""
    <div class="progress-card">
        <div class="progress-label">Match Strategy</div>
        <div class="progress-value">Not tracked yet</div>
    </div>
    """, unsafe_allow_html=True)

with progress_col3:
    st.markdown("""
    <div class="progress-card">
        <div class="progress-label">Mental Game</div>
        <div class="progress-value">Not tracked yet</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# GOALS
# ============================================================

st.markdown("""
<div class="section-header">
    <div class="section-kicker">Keep Improving</div>
    <div class="section-title">My Goals</div>
</div>
""", unsafe_allow_html=True)

goal_col1, goal_col2 = st.columns(2)

with goal_col1:
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-icon">🎯</div>
        <div class="card-title">Current Goal</div>
        <div class="card-text">
            Your coach-assigned goals will appear here.
        </div>
    </div>
    """, unsafe_allow_html=True)

with goal_col2:
    st.markdown("""
    <div class="dashboard-card">
        <div class="card-icon">🔥</div>
        <div class="card-title">Training Focus</div>
        <div class="card-text">
            Your current training focus will appear here.
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# LOGOUT
# ============================================================

st.write("")
st.divider()

if st.button("Log Out", key="logout_btn", use_container_width=True):
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    st.switch_page("pages/login.py")
