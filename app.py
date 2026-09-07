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
# SUPABASE SETUP
# -----------------------------
supabase = create_client(
    st.secrets.get("SUPABASE_URL", ""),
    st.secrets.get("SUPABASE_KEY", "")
)

user = st.session_state.get("user")
full_name = "Player"

if user and hasattr(user, "user_metadata"):
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
    padding-top: 1rem;
    padding-bottom: 0rem;
}

#MainMenu, footer {
    visibility: hidden;
}

/* REMOVE OVERFLOW CONSTRAINTS FOR STICKY NAVBAR */
[data-testid="stAppViewContainer"] > .main {
    overflow: visible !important;
}

div[data-testid="stVerticalBlock"] {
    overflow: visible !important;
}

/* FLOATING NAVBAR CONTAINER */
.floating-navbar {
    position: -webkit-sticky !important;
    position: sticky !important;
    top: 10px !important;
    z-index: 99999 !important;
    background-color: #FFFFFF;
    border-radius: 40px;
    padding: 12px 30px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    margin-bottom: 30px;
    border: 1px solid #EFEFEF;
}

.nav-logo {
    display: flex;
    align-items: center;
    font-weight: 800;
    font-size: 1.3rem;
    color: #0B3D2E;
    text-decoration: none;
    letter-spacing: -0.5px;
}

.nav-logo span {
    color: #88C425;
    margin-left: 4px;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: 24px;
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav-item {
    color: #0B3D2E;
    font-weight: 600;
    font-size: 0.95rem;
    text-decoration: none;
    padding-bottom: 4px;
    transition: all 0.2s ease;
}

.nav-item.active {
    border-bottom: 3px solid #88C425;
}

.nav-item:hover {
    color: #88C425;
}

.nav-cta-btn {
    background-color: #0B3D2E;
    color: #FFFFFF !important;
    padding: 10px 22px;
    border-radius: 20px;
    font-weight: 700;
    font-size: 0.9rem;
    text-decoration: none;
    transition: background-color 0.2s ease;
}

.nav-cta-btn:hover {
    background-color: #145A43;
}

/* HERO */
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

/* SECTION HEADINGS */
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

/* SERVICE CARDS */
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

/* REVIEWS CAROUSEL */
.carousel-container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    padding: 10px 0px 20px 0px;
}

.review-card-slide {
    background: white;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 25px;
    box-shadow: 0 8px 25px rgba(23,32,28,0.04);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.review-stars {
    color: #F59E0B;
    font-size: 1rem;
    margin-bottom: 10px;
}

.review-text {
    color: #59635E;
    font-size: 0.95rem;
    line-height: 1.6;
    font-style: italic;
    margin-bottom: 15px;
}

.review-author {
    color: #0B3D2E;
    font-weight: 800;
    font-size: 0.9rem;
}

.review-role {
    color: #7A837F;
    font-size: 0.8rem;
}

/* BUTTON STYLES */
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

.dot-btn-container div.stButton > button {
    min-height: 24px !important;
    height: 24px !important;
    max-width: 24px !important;
    padding: 0 !important;
    font-size: 0.65rem !important;
    line-height: 1 !important;
    border-radius: 50% !important;
    background: #E4E9E4 !important;
    color: #0B3D2E !important;
    border: none !important;
    margin: 0 auto !important;
}

.dot-btn-container div.stButton > button:hover {
    background: #0B3D2E !important;
    color: white !important;
}

/* CTA */
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

/* FOOTER STYLING */
.footer-wrapper {
    background: linear-gradient(135deg, #082D22 0%, #0B3D2E 50%, #145A43 100%);
    color: #FFFFFF;
    border-radius: 24px 24px 0 0;
    padding: 50px 40px 30px 40px;
    margin-top: 50px;
    display: block !important;
    visibility: visible !important;
}

.footer-grid {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 30px;
    margin-bottom: 40px;
}

.footer-brand {
    font-size: 1.4rem;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 12px;
}

.footer-brand span {
    color: #C9E86A;
}

.footer-tagline {
    font-size: 0.95rem;
    color: rgba(255, 255, 255, 0.75);
    margin-bottom: 20px;
    max-width: 280px;
    line-height: 1.5;
}

.footer-contact-item {
    font-size: 0.9rem;
    color: #C9E86A;
    margin-bottom: 6px;
    font-weight: 600;
}

.footer-col-title {
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #C9E86A;
    margin-bottom: 18px;
}

.footer-links {
    list-style: none;
    padding: 0;
    margin: 0;
}

.footer-links li {
    margin-bottom: 10px;
}

.footer-links a {
    color: rgba(255, 255, 255, 0.8);
    text-decoration: none;
    font-size: 0.9rem;
    transition: color 0.2s ease;
}

.footer-links a:hover {
    color: #FFFFFF;
}

.social-icons {
    display: flex;
    gap: 12px;
}

.social-icon {
    width: 38px;
    height: 38px;
    background: rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #FFFFFF;
    text-decoration: none;
    font-weight: 700;
    font-size: 0.9rem;
    transition: background 0.2s ease;
}

.social-icon:hover {
    background: #C9E86A;
    color: #082D22;
}

.footer-bottom {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 20px;
    text-align: center;
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.5);
}

/* INFO CARDS */
.info-card {
    background: white;
    border: 1px solid #E4E9E4;
    border-radius: 18px;
    padding: 22px;
    box-shadow: 0 6px 20px rgba(23,32,28,0.03);
    margin-bottom: 15px;
}

.event-date-badge {
    background: #EEF5D9;
    color: #0B3D2E;
    font-weight: 800;
    font-size: 0.75rem;
    padding: 4px 10px;
    border-radius: 8px;
    display: inline-block;
    margin-bottom: 8px;
    text-transform: uppercase;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# FLOATING NAVBAR
# -----------------------------
st.markdown("""
<div class="floating-navbar">
    <div class="nav-logo">
        🎾 CLUTCH<span>TENNIS</span>
    </div>
    <div class="nav-links">
        <a href="#" class="nav-item active">Home</a>
        <a href="#" class="nav-item">Location</a>
        <a href="#" class="nav-item">About Us</a>
        <a href="#" class="nav-item">FAQ</a>
        <a href="#" class="nav-item">Contact</a>
        <a href="#" class="nav-cta-btn">Book a Free Trial</a>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------
# HERO SECTION
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
# DATA LOAD WITH FALLBACK
# -----------------------------
sheet_url = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vSgtx-vuVX2vg5vG-NfSGzB9LyzYXFwQ6or-y0GjdpAWwYCwvh89ueQStE8OYVcbaGgoFsH0IISrNr-/"
    "pub?output=csv"
)

cache_bust_url = f"{sheet_url}&cachebust={pd.Timestamp.now().timestamp()}"

try:
    df = pd.read_csv(cache_bust_url)
    df.columns = df.columns.str.strip()
except Exception:
    # Fallback default data if sheet fetch fails
    df = pd.DataFrame([
        {"Service": "Private Coaching", "Description": "1-on-1 personalized instruction tailored to technical and tactical goals.", "Price": "$80 / hr"},
        {"Service": "Group Clinics", "Description": "Dynamic drills, high reps, and competitive point play in small groups.", "Price": "$40 / hr"},
        {"Service": "Mental Edge", "Description": "Strategy and mindset coaching to help you win critical pressure points.", "Price": "$60 / hr"},
        {"Service": "Tournament Prep", "Description": "Simulated match play and tactical analysis for competitive players.", "Price": "$90 / hr"}
    ])


# -----------------------------
# SERVICE CARDS
# -----------------------------
icons = ["🎾", "👥", "🧠", "🏆"]

if not df.empty:
    service_columns = st.columns(min(len(df), 4))

    for index, (_, row) in enumerate(df.iterrows()):
        col_idx = index % 4
        with service_columns[col_idx]:
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
# LOCATIONS & EVENTS SECTION
# -----------------------------
loc_col, event_col = st.columns(2)

with loc_col:
    st.markdown("""
    <div class="section-header">
        <div class="section-kicker">Coaching Location</div>
        <div class="section-title">Location Details</div>
    </div>
    <div class="info-card">
        <p style="font-size: 1.1rem; font-weight: 700; color: #0B3D2E; margin-bottom: 8px;">📍 Coppermill Tennis Court</p>
        <p style="color: #59635E; margin-bottom: 12px;">13287 Coppermill Dr, Herndon, VA 20171</p>
        <p style="font-size: 0.9rem; color: #69736E; margin: 0;">🎾 Summer, Fall, and Spring Training</p>
    </div>
    """, unsafe_allow_html=True)

with event_col:
    st.markdown("""
    <div class="section-header">
        <div class="section-kicker">Schedule</div>
        <div class="section-title">Upcoming Events</div>
    </div>
    <div class="info-card">
        <span class="event-date-badge">September 19</span>
        <p style="font-weight: 700; color: #17201C; margin: 4px 0;">Full Day Introductory Lessons | Herndon VA</p>
        <a href="#" style="color: #2B6CB0; font-weight: 600; font-size: 0.85rem; text-decoration: none;">View details →</a>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------
# REVIEWS DATA
# -----------------------------
reviews = [
    {"stars": "⭐⭐⭐⭐☆", "text": "Coach Hari completely transformed my serve in just three sessions. The tactical focus here is top-tier.", "author": "John M.", "role": "Advanced Player"},
    {"stars": "⭐⭐⭐⭐☆", "text": "The mental toughness training helped me stay calm during tiebreakers. Highly recommend Clutch Tennis!", "author": "Sarah K.", "role": "Competitive Junior"},
    {"stars": "⭐⭐⭐⭐⭐", "text": "Great energy in the group clinics. Excellent balance of skill drills and live match strategy.", "author": "David L.", "role": "Adult Clinic Member"},
    {"stars": "⭐⭐⭐⭐⭐", "text": "Footwork drills with Coach George made a massive difference in my court coverage and endurance.", "author": "Jason T.", "role": "Varsity Player"},
    {"stars": "⭐⭐⭐⭐⭐", "text": "The match analysis feedback was eye-opening. I completely changed how I construct points on key rallies.", "author": "Elena R.", "role": "USTA League Player"},
    {"stars": "⭐⭐⭐⭐⭐", "text": "Best coaching staff in the area! They break down technical flaws in a way that is super easy to understand.", "author": "Marcus B.", "role": "Intermediate Player"},
    {"stars": "⭐⭐⭐⭐⭐", "text": "My son’s confidence on the court skyrocketed after just a month of private lessons. Fantastic mentors.", "author": "Karen W.", "role": "Tennis Parent"},
    {"stars": "⭐⭐⭐⭐⭐", "text": "The small group size in the clinics ensures everyone gets personalized attention and high-volume reps.", "author": "Chris P.", "role": "Adult Beginner"},
    {"stars": "⭐⭐⭐⭐☆", "text": "Coach Mayur's focus on net play and doubles strategy gave our team the edge to win our local flight.", "author": "Rachel S.", "role": "Doubles Captain"},
    {"stars": "⭐⭐⭐⭐⭐", "text": "Top-notch facility and incredibly structured sessions. Every minute on court feels intentional.", "author": "Daniel H.", "role": "Competitive Junior"},
    {"stars": "⭐⭐⭐⭐⭐", "text": "I went from second-guessing my groundstrokes to playing aggressive, winning tennis in big moments.", "author": "Megan C.", "role": "High School Player"},
    {"stars": "⭐⭐⭐⭐⭐", "text": "The mental game coaching is what sets Clutch apart from every other academy. Total game changer.", "author": "Brian F.", "role": "Tournament Player"},
    {"stars": "⭐⭐⭐⭐☆", "text": "Awesome coaches who truly care about your long-term growth rather than quick, band-aid fixes.", "author": "Jessica V.", "role": "Adult Clinic Member"},
    {"stars": "⭐⭐⭐⭐⭐", "text": "Rebuilt my backhand technique from scratch. I'm finally hitting with depth and heavy topspin.", "author": "Tom E.", "role": "Intermediate Player"},
    {"stars": "⭐⭐⭐⭐⭐", "text": "Friendly environment, professional coaches, and noticeable results after every single session.", "author": "Olivia G.", "role": "Junior Player"}
]


# -----------------------------
# REVIEWS SECTION
# -----------------------------
st.markdown(
    """
<div class="section-header">
    <div class="section-kicker">Testimonials</div>
    <div class="section-title">What Players Say</div>
</div>
""",
    unsafe_allow_html=True
)

if "review_page" not in st.session_state:
    st.session_state.review_page = 0

items_per_page = 3
total_pages = (len(reviews) + items_per_page - 1) // items_per_page

start_idx = st.session_state.review_page * items_per_page
current_reviews = reviews[start_idx:start_idx + items_per_page]

card_items = []
for rev in current_reviews:
    card_html = (
        f'<div class="review-card-slide">'
        f'<div>'
        f'<div class="review-stars">{rev["stars"]}</div>'
        f'<div class="review-text">"{rev["text"]}"</div>'
        f'</div>'
        f'<div>'
        f'<div class="review-author">{rev["author"]}</div>'
        f'<div class="review-role">{rev["role"]}</div>'
        f'</div>'
        f'</div>'
    )
    card_items.append(card_html)

carousel_html = f'<div class="carousel-container">{"".join(card_items)}</div>'
st.markdown(carousel_html, unsafe_allow_html=True)

# Pagination Controls
st.markdown('<div class="dot-btn-container">', unsafe_allow_html=True)
nav_spacer_left, nav_center, nav_spacer_right = st.columns([3, 1, 3])

with nav_center:
    dot_cols = st.columns(total_pages)
    for page_num in range(total_pages):
        with dot_cols[page_num]:
            dot_symbol = "●" if page_num == st.session_state.review_page else "○"
            if st.button(dot_symbol, key=f"dot_page_{page_num}", use_container_width=True):
                st.session_state.review_page = page_num
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# BOOKING SECTION
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
# LOGOUT BUTTON
# -----------------------------
st.divider()

if st.button("Log Out", use_container_width=True):
    st.session_state["logged_in"] = False
    st.session_state["user"] = None
    st.switch_page("pages/login.py")


# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<div class="footer-wrapper">
    <div class="footer-grid">
        <div>
            <div class="footer-brand">🎾 CLUTCH<span>TENNIS</span></div>
            <div class="footer-tagline">
                Perfect Tennis Academy to get to the Next Level
            </div>
            <div class="footer-contact-item">✉️ haricharanparna@gmail.com</div>
            <div class="footer-contact-item">📞 (703) 962 0621</div>
        </div>
        <div>
            <div class="footer-col-title">About Us</div>
            <ul class="footer-links">
                <li><a href="#">Our Coaches</a></li>
                <li><a href="#">Our Locations</a></li>
                <li><a href="#">Our Story</a></li>
            </ul>
        </div>
        <div>
            <div class="footer-col-title">Resources</div>
            <ul class="footer-links">
                <li><a href="#">FAQs</a></li>
                <li><a href="#">Contact Us</a></li>
            </ul>
        </div>
        <div>
            <div class="footer-col-title">Follow Us</div>
            <div class="social-icons">
                <a href="#" class="social-icon">G</a>
                <a href="#" class="social-icon">YT</a>
                <a href="#" class="social-icon">IN</a>
            </div>
        </div>
    </div>
    <div class="footer-bottom">
        © 2026 Clutch Tennis. All rights reserved.
    </div>
</div>
""", unsafe_allow_html=True)
