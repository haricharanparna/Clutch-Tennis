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

from coach_emails import get_coach_emails

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
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]  # must be the ANON key

# Defaults strictly to your production domain so OAuth callbacks match
_app_base = st.secrets.get("APP_URL", "https://clutchtennis.streamlit.app").rstrip("/")
if _app_base.endswith("/login"):
    _app_base = _app_base[:-6]
APP_URL = _app_base

LOGIN_URL = f"{APP_URL}/login"

PLAYER_DASHBOARD_PAGE = "pages/player_dashboard.py"
COACH_DASHBOARD_PAGE = "pages/coach_dashboard.py"

VERIFIER_TTL_SECONDS = 24 * 60 * 60  # 24 hours

# ============================================================
# SESSION STATE + SUPABASE CLIENT
# ============================================================

st.session_state.setdefault("logged_in", False)
st.session_state.setdefault("user", None)
st.session_state.setdefault("supabase_session", None)
st.session_state.setdefault("role", None)

if "supabase" not in st.session_state:
    st.session_state["supabase"] = create_client(SUPABASE_URL, SUPABASE_KEY)
supabase = st.session_state["supabase"]

# ============================================================
# ROLE ROUTING
# ============================================================


def resolve_role(user) -> str:
    """Return 'coach' or 'player'."""
    if not user:
        return "player"
    email = (getattr(user, "email", "") or "").strip().lower()
    metadata = getattr(user, "user_metadata", None) or {}

    coach_emails = get_coach_emails()
    if coach_emails:
        return "coach" if email in coach_emails else "player"
    return "coach" if metadata.get("role") == "coach" else "player"


def dashboard_for(role) -> str:
    return COACH_DASHBOARD_PAGE if role == "coach" else PLAYER_DASHBOARD_PAGE


def _store_login(auth_response) -> None:
    st.session_state["logged_in"] = True
    st.session_state["user"] = auth_response.user
    st.session_state["supabase_session"] = auth_response.session
    st.session_state["role"] = resolve_role(auth_response.user)


# Automatically switch if user is already logged in
if st.session_state.get("logged_in") and st.session_state.get("user"):
    role = st.session_state.get("role") or resolve_role(st.session_state.get("user"))
    st.session_state["role"] = role
    st.switch_page(dashboard_for(role))

# ============================================================
# PKCE HELPERS
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


def _get_verifier(sid: str):
    if not sid:
        return None
    store = _verifier_store()
    with store["lock"]:
        _purge_expired(store["items"])
        item = store["items"].get(sid)
    return item[0] if item else None


def build_google_url() -> str:
    sid = uuid.uuid4().hex
    verifier = secrets.token_urlsafe(64)
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )
    _save_verifier(sid, verifier)

    return f"{SUPABASE_URL}/auth/v1/authorize?" + urlencode(
        {
            "provider": "google",
            "redirect_to": LOGIN_URL,
            "state": sid,  # sid passed safely via state parameter
            "code_challenge": challenge,
            "code_challenge_method": "s256",
        }
    )


# ============================================================
# PROCESS OAUTH CALLBACK (?code=...&state=...) OR ?error=...
# ============================================================

callback_error = None
query_params = (
    st.query_params.to_dict()
    if hasattr(st.query_params, "to_dict")
    else dict(st.query_params)
)

if "code" in query_params:
    code = query_params.get("code")
    if isinstance(code, list):
        code = code[0]

    # Look up sid from state parameter (or fallback to sid)
    sid = query_params.get("state") or query_params.get("sid")
    if isinstance(sid, list):
        sid = sid[0]

    verifier = _get_verifier(sid)

    # Clear query parameters immediately
    st.query_params.clear()

    if not verifier:
        callback_error = "Google sign-in session expired or state lost. Please try again."
    else:
        try:
            auth_response = supabase.auth.exchange_code_for_session(
                {"auth_code": code, "code_verifier": verifier}
            )
            if auth_response and auth_response.session and auth_response.user:
                _store_login(auth_response)
                st.rerun()
            else:
                callback_error = "Google sign-in did not return a valid session. Please try again."
        except Exception as err:
            callback_error = f"Google sign-in failed: {err}"

elif "error" in query_params:
    err_desc = query_params.get("error_description") or query_params.get("error")
    if isinstance(err_desc, list):
        err_desc = err_desc[0]
    callback_error = err_desc
    st.query_params.clear()

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
            <div class="login-subtitle">Sign in to access your dashboard</div>
        </div>
    """),
    unsafe_allow_html=True,
)

if callback_error:
    st.error(callback_error)

# ---- Google ----
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
                st.error(
                    "Please confirm your email first. Check your inbox for the confirmation link."
                )
            else:
                st.error(f"Login failed: {message}")

if login_ok:
    st.switch_page(dashboard_for(st.session_state["role"]))
