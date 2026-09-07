import streamlit as st
import re
from supabase import create_client
import extra_streamlit_components as stx

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
# CONNECT TO SUPABASE & COOKIE MANAGER
# ============================================================

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# Initialize Cookie Manager
cookie_manager = stx.CookieManager()

COOKIE_NAME = "clutch_tennis_auth"
FIVE_DAYS_IN_SECONDS = 5 * 24 * 60 * 60  # 432,000 seconds


# ============================================================
# SESSION MANAGEMENT (PERSISTENT COOKIES)
# ============================================================

def restore_session_from_cookie():
    """
    Checks for a valid session token stored in browser cookies
    and restores the Supabase session on page refresh.
    """
    token = cookie_manager.get(cookie=COOKIE_NAME)
    
    if token and not st.session_state.get("logged_in", False):
        try:
            # Restore Supabase session using stored refresh token
            res = supabase.auth.set_session(token["access_token"], token["refresh_token"])
            if res.user:
                st.session_state["logged_in"] = True
                st.session_state["user"] = res.user
                return True
        except Exception:
            # Remove invalid or expired cookie
            cookie_manager.delete(COOKIE_NAME)
            st.session_state.clear()
            return False

    return st.session_state.get("logged_in", False)


# Attempt to restore session immediately on page load
if restore_session_from_cookie():
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

/* Card Wrapper Header */

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

/* Input Fields */

div[data-baseweb="input"] {
    border-radius: 12px !important;
    background-color: #FFFFFF !important;
    border: 1px solid #E4E9E4 !important;
}

div[data-baseweb="input"]:focus-within {
    border-color: #0B3D2E !important;
    box-shadow: 0 0 0 1px #0B3D2E !important;
}

/* Form Container */

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

/* Secondary Buttons */

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
    <div class="login-brand">
        🎾 CLUTCH<span>TENNIS</span>
    </div>

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
                        "https://clutch-tennis-6yc8kmr8cduasgptdslws"
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
# LOGIN HANDLER WITH 5-DAY PERSISTENCE
# ============================================================

if loginbutton:

    if not emailinput or not passinput:

        st.error(
            "Please enter both your email and your password."
        )

    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", emailinput):

        st.error(
            "Please enter a valid email address."
        )

    else:

        try:

            data = supabase.auth.sign_in_with_password({
                "email": emailinput,
                "password": passinput
            })

            if data.user and data.session:

                # Save tokens in a 5-day browser cookie
                cookie_manager.set(
                    cookie=COOKIE_NAME,
                    val={
                        "access_token": data.session.access_token,
                        "refresh_token": data.session.refresh_token
                    },
                    max_age=FIVE_DAYS_IN_SECONDS
                )

                st.session_state["logged_in"] = True
                st.session_state["user"] = data.user

                # Go to main application
                st.switch_page("app.py")

            else:

                st.error(
                    "Login failed. Please try again."
                )

        except Exception:

            st.error(
                "Incorrect email or password."
            )
