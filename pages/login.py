import streamlit as st
import re
from supabase import create_client

st.set_page_config(
    page_title="Clutch Tennis | Login",
    page_icon="🎾"
)

# Connect to Supabase
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# If the user is already logged in, send them to the main app
if st.session_state.get("logged_in", False):
    st.switch_page("app.py")

st.title("Clutch Tennis 🎾")
st.header("Welcome Back")

st.write("Log in to continue.")

# Email input
# This is outside the form so Forgot Password can use it
emailinput = st.text_input(
    "Enter Your Email"
)

# Login form
with st.form("login_form"):

    passinput = st.text_input(
        "Enter Your Password",
        type="password"
    )

    # Works when clicking Login or pressing Enter
    loginbutton = st.form_submit_button(
        "Login",
        use_container_width=True
    )

# Forgot password button
forgotpassword = st.button(
    "Forgot Password?",
    use_container_width=True
)

# Create account button
signup_button = st.button(
    "Create an Account",
    use_container_width=True
)

# -----------------------------
# CREATE ACCOUNT
# -----------------------------
if signup_button:

    st.switch_page(
        "pages/signup.py"
    )

# -----------------------------
# FORGOT PASSWORD
# -----------------------------
if forgotpassword:

    if not emailinput:

        st.error(
            "Please enter your email address first."
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

            # Send password reset email
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
                "Password reset email sent! "
                "Check your inbox for the reset link."
            )

        except Exception:

            st.error(
                "Unable to send the password reset email. "
                "Please try again."
            )

# -----------------------------
# LOGIN
# -----------------------------
if loginbutton:

    if not emailinput or not passinput:

        st.error(
            "Please enter both your email and password."
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

            # Try to log the user into Supabase
            data = supabase.auth.sign_in_with_password({
                "email": emailinput,
                "password": passinput
            })

            # If login was successful
            if data.user:

                st.session_state["logged_in"] = True

                st.session_state["user"] = data.user

                st.switch_page(
                    "app.py"
                )

            else:

                st.error(
                    "Login failed."
                )

        except Exception:

            st.error(
                "Incorrect email or password."
            )
