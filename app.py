import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(
    page_title="Clutch Tennis",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# LOGIN PROTECTION
# -----------------------------
if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")

# -----------------------------
# SUPABASE
# -----------------------------
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

user = st.session_state.get("user")

full_name = "Player"

if user:
    full_name = user.user_metadata.get("full_name", "Player")

# -----------------------------
# GLOBAL CSS
# -----------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            circle at 90% 5%,
            rgba(11,61,46,0.08),
            transparent 25%
        ),
        #F7F8F5;
    color: #17201C;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Hide default menu/footer */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* -----------------------------
   HERO
----------------------------- */

.hero {
    background: linear-gradient(
        135deg,
        #082D22 0%,
        #0B3D2E 55%,
        #145A43 100%
    );
    border-radius: 28px;
    padding: 65px 60px;
    color: white;
    position: relative;
    overflow: hidden;
    margin-bottom: 35px;
    box-shadow: 0 20px 50px rgba(11,61,46,0.18);
}

.hero:after {
    content: "🎾";
    position: absolute;
    right: 50px;
    top: 15px;
    font-size: 170px;
    opacity: 0.09;
    transform: rotate(15deg);
}

.hero-eyebrow {
    text-transform: uppercase;
    letter-spacing: 3px;
    font-size: 0.78rem;
    font-weight: 700;
    opacity: 0.75;
    margin-bottom: 15px;
}

.hero-title {
    font-size: 4rem;
    line-height: 1.02;
    font-weight: 800;
    margin: 0;
    max-width: 700px;
}

.hero-title span {
    color: #C9E86A;
}

.hero-text {
    font-size: 1.08rem;
    line-height: 1.7;
    max-width: 620px;
    margin-top: 22px;
    opacity: 0.88;
}

.welcome-pill {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.16);
    padding: 8px 15px;
    border-radius: 50px;
    font-size: 0.85rem;
    margin-bottom: 20px;
}

/* -----------------------------
   SECTION HEADINGS
----------------------------- */

.section-header {
    margin-top: 45px;
    margin-bottom: 20px;
}

.section-kicker {
    color: #0B3D2E;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.72rem;
    font-weight: 800;
}

.section-title {
    font-size: 2rem;
    font-weight: 800;
    margin-top: 4px;
    color: #17201C;
}

/* -----------------------------
   SERVICE CARDS
----------------------------- */

.service-card {
    background: white;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 28px;
    min-height: 290px;
    display: flex;
    flex-direction: column;
    transition: 0.2s ease;
    box-shadow: 0 8px 25px rgba(23,32,28,0.04);
}

.service-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 35px rgba(23,32,28,0.08);
    border-color: #C9E86A;
}

.service-icon {
    width: 48px;
    height: 48px;
    background: #EEF5D9;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    margin-bottom: 22px;
}

.service-name {
    color: #0B3D2E;
    font-size: 1.25rem;
    font-weight: 800;
}

.service-description {
    color: #66706B;
    line-height: 1.6;
    margin-top: 10px;
    flex-grow: 1;
}

.service-price {
    color: #17201C;
    font-size: 1rem;
    font-weight: 700;
    margin-top: 20px;
}

/* -----------------------------
   BUTTONS
----------------------------- */

div.stButton > button {
    background: #0B3D2E;
    color: white;
    border: 0;
    border-radius: 12px;
    min-height: 48px;
    font-weight: 700;
    transition: 0.2s ease;
}

div.stButton > button:hover {
    background: #145A43;
    border: 0;
    color: white;
    transform: translateY(-1px);
}

/* -----------------------------
   CTA
----------------------------- */

.cta {
    background: #EAF2D5;
    border: 1px solid #D9E7B9;
    border-radius: 22px;
    padding: 35px;
    margin-top: 50px;
}

.cta h2 {
    color: #0B3D2E;
    margin-bottom: 8px;
}

.small-note {
    color: #69736E;
    font-size: 0.9rem;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# HERO
# -----------------------------

st.markdown(
    f"""
<div class="hero">
    <div class="welcome-pill">
        Welcome back, {full_name} 👋
    </div>
    <div class="hero-eyebrow">
        Clutch Tennis Academy
    </div>
    <div class="hero-title">
        Train Hard.<br>
        <span>Play Clutch.</span>
    </div>
    <div class="hero-text">
        Personalized tennis coaching designed to sharpen your skills,
        build confidence, and help you perform when it matters most.
    </div>
</div>
""",
    unsafe_allow_html=True
)


# -----------------------------
# SERVICES HEADER
# -----------------------------

st.markdown(
    """
<div class="section-header">
    <div class="section-kicker">What We Offer</div>
    <div class="section-title">Train for your game.</div>
</div>
""",
    unsafe_allow_html=True
)


# -----------------------------
# GOOGLE SHEETS
# -----------------------------

sheet_url = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vSgtx-vuVX2vg5vG-NfSGzB9LyzYXFwQ6or-y0GjdpAWwYCwvh89ueQStE8OYVcbaGgoFsH0IISrNr-/"
    "pub?output=csv"
)

cache_bust_url = (
    sheet_url
    + "&cachebust="
    + str(pd.Timestamp.now().timestamp())
)

try:
    df = pd.read_csv(cache_bust_url)
    df.columns = df.columns.str.strip()

except Exception:
    df = pd.DataFrame()


# -----------------------------
# SERVICE CARDS
# -----------------------------

icons = ["🎾", "👥", "🧠", "🏆"]

if not df.empty:

    service_columns = st.columns(len(df))

    for index, (_, row) in enumerate(df.iterrows()):

        with service_columns[index]:

            icon = icons[index] if index < len(icons) else "🎾"

            service_name = str(row.get("Service", "Tennis Coaching"))
            description = str(row.get("Description", ""))
            price = str(row.get("Price", ""))

            st.markdown(
                f"""
<div class="service-card">
    <div class="service-icon">
        {icon}
    </div>
    <div class="service-name">
        {service_name}
    </div>
    <div class="service-description">
        {description}
    </div>
    <div class="service-price">
        {price}
    </div>
</div>
""",
                unsafe_allow_html=True
            )


# -----------------------------
# BOOKING HEADER
# -----------------------------

st.markdown(
    """
<div class="section-header">
    <div class="section-kicker">Start Training</div>
    <div class="section-title">Ready to get better?</div>
</div>
""",
    unsafe_allow_html=True
)


# -----------------------------
# BOOKING BUTTONS
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

buttons = [
    ("Private Coaching", col1),
    ("Group Coaching", col2),
    ("Mental Toughness", col3),
    ("Match Strategy", col4)
]

for label, column in buttons:

    with column:

        if st.button(
            f"Book {label} →",
            use_container_width=True,
            key=f"book_{label}"
        ):
            st.switch_page("pages/booking.py")


# -----------------------------
# CTA
# -----------------------------

st.markdown(
    """
<div class="cta">
    <h2>Your next level starts here. 🎾</h2>
    <div class="small-note">
        Train with purpose. Build confidence. Compete with confidence.
    </div>
</div>
""",
    unsafe_allow_html=True
)


# -----------------------------
# DIVIDER
# -----------------------------

st.divider()


# -----------------------------
# LOGOUT
# -----------------------------

if st.button(
    "Log Out",
    use_container_width=True
):

    st.session_state["logged_in"] = False
    st.session_state["user"] = None

    st.switch_page("pages/login.py")
