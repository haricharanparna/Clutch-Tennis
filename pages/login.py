import textwrap
import streamlit as st
from supabase import create_client

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Login | Clutch Tennis",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# SUPABASE CLIENT SETUP
# ============================================================

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# Define exact app URL for redirects
APP_URL = st.secrets.get("APP_URL", "http://localhost:8501")

# Initialize session state keys safely
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "supabase_session" not in st.session_state:
    st.session_state["supabase_session"] = None

# ============================================================
# CHECK EXISTING SESSION OR PROCESS URL CALLBACK
# ============================================================

query_params = st.query_params

# 1. Process OAuth / Magic Link callback parameter
if "code" in query_params:
    auth_code = query_params.get("code")
    if auth_code and isinstance(auth_code, str) and auth_code.strip():
        try:
            auth_response = supabase.auth.exchange_code_for_session({"auth_code": auth_code})
            if auth_response and auth_response.session:
                st.session_state["logged_in"] = True
                st.session_state["user"] = auth_response.user
                st.session_state["supabase_session"] = auth_response.session
                
                # Clear parameters to prevent re-submitting the same code on refresh
                st.query_params.clear()
                st.switch_page("pages/player_dashboard.py")
        except Exception as err:
            st.error(f"Authentication failed: {str(err)}")
            st.query_params.clear()

# 2. Redirect immediately if already logged in
if st.session_state["logged_in"]:
    st.switch_page("pages/player_dashboard.py")

# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    textwrap.dedent("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: #F7F8F5;
    color: #17201C;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 450px;
    padding-top: 4rem;
    padding-bottom: 4rem;
}

#MainMenu, footer {
    visibility: hidden;
}

.login-header {
    text-align: center;
    margin-bottom: 25px;
}

.login-logo {
    font-weight: 800;
    font-size: 1.6rem;
    color: #0B3D2E;
    letter-spacing: -0.5px;
}

.login-logo span {
    color: #88C425;
}

.login-subtitle {
    color: #66706B;
    font-size: 0.95rem;
    margin-top: 6px;
}

.divider-text {
    text-align: center;
    color: #8A938E;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 20px 0;
}

div.stButton > button {
    border-radius: 12px !important;
    min-height: 48px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    width: 100% !important;
}

div[data-testid="stColumn"]:has(div.google-btn-marker) div.stButton > button {
    background-color: #FFFFFF !important;
    color: #17201C !important;
    border: 1px solid #D1D5DB !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
}

div[data-testid="stColumn"]:has(div.google-btn-marker) div.stButton > button:hover {
    background-color: #F9FAFB !important;
    border-color: #9CA3AF !important;
}

div[data-testid="stColumn"]:has(div.submit-btn-marker) div.stButton > button {
    background: #0B3D2E !important;
    color: white !important;
    border: 0 !important;
}

div[data-testid="stColumn"]:has(div.submit-btn-marker) div.stButton > button:hover {
    background-color: #145A43 !important;
}
</style>
"""),
    unsafe_allow_html=True,
)

# ============================================================
# LOGIN INTERFACE
# ============================================================

st.markdown(
    textwrap.dedent("""
        <div class="login-header">
            <div class="login-logo">🎾 CLUTCH<span>TENNIS</span></div>
            <div class="login-subtitle">Sign in to access your player dashboard</div>
        </div>
    """),
    unsafe_allow_html=True,
)

# Google OAuth Section
st.markdown('<div class="google-btn-marker"></div>', unsafe_allow_html=True)
if st.button("🌐 Continue with Google", key="google_login", use_container_width=True):
    try:
        response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": f"{APP_URL}"
            }
        })
        if response.url:
            st.markdown(f'<a href="{response.url}" target="_self" style="text-decoration:none;"><button style="width:100%; height:48px; border-radius:12px; background-color:#0B3D2E; color:white; font-weight:700; border:none; cursor:pointer;">Proceed to Google Authorization</button></a>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Google sign-in error: {str(e)}")

st.markdown('<div class="divider-text">OR EMAIL LOGIN</div>', unsafe_allow_html=True)

# Email/Password Section
with st.form("login_form", clear_on_submit=False):
    email = st.text_input("Email Address", placeholder="player@example.com")
    password = st.text_input("Password", type="password", placeholder="••••••••")
    
    st.markdown('<div class="submit-btn-marker"></div>', unsafe_allow_html=True)
    submit = st.form_submit_button("Sign In with Email", use_container_width=True)

    if submit:
        if not email or not password:
            st.warning("Please enter both your email and password.")
        else:
            try:
                response = supabase.auth.sign_in_with_password({
                    "email": email.strip(),
                    "password": password
                })
                
                if response.session and response.user:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = response.user
                    st.session_state["supabase_session"] = response.session
                    st.success("Login successful!")
                    st.switch_page("pages/player_dashboard.py")
                else:
                    st.error("Authentication failed: Invalid email or password.")
            except Exception as e:
                st.error(f"Login failed: {str(e)}")
