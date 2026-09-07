import streamlit as st
from supabase import create_client
import streamlit.components.v1 as components

# Page Config
st.set_page_config(
    page_title="Clutch Tennis | Reset Password",
    page_icon="🎾",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Connect to Supabase
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# Read the Supabase recovery tokens from the URL fragment
components.html(
    """
    <script>
        const hash = window.parent.location.hash;

        if (hash && hash.includes("access_token")) {
            const params = new URLSearchParams(hash.substring(1));

            const accessToken = params.get("access_token");
            const refreshToken = params.get("refresh_token");

            if (accessToken && refreshToken) {
                const url =
                    window.parent.location.pathname +
                    "?access_token=" +
                    encodeURIComponent(accessToken) +
                    "&refresh_token=" +
                    encodeURIComponent(refreshToken);

                window.parent.history.replaceState(
                    {},
                    "",
                    url
                );

                window.parent.location.reload();
            }
        }
    </script>
    """,
    height=0
)

# Get tokens from query parameters
access_token = st.query_params.get("access_token")
refresh_token = st.query_params.get("refresh_token")

# Establish the recovery session
if access_token and refresh_token:
    try:
        supabase.auth.set_session(
            access_token,
            refresh_token
        )
        st.session_state["recovery_session"] = True
    except Exception:
        st.session_state["recovery_session"] = False

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
    max-width: 480px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Card Wrapper Header */
.reset-header {
    text-align: center;
    margin-bottom: 25px;
}

.reset-brand {
    font-size: 1.8rem;
    font-weight: 800;
    color: #0B3D2E;
    letter-spacing: -0.5px;
}

.reset-brand span {
    color: #88C425;
}

.reset-subtitle {
    font-size: 0.95rem;
    color: #66706B;
    margin-top: 6px;
}

/* Input Fields Styling */
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

/* Primary Button Styling */
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

/* Secondary Button Styling */
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

# Header Section
st.markdown("""
<div class="reset-header">
    <div class="reset-brand">🎾 CLUTCH<span>TENNIS</span></div>
    <div class="reset-subtitle">Choose a new, secure password for your account.</div>
</div>
""", unsafe_allow_html=True)

# Show invalid token warning early if applicable
if access_token and refresh_token and not st.session_state.get("recovery_session", False):
    st.error("Your password reset link is invalid or expired. Please request a new one.")

# Reset Password Form
with st.form("reset_form", clear_on_submit=False):
    newpassword = st.text_input(
        "New Password",
        type="password",
        placeholder="At least 6 characters"
    )

    confirmpassword = st.text_input(
        "Confirm New Password",
        type="password",
        placeholder="Re-enter new password"
    )

    resetbutton = st.form_submit_button(
        "Update Password",
        use_container_width=True
    )

# Navigation Back to Login
login_button = st.button(
    "← Back to Login",
    use_container_width=True
)

if login_button:
    st.switch_page("pages/login.py")

# Reset Handler
if resetbutton:
    if not st.session_state.get("recovery_session", False):
        st.error("Your password reset session is invalid. Please request a new reset link from the login page.")
    elif not newpassword or not confirmpassword:
        st.error("Please fill out both password fields.")
    elif newpassword != confirmpassword:
        st.error("Passwords do not match.")
    elif len(newpassword) < 6:
        st.error("Password must be at least 6 characters long.")
    else:
        try:
            response = supabase.auth.update_user({
                "password": newpassword
            })

            if response.user:
                st.success("Password updated successfully! 🎾")
                st.info("You can now log in with your new password.")
                st.switch_page("pages/login.py")
            else:
                st.error("Password could not be updated. Please try again.")

        except Exception:
            st.error("Unable to reset your password. Please request a new reset email.")
