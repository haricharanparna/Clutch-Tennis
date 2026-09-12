import streamlit as st
import requests

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Contact Us | Clutch Tennis",
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
.contact-hero {
    background: linear-gradient(135deg, #082D22 0%, #0B3D2E 55%, #145A43 100%);
    border-radius: 24px;
    padding: 45px 40px;
    color: white;
    margin-bottom: 35px;
    box-shadow: 0 15px 35px rgba(11,61,46,0.15);
}

.contact-kicker {
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.8rem;
    font-weight: 700;
    color: #C9E86A;
    margin-bottom: 8px;
}

.contact-title {
    font-size: 2.8rem;
    font-weight: 800;
    margin: 0;
}

.contact-subtitle {
    font-size: 1rem;
    opacity: 0.85;
    margin-top: 10px;
    max-width: 600px;
}

/* INFO CARDS */
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
.social-link-btn {
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

.social-link-btn:hover {
    background: #0B3D2E;
    color: #FFFFFF;
    border-color: #0B3D2E;
}

/* FORM STYLING */
[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 30px 25px;
    box-shadow: 0 10px 30px rgba(23,32,28,0.05);
}

div[data-baseweb="input"], div[data-baseweb="textarea"] {
    border-radius: 12px !important;
    background-color: #FFFFFF !important;
    border: 1px solid #E4E9E4 !important;
}

div[data-testid="stFormSubmitButton"] > button {
    background: #0B3D2E !important;
    color: #FFFFFF !important;
    border: 0 !important;
    border-radius: 12px !important;
    min-height: 48px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
    margin-top: 10px;
}

div[data-testid="stFormSubmitButton"] > button:hover {
    background: #145A43 !important;
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
        st.switch_page("pages/about.py")

with nav_col5:
    st.markdown('<div class="nav-link-btn-marker"></div>', unsafe_allow_html=True)
    if st.button("FAQ", key="nav_faq"):
        st.switch_page("pages/faq.py")

with nav_col6:
    st.markdown('<div class="nav-link-btn-marker"></div>', unsafe_allow_html=True)
    if st.button("Contact", key="nav_contact"):
        st.rerun()

with nav_col7:
    st.markdown('<div class="nav-cta-marker"></div>', unsafe_allow_html=True)
    if st.button("Book a Free Trial", key="nav_cta_btn", use_container_width=True):
        st.switch_page("pages/booking.py")

# -----------------------------
# HERO HEADER
# -----------------------------
st.markdown("""
<div class="contact-hero">
    <div class="contact-kicker">Get In Touch</div>
    <div class="contact-title">Contact Our Team</div>
    <div class="contact-subtitle">
        Have questions about training, scheduling, or court locations? Send us a message or connect through our channels.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# TWO-COLUMN CONTENT AREA
# -----------------------------
left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    # --- DIRECT CONTACT DETAILS ---
    st.markdown("""
    <div class="info-card-box">
        <div class="info-card-title">📞 Direct Contact</div>
        <p><strong>Email:</strong> haricharanparna@gmail.com</p>
        <p><strong>Phone:</strong> (703) 962-0621</p>
        <p><strong>Location:</strong> Coppermill Tennis Court, Herndon, VA</p>
    </div>
    """, unsafe_allow_html=True)

    # --- SOCIAL & EXTERNAL LINKS PLACEHOLDERS ---
    st.markdown("""
    <div class="info-card-box">
        <div class="info-card-title">🌐 Connect With Us</div>
        <!-- PLACEHOLDER LINK 1: INSTAGRAM -->
        <a href="https://instagram.com/YOUR_INSTAGRAM_HANDLE" target="_blank" class="social-link-btn">
            📷 Follow on Instagram
        </a>
        <!-- PLACEHOLDER LINK 2: FACEBOOK -->
        <a href="https://facebook.com/YOUR_FACEBOOK_PAGE" target="_blank" class="social-link-btn">
            📘 Like us on Facebook
        </a>
        <!-- PLACEHOLDER LINK 3: GOOGLE MAPS / LOCATION -->
        <a href="https://maps.google.com/?q=13287+Coppermill+Dr,+Herndon,+VA+20171" target="_blank" class="social-link-btn">
            📍 Open Location in Google Maps
        </a>
        <!-- PLACEHOLDER LINK 4: CUSTOM LINK (e.g. WhatsApp, Linktree, YouTube) -->
        <a href="https://YOUR_CUSTOM_LINK_HERE.com" target="_blank" class="social-link-btn">
            🔗 Additional Custom Link Placeholder
        </a>
    </div>
    """, unsafe_allow_html=True)

with right_col:
    # --- INTERACTIVE CONTACT FORM ---
    st.markdown("""
    <div class="info-card-title" style="margin-bottom: 8px;">✉️ Send Us a Message</div>
    """, unsafe_allow_html=True)

    with st.form("contact_form", clear_on_submit=True):
        sender_name = st.text_input("Full Name", placeholder="Alex Morgan")
        sender_email = st.text_input("Email Address", placeholder="alex@example.com")
        subject = st.text_input("Subject", placeholder="Question about Private Lessons")
        message = st.text_area("Message", placeholder="Write your message here...", height=150)
        
        submitted = st.form_submit_button("Send Message", use_container_width=True)

    if submitted:
        if not sender_name.strip() or not sender_email.strip() or not message.strip():
            st.error("❌ Please fill in all required fields (Name, Email, and Message).")
        else:
            # PLACEHOLDER FORM ENDPOINT (Replace endpoint URL below with your SheetMonkey / Formspree URL)
            endpoint_url = "https://api.sheetmonkey.io/form/YOUR_FORM_ID_HERE"
            
            payload = {
                "Name": sender_name,
                "Email": sender_email,
                "Subject": subject,
                "Message": message
            }
            
            try:
                # Simulating request submission logic
                # response = requests.post(endpoint_url, json=payload, timeout=10)
                st.success("Message sent successfully! 🎾 We'll respond shortly.")
            except Exception:
                st.error("Failed to send message. Please try again later.")
