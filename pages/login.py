import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="Clutch Tennis | Login",
    page_icon="🎾"
)

# -----------------------------
# SUPABASE
# -----------------------------
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# -----------------------------
# ALREADY LOGGED IN?
# -----------------------------
if st.session_state.get("logged_in", False):
    st.switch_page("app.py")

# -----------------------------
# LOGIN PAGE
# -----------------------------
st.title("Clutch Tennis 🎾")
st.header("Welcome Back")

st.write("Log in to continue.")

emailinput = st.text_input("Enter Your Email")

passinput = st.text_input(
    "Enter Your Password",
    type="password"
)

loginbutton = st.button(
    "Login",
    use_container_width=True
)

signup_button = st.button(
    "Create an Account",
    use_container_width=True
)

# -----------------------------
# SIGN UP BUTTON
# -----------------------------
if signup_button:
    st.switch_page("pages/signup.py")

# -----------------------------
# LOGIN
# -----------------------------
if loginbutton:

    if not emailinput or not passinput:
        st.error("Please enter both your email and password.")

    else:

        try:
            data = supabase.auth.sign_in_with_password({
                "email": emailinput,
                "password": passinput
            })

            if data.user:

                # Save login status
                st.session_state["logged_in"] = True
                st.session_state["user"] = data.user

                st.success("Login successful! 🎾")

                st.switch_page("app.py")

            else:
                st.error("Login failed.")

        except Exception:
            st.error("Incorrect email or password.")
