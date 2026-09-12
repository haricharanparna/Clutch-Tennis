import streamlit as st
import requests
import re
from datetime import datetime
import streamlit.components.v1 as components

# Page Config
st.set_page_config(
    page_title="Book a Lesson | Clutch Tennis",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Login Protection
if not st.session_state.get("logged_in", False):
    st.switch_page("pages/login.py")

# Custom Styling (Matches Clutch Tennis Theme)
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

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    max-width: 1150px;
    padding-top: 1rem;
    padding-bottom: 3rem;
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

/* Header Banner */
.booking-header {
    text-align: center;
    margin-bottom: 25px;
}

.booking-brand {
    font-size: 1.8rem;
    font-weight: 800;
    color: #0B3D2E;
    letter-spacing: -0.5px;
}

.booking-brand span {
    color: #88C425;
}

.booking-subtitle {
    font-size: 0.95rem;
    color: #66706B;
    margin-top: 6px;
}

/* Form Container Styling */
[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 30px 25px;
    box-shadow: 0 10px 30px rgba(23,32,28,0.05);
}

/* Input Fields Styling */
div[data-baseweb="input"], div[data-baseweb="select"] > div {
    border-radius: 12px !important;
    background-color: #FFFFFF !important;
    border: 1px solid #E4E9E4 !important;
}

div[data-baseweb="input"]:focus-within, div[data-baseweb="select"] > div:focus-within {
    border-color: #0B3D2E !important;
    box-shadow: 0 0 0 1px #0B3D2E !important;
}

/* Form Submit Button Styling */
div[data-testid="stFormSubmitButton"] > button {
    background: #0B3D2E !important;
    color: #FFFFFF !important;
    border: 0 !important;
    border-radius: 12px !important;
    min-height: 48px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    margin-top: 10px;
}

div[data-testid="stFormSubmitButton"] > button:hover {
    background: #145A43 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
}

/* Section Card Wrapper */
.disclaimer-card {
    background: #FFFFFF;
    border: 1px solid #E4E9E4;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(23,32,28,0.03);
}

.section-title {
    font-weight: 700;
    color: #0B3D2E;
    font-size: 1.1rem;
    margin-bottom: 6px;
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
        st.switch_page("app.py")

with nav_col7:
    st.markdown('<div class="nav-cta-marker"></div>', unsafe_allow_html=True)
    if st.button("Book a Free Trial", key="nav_cta_btn", use_container_width=True):
        st.rerun()

# Configuration & Constants
availability_url = (
    "https://script.google.com/macros/s/"
    "AKfycbxclfNHxhTVJeXhwsN14---f3qdq0fGedhzZANjNZ4b3dp202xyVzhx5FGqVDha5aKBhQ/"
    "exec"
)

times = [
    "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
    "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM",
    "5:00 PM", "6:00 PM", "7:00 PM"
]

# Session State Initialization
if "name_error" not in st.session_state:
    st.session_state["name_error"] = False

if "email_error" not in st.session_state:
    st.session_state["email_error"] = False

if "time_error" not in st.session_state:
    st.session_state["time_error"] = False

# Center Content Layout Wrapper for Form Elements
form_col1, form_col2, form_col3 = st.columns([1, 2, 1])

with form_col2:
    # Header Section
    st.markdown("""
    <div class="booking-header">
        <div class="booking-brand">🎾 CLUTCH<span>TENNIS</span></div>
        <div class="booking-subtitle">Request a session with your coach and elevate your game.</div>
    </div>
    """, unsafe_allow_html=True)

    # Date Picker Section
    preferred_date = st.date_input("Select Preferred Date")

    # Dynamic Availability Fetch
    try:
        availability_response = requests.get(
            availability_url,
            params={"date": str(preferred_date)},
            timeout=10
        )
        if availability_response.status_code == 200:
            try:
                booked_times = availability_response.json().get("bookedTimes", [])
            except ValueError:
                booked_times = []
        else:
            booked_times = []
    except Exception:
        booked_times = []

    available_times = [t for t in times if t not in booked_times]

    # Validation Error Border Styles
    if st.session_state["name_error"]:
        st.markdown("""
        <style>
        div[data-testid="stTextInput"]:has(input[aria-label="Full Name"]) input {
            border: 2px solid #D9383A !important;
        }
        </style>
        """, unsafe_allow_html=True)

    if st.session_state["email_error"]:
        st.markdown("""
        <style>
        div[data-testid="stTextInput"]:has(input[aria-label="Your Email Address"]) input {
            border: 2px solid #D9383A !important;
        }
        </style>
        """, unsafe_allow_html=True)

    # Disclaimer Box Section
    st.markdown('<div class="section-title">Disclaimer & Booking Agreement</div>', unsafe_allow_html=True)
    st.caption("Please review the agreement below prior to submitting your request.")

    components.html(
        """
        <div id="disclaimerBox" style="
            height: 240px;
            overflow-y: auto;
            border: 1px solid #E4E9E4;
            border-radius: 12px;
            padding: 18px;
            background-color: #FFFFFF;
            color: #17201C;
            font-family: 'Inter', sans-serif;
            font-size: 0.88rem;
            line-height: 1.6;
            box-sizing: border-box;
        ">
            <h4 style="color:#0B3D2E; margin-top:0; font-size: 1rem; font-weight:700;">
                Clutch Tennis Participation & Booking Disclaimer
            </h4>
            <p>Tennis coaching involves physical activity, movement, and participation in drills. Physical activity involves inherent risks, including the possibility of injury.</p>
            <p>By requesting a session, you acknowledge these risks and agree to follow all coaching and safety instructions during practice.</p>
            <p>Participants are expected to communicate any injuries or limitations prior to sessions and bring appropriate court footwear and gear.</p>
            <p>Outdoor sessions are subject to weather conditions and may be rescheduled due to rain, wet courts, or hazardous conditions.</p>
            <p>Participation does not guarantee specific athletic outcomes; growth relies on personal effort, consistency, and training.</p>
            <hr style="border:0; border-top:1px solid #E4E9E4; margin:15px 0;">
            <p style="text-align:center; color:#0B3D2E; font-weight:700; margin-bottom:0;">
                Scroll to the bottom to acknowledge agreement.
            </p>
        </div>
        """,
        height=260
    )

    # Checkbox Confirmation
    disclaimer_agreed = st.checkbox(
        "I have read and agree to the Participation & Booking Disclaimer."
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # Main Booking Form
    with st.form("booking_form", clear_on_submit=False):
        name = st.text_input(
            "Full Name",
            placeholder="Alex Morgan",
            key="booking_name"
        )

        email = st.text_input(
            "Your Email Address",
            placeholder="player@clutch-tennis.com",
            key="booking_email"
        )

        lesson_type = st.selectbox(
            "Lesson Type",
            [
                "Private Coaching",
                "Group Coaching",
                "Mental Toughness",
                "Match Play & Strategy"
            ]
        )

        if available_times:
            preferred_time = st.selectbox(
                "Preferred Time",
                available_times,
                key="booking_time"
            )
        else:
            st.warning("No available time slots for this selected date.")
            preferred_time = None

        notes = st.text_area(
            "Goals or Special Requests",
            placeholder="Tell us what you'd like to focus on during this session..."
        )

        submitted = st.form_submit_button(
            "Submit Booking Request",
            use_container_width=True
        )

    # Form Validation & Execution
    if submitted:
        name_error = not name.strip()
        email_error = not email.strip() or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email)
        time_error = not preferred_time
        disclaimer_error = not disclaimer_agreed

        st.session_state["name_error"] = name_error
        st.session_state["email_error"] = email_error
        st.session_state["time_error"] = time_error

        if name_error:
            st.error("❌ Full Name: Please enter your name.")

        if email_error:
            st.error("❌ Email: Please enter a valid email address.")

        if time_error:
            st.error("❌ Preferred Time: Please select an available time.")

        if disclaimer_error:
            st.error("❌ Disclaimer: Please accept the booking agreement above.")

        if not name_error and not email_error and not time_error and not disclaimer_error:
            with st.spinner("Submitting your booking request..."):
                endpoint = "https://api.sheetmonkey.io/form/fQvQ98iNDidpE7BcoVNnmH"
                disclaimer_date = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

                payload = {
                    "Name": name,
                    "Email": email,
                    "Lesson Type": lesson_type,
                    "Preferred Date": str(preferred_date),
                    "Preferred Time": str(preferred_time),
                    "Notes": notes,
                    "Disclaimer Agreed": "Yes",
                    "Disclaimer Date": disclaimer_date,
                    "Disclaimer Version": "Version 1.0"
                }

                try:
                    response = requests.post(
                        endpoint,
                        json=payload,
                        headers={"Content-Type": "application/json"},
                        timeout=15
                    )

                    if response.status_code in [200, 201]:
                        st.success("Booking request submitted successfully! 🎾")
                        st.info("Your request has been recorded. We will confirm your session shortly.")

                        st.session_state["name_error"] = False
                        st.session_state["email_error"] = False
                        st.session_state["time_error"] = False
                    else:
                        st.error("Submission failed. Please check your network connection and try again.")

                except Exception:
                    st.error("Network error encountered. Please try again.")
