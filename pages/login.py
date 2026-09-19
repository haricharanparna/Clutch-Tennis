import base64
import hashlib
import secrets
import textwrap
import threading
import time
import uuid
from urllib.parse import urlencode

import streamlit as st
from supabase import create_client

# ============================================================
# PAGE CONFIG (must be the first Streamlit call)
# ============================================================

st.set_page_config(
    page_title="Login | Clutch Tennis",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CONFIG
# ============================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"].rstrip("/")
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]  # must be the ANON key, never service_role
APP_URL = st.secrets.get("APP_URL", "http://localhost:8501").rstrip("/")

DASHBOARD_PAGE = "pages/player_dashboard.py"
VERIFIER_TTL_SECONDS = 60 * 60  # how long a Google login link stays valid

# ============================================================
# SESSION STATE + SUPABASE CLIENT (one client per browser session)
# ============================================================

st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("user", None)
st.session_state.setdefault("supabase_session", None)

# Keeping the client in session_state means the signed-in session stays attached
# to it. Other pages can reuse it: supabase = st.session_state["supabase"]
if "supabase" not in st.session_state:
    st.session_state["supabase"] = create_client(SUPABASE_URL, SUPABASE_KEY)
supabase = st.session_state["supabase"]

# ============================================================
# PKCE HELPERS
#
# Why this exists: Google sign-in opens in a new tab, so the callback arrives
# in a brand-new Streamlit session with a brand-new Supabase client that never
# saw the PKCE code verifier. We generate the verifier ourselves, keep it in
# server memory under a random ID (sid), and pass the sid through the redirect
# URL so the callback can look the verifier up again.
# ============================================================


@st.cache_resource
def _verifier_store() -> dict:
    return {"lock": threading.Lock(), "items": {}}


def _purge_expired(items: dict) -> None:
    cutoff = time.time() - VERIFIER_TTL_SECONDS
    for key in [k for k, (_, created) in items.items() if created < cutoff]:
        items.pop(key, None)


def _save_verifier(sid: str, verifier: str) -> None:
    store = _verifier_store()
    with store["lock"]:
        _purge_expired(store["items"])
        store["items"][sid] = (verifier, time.time())


def _pop_verifier(sid: str):
    if not sid:
        return None
    store = _verifier_store()
    with store["lock"]:
        _purge_expired(store["items"])
        item = store["items"].pop(sid, None)
    return item[0] if item else None


def build_google_url() -> str:
    sid = uuid.uuid4().hex
    verifier = secrets.token_urlsafe(64)  # 86 chars, within PKCE's 43-128 limit
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )
    _save_verifier(sid, verifier)
    return f"{SUPABASE_URL}/auth/v1/authorize?" + urlencode(
        {
            "provider": "google",
            # Trailing slash before "?" so the "/**" Redirect URL pattern in Supabase matches
            "redirect_to": f"{APP_URL}/?sid={sid}",
            "code_challenge": challenge,
            "code_challenge_method": "s256",
        }
    )


def _store_login(auth_response) -> None:
    st.session_state["logged_in"] = True
    st.session_state["user"] = auth_response.user
    st.session_state["supabase_session"] = auth_response.session


# ============================================================
# PROCESS OAUTH CALLBACK (?code=...&sid=...) OR ?error=...
# ============================================================

callback_error = None
params = st.query_params

if "code" in params:
    code = params.get("code", "")
    verifier = _pop_verifier(params.get("sid", ""))
    st.query_params.clear()  # never re-submit the same one-time code

    if not verifier:
        callback_error = "That Google sign-in link expired or was already used. Please try again."
    else:
        try:
            auth_response = supabase.auth.exchange_code_for_session(
                {"auth_code": code, "code_verifier": verifier}
            )
            if auth_response and auth_response.session:
                _store_login(auth_response)
            else:
                callback_error = "Google sign-in did not return a session. Please try again."
        except Exception as err:
            callback_error = f"Google sign-in failed: {err}"

elif "error" in params:
    callback_error = params.get("error_description") or params.get("error")
    st.query_params.clear()

# Already logged in (or just finished the OAuth callback): go to the dashboard.
# switch_page is called outside any try/except on purpose.
if st.session_state["logged_in"]:
    st.switch_page(DASHBOARD_PAGE)

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

/* ---- Form fields: readable in both light and dark browser modes ---- */
[data-testid="stWidgetLabel"] p {
    color: #17201C !important;
    font-weight: 600;
}

[data-testid="stTextInput"] div[data-baseweb="input"],
[data-testid="stTextInput"] div[data-baseweb="base-input"] {
    background-color: #FFFFFF !important;
    border-radius: 10px !important;
}

[data-testid="stTextInput"] div[data-baseweb="input"] {
    border: 1px solid #D1D5DB !important;
}

[data-testid="stTextInput"] input {
    background-color: #FFFFFF !important;
    color: #17201C !important;
    -webkit-text-fill-color: #17201C !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: #9AA29E !important;
    -webkit-text-fill-color: #9AA29E !important;
}

[data-testid="stTextInput"] button {
    color: #66706B !important;
}

[data-testid="stForm"] {
    background: transparent !important;
    border: 0 !important;
    padding: 0 !important;
}

/* ---- Google button (white, outlined) ---- */
.st-key-google_wrap a {
    background-color: #FFFFFF !important;
    border: 1px solid #D1D5DB !important;
    border-radius: 12px !important;
    min-height: 48px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05) !important;
    text-decoration: none !important;
}

.st-key-google_wrap a,
.st-key-google_wrap a * {
    color: #17201C !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}

.st-key-google_wrap a:hover {
    background-color: #F9FAFB !important;
    border-color: #9CA3AF !important;
}

/* ---- Email sign-in button (solid green) ---- */
[data-testid="stFormSubmitButton"] button {
    background: #0B3D2E !important;
    border: 0 !important;
    border-radius: 12px !important;
    min-height: 48px !important;
    width: 100% !important;
}

[data-testid="stFormSubmitButton"] button,
[data-testid="stFormSubmitButton"] button * {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
}

[data-testid="stFormSubmitButton"] button:hover {
    background: #145A43 !important;
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

if callback_error:
    st.error(callback_error)

# ---- Google ----
# Build the link once per browser session. If you add a logout button, delete
# st.session_state["google_url"] there so the next login gets a fresh link.
if "google_url" not in st.session_state:
    st.session_state["google_url"] = build_google_url()

with st.container(key="google_wrap"):
    st.link_button(
        "Continue with Google",
        st.session_state["google_url"],
        use_container_width=True,
    )

st.markdown('<div class="divider-text">OR EMAIL LOGIN</div>', unsafe_allow_html=True)

# ---- Email / password ----
login_ok = False

with st.form("login_form", clear_on_submit=False):
    email = st.text_input("Email Address", placeholder="player@example.com")
    password = st.text_input("Password", type="password", placeholder="••••••••")
    submit = st.form_submit_button("Sign In with Email", use_container_width=True)

if submit:
    if not email or not password:
        st.warning("Please enter both your email and password.")
    else:
        try:
            response = supabase.auth.sign_in_with_password(
                {"email": email.strip(), "password": password}
            )
            if response and response.session and response.user:
                _store_login(response)
                login_ok = True
            else:
                st.error("Sign-in failed. Check your email and password.")
        except Exception as err:
            message = str(err)
            if "invalid login credentials" in message.lower():
                st.error("Invalid email or password.")
            elif "email not confirmed" in message.lower():
                st.error("Please confirm your email first. Check your inbox for the confirmation link.")
            else:
                st.error(f"Login failed: {message}")

# switch_page outside the try/except so Streamlit's internal control-flow exception isn't swallowed
if login_ok:
    st.switch_page(DASHBOARD_PAGE)

