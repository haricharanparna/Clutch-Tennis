import streamlit as st

st.set_page_config(
    page_title="FAQ | Clutch Tennis",
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

/* HEADER CARD */
.faq-header {
    background: linear-gradient(135deg, #082D22 0%, #0B3D2E 55%, #145A43 100%);
    border-radius: 24px;
    padding: 45px 40px;
    color: white;
    margin-bottom: 35px;
    box-shadow: 0 15px 35px rgba(11,61,46,0.15);
}

.faq-kicker {
    text-transform: uppercase;
    letter-spacing: 2px;
    font-size: 0.8rem;
    font-weight: 700;
    color: #C9E86A;
    margin-bottom: 8px;
}

.faq-title {
    font-size: 2.8rem;
    font-weight: 800;
    margin: 0;
}

.faq-subtitle {
    font-size: 1rem;
    opacity: 0.85;
    margin-top: 10px;
    max-width: 600px;
}

/* SECTION TITLES */
.faq-section-title {
    color: #0B3D2E;
    font-size: 1.35rem;
    font-weight: 800;
    margin-top: 30px;
    margin-bottom: 15px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* EXPANDER CUSTOMIZATION */
.stExpander {
    background: #FFFFFF !important;
    border: 1px solid #E4E9E4 !important;
    border-radius: 14px !important;
    margin-bottom: 12px !important;
    box-shadow: 0 4px 15px rgba(23,32,28,0.02) !important;
}

.stExpander > details > summary {
    font-weight: 700 !important;
    color: #17201C !important;
    font-size: 1rem !important;
    padding: 14px 18px !important;
}

.stExpander p {
    color: #59635E !important;
    line-height: 1.6 !important;
    font-size: 0.95rem !important;
}

/* CONTACT CTA CARD */
.faq-cta {
    background: white;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 30px;
    margin-top: 40px;
    text-align: center;
    box-shadow: 0 8px 25px rgba(23,32,28,0.04);
}

.faq-cta-title {
    font-size: 1.3rem;
    font-weight: 800;
    color: #0B3D2E;
}

.faq-cta-text {
    color: #66706B;
    font-size: 0.95rem;
    margin-top: 6px;
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
        st.switch_page("pages/location.py")

with nav_col4:
    st.markdown('<div class="nav-link-btn-marker"></div>', unsafe_allow_html=True)
    if st.button("About Us", key="nav_about"):
        st.switch_page("pages/about.py")

with nav_col5:
    st.markdown('<div class="nav-link-btn-marker"></div>', unsafe_allow_html=True)
    if st.button("FAQ", key="nav_faq"):
        st.rerun()

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
<div class="faq-header">
    <div class="faq-kicker">Got Questions?</div>
    <div class="faq-title">Frequently Asked Questions</div>
    <div class="faq-subtitle">
        Everything you need to know about our coaching programs, court locations, scheduling, and trial lessons.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# FAQ CONTENT DATA
# -----------------------------
faqs = {
    "🎾 General & Programs": [
        ("What skill levels do you coach?", "We cater to all skill levels! Whether you are picking up a racquet for the first time, looking to join a recreational USTA team, or preparing for high-school varsity and tournament play, we tailor our programs to meet your goals."),
        ("What is included in the Free Trial session?", "The Free Trial is a 30-minute evaluation session where a coach assesses your skill level, discusses your tennis goals, and introduces you to our core drill structures so you can see if our academy is the right fit."),
        ("What should I bring to my first lesson?", "Please bring your tennis racquet, non-marking tennis court shoes, a water bottle, and athletic wear. If you don't own a racquet yet, let us know in advance and we can provide a demo racquet for your session.")
    ],
    "📅 Scheduling & Bookings": [
        ("How do I schedule or reschedule a lesson?", "You can manage all bookings directly through your dashboard after logging in. To avoid a cancellation fee, lessons must be rescheduled or canceled at least 24 hours in advance."),
        ("What happens if it rains or there is bad weather?", "In the event of rain or unplayable court conditions, outdoor sessions will be canceled at least 1 hour prior to the start time. You will receive a notification via email/SMS, and a credit will be applied to your account to reschedule."),
        ("Are private lessons available on weekends?", "Yes! Private lessons and group clinics run 7 days a week, subject to court availability and coach schedules.")
    ],
    "📍 Location & Facilities": [
        ("Where are the lessons hosted?", "Our primary outdoor courts are located at Coppermill Tennis Court (13287 Coppermill Dr, Herndon, VA 20171). We operate here throughout Spring, Summer, and Fall."),
        ("Is parking available on site?", "Yes, free street parking and designated parking spaces are available directly adjacent to the courts.")
    ],
    "💳 Payments & Pricing": [
        ("What payment methods do you accept?", "We accept all major credit cards, debit cards, and online payments through our secure checkout system. Cash or check payments can also be arranged upon request."),
        ("Do you offer lesson packages or discounts?", "Yes! We offer discounted multi-lesson packages (5-session and 10-session bundles) for private coaching as well as monthly subscription rates for group clinics.")
    ]
}

# -----------------------------
# RENDER FAQ ACCORDIONS
# -----------------------------
for category, items in faqs.items():
    st.markdown(f'<div class="faq-section-title">{category}</div>', unsafe_allow_html=True)
    for question, answer in items:
        with st.expander(question):
            st.write(answer)

# -----------------------------
# FOOTER CTA
# -----------------------------
st.markdown("""
<div class="faq-cta">
    <div class="faq-cta-title">Still have questions?</div>
    <div class="faq-cta-text">
        We're here to help. Reach out to our team at <b>haricharanparna@gmail.com</b> or call <b>(703) 962 0621</b>.
    </div>
</div>
""", unsafe_allow_html=True)
