import streamlit as st
import re
from supabase import create_client
from coach_emails import get_coach_emails

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Clutch Tennis | Sign Up",
    page_icon="🎾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CONNECT TO SUPABASE
# ============================================================

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# ============================================================
# REDIRECT IF ALREADY LOGGED IN
# ============================================================

if st.session_state.get("logged_in", False):
    st.switch_page("app.py")

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
    background: radial-gradient(
        circle at 50% 10%,
        rgba(11,61,46,0.08),
        transparent 40%
    ), #F7F8F5;
    color: #17201C;
}

[data-testid="stHeader"] {
    background: transparent;
}

#MainMenu, footer {
    visibility: hidden;
}

.block-container {
    max-width: 480px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.signup-header {
    text-align: center;
    margin-bottom: 25px;
}

.signup-brand {
    font-size: 1.8rem;
    font-weight: 800;
    color: #0B3D2E;
    letter-spacing: -0.5px;
}

.signup-brand span {
    color: #88C425;
}

.signup-subtitle {
    font-size: 0.95rem;
    color: #66706B;
    margin-top: 6px;
}

div[data-baseweb="input"] {
    border-radius: 12px !important;
    background-color: #FFFFFF !important;
    border: 1px solid #E4E9E4 !important;
}

div[data-baseweb="input"]:focus-within {
    border-color: #0B3D2E !important;
    box-shadow: 0 0 0 1px #0B3D2E !important;
}

[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 30px 25px;
    box-shadow: 0 10px 30px rgba(23,32,28,0.05);
}

div[data-testid="stFormSubmitButton"] > button {
    background: #0B3D2E !important;
    color: #FFFFFF !important;
    border: 0 !important;
    border-radius: 12px !important;
    min-height: 46px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}

div[data-testid="stFormSubmitButton"] > button:hover {
    background: #145A43 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
}

div.stButton > button {
    background: transparent !important;
    color: #0B3D2E !important;
    border: 1px solid #E4E9E4 !important;
    border-radius: 12px !important;
    min-height: 42px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    margin-top: 15px;
    transition: all 0.2s ease !important;
}

div.stButton > button:hover {
    background: #EEF5D9 !important;
    border-color: #88C425 !important;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="signup-header">
    <div class="signup-brand">🎾 CLUTCH<span>TENNIS</span></div>
    <div class="signup-subtitle">
        Create an account to start your training journey.
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SIGNUP FORM
# ============================================================

with st.form("signup_form", clear_on_submit=False):

    nameinput = st.text_input(
        "Full Name",
        placeholder="Alex Morgan"
    )

    emailinput = st.text_input(
        "Email Address",
        placeholder="player@clutch-tennis.com"
    )

    passwordinput = st.text_input(
        "Password",
        type="password",
        placeholder="At least 6 characters"
    )

    confirmpassword = st.text_input(
        "Confirm Password",
        type="password",
        placeholder="Re-enter password"
    )

    createacc = st.form_submit_button(
        "Create Account",
        use_container_width=True
    )

# ============================================================
# BACK TO LOGIN
# ============================================================

login_button = st.button(
    "← Back to Login",
    use_container_width=True
)

if login_button:
    st.switch_page("pages/login.py")

# ============================================================
# ACCOUNT CREATION
# ============================================================

if createacc:

    # -----------------------------
    # BASIC VALIDATION
    # -----------------------------

    if not nameinput or not emailinput or not passwordinput or not confirmpassword:
        st.error("Please fill out all fields.")

    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", emailinput):
        st.error("Please enter a valid email address.")

    elif passwordinput != confirmpassword:
        st.error("Passwords do not match.")

    elif len(passwordinput) < 6:
        st.error("Password must be at least 6 characters long.")

    else:

        # -----------------------------
        # CHECK COACH GOOGLE SHEET
        # -----------------------------

        coach_emails = get_coach_emails()

        email_clean = emailinput.strip().lower()

        if email_clean in coach_emails:
            role = "coach"
        else:
            role = "player"

        # -----------------------------
        # CREATE SUPABASE ACCOUNT
        # -----------------------------

        try:

            data = supabase.auth.sign_up({
                "email": email_clean,
                "password": passwordinput,
                "options": {
                    "data": {
                        "full_name": nameinput,
                        "role": role
                    }
                }
            })

            if data.user:

                if role == "coach":
                    st.success("Coach account created successfully! 🎾")
                else:
                    st.success("Player account created successfully! 🎾")

                st.info("You can now log in with your credentials.")

                st.switch_page("pages/login.py")

            else:
                st.error(
                    "Account could not be created. Please try again."
                )

        except Exception as e:
            st.error(
                "Something went wrong during account creation. "
                "Please try again."
            )
