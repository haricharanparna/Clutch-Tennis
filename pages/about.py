import streamlit as st

st.set_page_config(
    page_title="Clutch Tennis | About",
    page_icon="🎾",
    layout="wide"
)

# -----------------------------
# LOGIN PROTECTION
# -----------------------------
if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")

# -----------------------------
# CSS
# -----------------------------
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

.page-hero {
    background: linear-gradient(
        135deg,
        #082D22,
        #0B3D2E
    );
    border-radius: 26px;
    padding: 50px;
    color: white;
    margin-bottom: 45px;
}

.kicker {
    color: #C9E86A;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.75rem;
    font-weight: 800;
}

.page-title {
    font-size: 3rem;
    font-weight: 800;
    margin-top: 10px;
}

.page-subtitle {
    font-size: 1.05rem;
    opacity: 0.82;
    max-width: 650px;
    line-height: 1.7;
}

.section-title {
    color: #0B3D2E;
    font-size: 1.8rem;
    font-weight: 800;
    margin: 35px 0 15px;
}

.info-card {
    background: white;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 30px;
    height: 100%;
    box-shadow: 0 8px 25px rgba(23,32,28,0.04);
}

.info-card h3 {
    color: #0B3D2E;
    margin-bottom: 10px;
}

.info-card p {
    color: #66706B;
    line-height: 1.7;
}

/* Centered Header with Green Side Accents */
.coaches-header-container {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 50px 0 30px 0;
}

.coaches-header-line {
    flex: 1;
    height: 3px;
    background-color: #2E7D32;
    max-width: 200px;
}

.coaches-header-title {
    color: #1E40AF;
    font-size: 2.2rem;
    font-weight: 800;
    text-transform: uppercase;
    margin: 0 20px;
    letter-spacing: 1px;
}

/* Redesigned Coach Cards */
.coach-card-redesign {
    background: white;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 30px 20px 20px 20px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(23,32,28,0.04);
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 15px;
}

.coach-avatar-container {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    background-color: #A7F3D0;
    border: 4px solid #86EFAC;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    margin-bottom: 20px;
}

.coach-avatar-container img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.avatar-placeholder-text {
    font-size: 0.75rem;
    color: #065F46;
    font-weight: 600;
    text-align: center;
    padding: 10px;
}

.coach-name-title {
    color: #1E293B;
    font-size: 1.15rem;
    font-weight: 800;
    text-transform: uppercase;
    margin-bottom: 5px;
}

.coach-divider-sm {
    width: 30px;
    height: 3px;
    background-color: #86EFAC;
    margin: 6px auto 12px auto;
}

.coach-role-text {
    color: #64748B;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    min-height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* GLOBAL PAGE BUTTONS */
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

# -----------------------------
# UNIFIED NAVBAR
# -----------------------------
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
        st.switch_page("app.py")

with nav_col4:
    st.markdown('<div class="nav-link-btn-marker"></div>', unsafe_allow_html=True)
    if st.button("About Us", key="nav_about"):
        st.rerun()

with nav_col5:
    st.markdown('<div class="nav-link-btn-marker"></div>', unsafe_allow_html=True)
    if st.button("FAQ", key="nav_faq"):
        st.switch_page("pages/faq.py")

with nav_col6:
    st.markdown('<div class="nav-link-btn-marker"></div>', unsafe_allow_html=True)
    if st.button("Contact", key="nav_contact"):
        st.switch_page("app.py")

with nav_col7:
    st.markdown('<div class="nav-cta-marker"></div>', unsafe_allow_html=True)
    if st.button("Book a Free Trial", key="nav_cta_btn", use_container_width=True):
        st.switch_page("pages/booking.py")

# -----------------------------
# HERO
# -----------------------------
st.markdown("""
<div class="page-hero">
    <div class="kicker">About Clutch Tennis</div>
    <div class="page-title">
        More than tennis.
    </div>
    <div class="page-subtitle">
        We help players develop the skills, confidence, and mindset
        needed to compete at their best.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# STORY
# -----------------------------
st.markdown(
    '<div class="section-title">Our Approach</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="info-card">
    <h3>🎾 Skill</h3>
    <p>
        Build strong fundamentals and develop the technical
        skills needed to become a better tennis player.
    </p>
</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="info-card">
    <h3>🧠 Mindset</h3>
    <p>
        Develop confidence, focus, and mental toughness for
        challenging moments on the court.
    </p>
</div>
""", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("""
<div class="info-card">
    <h3>🏆 Competition</h3>
    <p>
        Practice strategies and match situations that prepare
        players for competitive tennis.
    </p>
</div>
""", unsafe_allow_html=True)

with col4:
    st.markdown("""
<div class="info-card">
    <h3>💪 Confidence</h3>
    <p>
        Learn to trust your preparation and your abilities
        when matches become challenging.
    </p>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# MEET THE COACHES
# -----------------------------
st.markdown("""
<div class="coaches-header-container">
    <div class="coaches-header-line"></div>
    <div class="coaches-header-title">Our Coaches and Staff</div>
    <div class="coaches-header-line"></div>
</div>
""", unsafe_allow_html=True)

coaches = [
    {
        "name": "Hari Parna",
        "role": "Founder and CEO",
        "image_url": None,
        "key": "hari"
    },
    {
        "name": "Mayur Parna",
        "role": "Co-Founder and CTO",
        "image_url": None,
        "key": "mayur"
    },
    {
        "name": "Curious George",
        "role": "Mascot",
        "image_url": None,
        "key": "george"
    }
]

coach_cols = st.columns(len(coaches))

for col, coach in zip(coach_cols, coaches):
    with col:
        if coach["image_url"]:
            image_content = f'<img src="{coach["image_url"]}" alt="{coach["name"]}" />'
        else:
            image_content = '<div class="avatar-placeholder-text">ADD IMAGE HERE</div>'

        st.markdown(f"""
<div class="coach-card-redesign">
    <div class="coach-avatar-container">
        {image_content}
    </div>
    <div class="coach-name-title">{coach['name']}</div>
    <div class="coach-divider-sm"></div>
    <div class="coach-role-text">{coach['role']}</div>
</div>
""", unsafe_allow_html=True)

        if st.button("VIEW PROFILE", key=f"btn_{coach['key']}", use_container_width=True):
            st.info(f"Opening profile for {coach['name']}...")

# -----------------------------
# WHY CLUTCH
# -----------------------------
st.markdown(
    '<div class="section-title">Why Clutch Tennis?</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-card">
<p>🎯 <strong>Personalized Training</strong><br>
Training is built around each player's individual goals.</p>
<p>💪 <strong>Confidence</strong><br>
Develop the confidence to trust your skills during matches.</p>
<p>🧠 <strong>Mental Toughness</strong><br>
Stay focused and composed in competitive situations.</p>
<p>🏆 <strong>Match Preparation</strong><br>
Practice strategies that translate directly to competitive tennis.</p>
</div>
""", unsafe_allow_html=True)

st.write("")

if st.button("Book a Lesson →", use_container_width=True):
    st.switch_page("pages/booking.py")
