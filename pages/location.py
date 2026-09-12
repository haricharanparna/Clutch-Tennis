import streamlit as st

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Location | Clutch Tennis",
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
# GLOBAL CSS
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 50% 10%, rgba(11,61,46,0.08), transparent 40%), #F7F8F5;
    color: #17201C;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1150px;
    padding-top: 1rem;
    padding-bottom: 3rem;
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

/* PAGE HERO BANNER */
.location-hero {
    background: linear-gradient(135deg, #082D22 0%, #0B3D2E 55%, #145A43 100%);
    border-radius: 24px;
    padding: 45px 40px;
    color: white;
    margin-bottom: 35px;
    box-shadow: 0 15px 35px rgba(11,61,46,0.15);
}

.location-kicker {
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.8rem;
    font-weight: 700;
    color: #C9E86A;
    margin-bottom: 8px;
}

.location-title {
    font-size: 2.8rem;
    font-weight: 800;
    margin: 0;
}

.location-subtitle {
    font-size: 1rem;
    opacity: 0.85;
    margin-top: 10px;
    max-width: 600px;
}

/* CARD BOXES */
.info-card-box {
    background: #FFFFFF;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 25px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(23,32,28,0.03);
}

.info-card-title {
    font-size: 1.15rem;
    font-weight: 800;
    color: #0B3D2E;
    margin-bottom: 12px;
}

/* LINK CARDS */
.action-link-btn {
    display: block;
    background: #F7F8F5;
    border: 1px solid #E4E9E4;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 10px;
    color: #0B3D2E;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.2s ease;
}

.action-link-btn:hover {
    background: #0B3D2E;
    color: #FFFFFF;
    border-color: #0B3D2E;
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
        st.rerun()

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

# -----------------------------
# HERO HEADER
# -----------------------------
st.markdown("""
<div class="location-hero">
    <div class="location-kicker">Find Us</div>
    <div class="location-title">Our Court Location</div>
    <div class="location-subtitle">
        Join us at our primary outdoor training facilities. Check court details, directions, and navigation links below.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# TWO-COLUMN LAYOUT
# -----------------------------
left_col, right_col = st.columns([1.1, 1], gap="large")

with left_col:
    st.markdown("""
<div class="info-card-box">
    <div class="info-card-title">📍 Coppermill Tennis Court</div>
    <p><strong>Address:</strong> 13287 Coppermill Dr, Herndon, VA 20171</p>
    <p><strong>Operating Seasons:</strong> Spring, Summer, & Fall</p>
    <p><strong>Amenities:</strong> Outdoor hard courts, lighted facilities, and adjacent public parking.</p>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="info-card-box">
    <div class="info-card-title">🗺️ Maps & Directions</div>
    
    <a href="https://maps.google.com/?q=13287+Coppermill+Dr,+Herndon,+VA+20171" target="_blank" class="action-link-btn">
        🚗 Open in Google Maps
    </a>

    <a href="https://maps.apple.com/?address=13287+Coppermill+Dr,+Herndon,+VA+20171" target="_blank" class="action-link-btn">
        🍏 Open in Apple Maps
    </a>

    <a href="https://waze.com/ul?q=13287+Coppermill+Dr+Herndon+VA" target="_blank" class="action-link-btn">
        🚙 Open in Waze
    </a>

    <a href="https://YOUR_SECONDARY_LOCATION_LINK.com" target="_blank" class="action-link-btn">
        🎾 Indoor Facility Backup Location Link
    </a>
</div>
""", unsafe_allow_html=True)

with right_col:
    st.markdown("""
<div class="info-card-title" style="margin-bottom: 8px;">📌 Interactive Map View</div>
""", unsafe_allow_html=True)

    court_coords = {
        "lat": [38.938722],
        "lon": [-77.408750]
    }

    st.map(court_coords, zoom=14)

    st.caption("Coordinates: 38°56'19.4\"N 77°24'31.5\"W | Coppermill Dr, Herndon, VA")
