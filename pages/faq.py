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
    max-width: 1000px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

#MainMenu, footer {
    visibility: hidden;
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

/* BACK BUTTON */
div.stButton > button {
    background: transparent;
    color: #0B3D2E;
    border: 2px solid #0B3D2E;
    border-radius: 20px;
    font-weight: 700;
    padding: 6px 20px;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    background: #0B3D2E;
    color: #FFFFFF;
    border-color: #0B3D2E;
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
# TOP NAVIGATION
# -----------------------------
col_back, _ = st.columns([1, 4])
with col_back:
    if st.button("← Back to Home", key="back_home"):
        st.switch_page("app.py")

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
