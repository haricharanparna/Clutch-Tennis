import streamlit as st
import re
from supabase import create_client

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Clutch Tennis | Login",
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
# COACH EMAILS
# ============================================================

COACH_EMAILS = {
    "parnamayur@gmail.com",
    "haricharanparna@gmail.com",
    "thejonidhips@gmail.com",
    "lavanya.omtri@gmail.com"
}

# ============================================================
# IF ALREADY LOGGED IN
# ============================================================

if st.session_state.get("logged_in", False):

    user = st.session_state.get("user")

    if user and user.email:
        user_email = user.email.lower()

        if user_email in COACH_EMAILS:
            st.switch_page("pages/coach.py")
        else:
            st.switch_page("pages/playerdashboard.py")

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

/* Header */

.login-header {
    text-align: center;
    margin-bottom: 25px;
}

.login-brand {
    font-size: 1.8rem;
    font-weight: 800;
    color: #0B3D2E;
    letter-spacing: -0.5px;
}

.login-brand span {
    color: #88C425;
}

.login-subtitle {
    font-size: 0.95rem;
    color: #66706B;
    margin-top: 6px;
}

/* Inputs */

div[data-baseweb="input"] {
    border-radius: 12px !important;
    background-color: #FFFFFF !important;
    border: 1px solid #E4E9E4 !important;
}

div[data-baseweb="input"]:focus-within {
    border-color: #0B3D2E !important;
    box-shadow: 0 0 0 1px #0B3D2E !important;
}

/* Form */

[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E4E9E4;
    border-radius: 20px;
    padding: 30px 25px;
    box-shadow: 0 10px 30px rgba(23,32,28,0.05);
}

/* Primary Button */

div.stButton > button,
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

div.stButton > button:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    background: #145A43 !important;
    color: #FFFFFF !important;
    transform: translateY(-1px);
}

/* Secondary buttons */

.secondary-btn-container {
    margin-top: 15px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="login-header">
    <div class="login-brand">🎾 CLUTCH<span>TENNIS</span></div>
    <div class="login-subtitle">
        Welcome back! Please enter your details.
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# LOGIN FORM
# ============================================================

with st.form("login_form", clear_on_submit=False):

    emailinput = st.text_input(
        "Email Address",
        placeholder="player@clutch-tennis.com"
    )

    passinput = st.text_input(
        "Password",
        type="password",
        placeholder="••••••••"
    )

    loginbutton = st.form_submit_button(
        "Sign In",
        use_container_width=True
    )

# ============================================================
# SECONDARY ACTIONS
# ============================================================

col1, col2 = st.columns(2)

with col1:
    forgotpassword = st.button(
        "Forgot Password?",
        use_container_width=True,
        type="secondary"
    )

with col2:
    signup_button = st.button(
        "Create Account",
        use_container_width=True,
        type="secondary"
    )

# ============================================================
# CREATE ACCOUNT
# ============================================================

if signup_button:
    st.switch_page("pages/signup.py")

# ============================================================
# FORGOT PASSWORD
# ============================================================

if forgotpassword:

    if not emailinput:
        st.error("Please enter your email address above first.")

    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", emailinput):
        st.error("Please enter a valid email address.")

    else:

        try:

            supabase.auth.reset_password_for_email(
                emailinput,
                options={
                    "redirect_to": (
                        "https://clutch-tennis-6yc8kmr8cduasgptdslws4"
                        ".streamlit.app/reset_password"
                    )
                }
            )

            st.success(
                "Password reset email sent! Check your inbox for the link."
            )

        except Exception:
            st.error(
                "Unable to send reset email. Please try again."
            )

# ============================================================
# LOGIN HANDLER
# ============================================================

if loginbutton:

    if not emailinput or not passinput:

        st.error(
            "Please enter both your email and your password."
        )

    elif not re.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        emailinput
    ):

        st.error(
            "Please enter a valid email address."
        )

    else:

        try:

            data = supabase.auth.sign_in_with_password({
                "email": emailinput,
                "password": passinput
            })

            if data.user:

                # Save login information
                st.session_state["logged_in"] = True
                st.session_state["user"] = data.user

                # Get logged-in email
                user_email = data.user.email.lower()

                # ====================================================
                # ROLE CHECK
                # ====================================================

                if user_email in COACH_EMAILS:

                    # Coach
                    st.switch_page("pages/coach.py")

                else:

                    # Player
                    st.switch_page("pages/playerdashboard.py")

            else:

                st.error(
                    "Login failed. Please try again."
                )

        except Exception:

            st.error(
                "Incorrect email or password."
            )
