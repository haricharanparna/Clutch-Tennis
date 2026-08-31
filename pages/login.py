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

# Login form
# Pressing Enter inside the form will submit it
with st.form("login_form"):

    emailinput = st.text_input(
        "Enter Your Email"
    )

    passinput = st.text_input(
        "Enter Your Password",
        type="password"
    )

    # Works when clicking Login or pressing Enter
    loginbutton = st.form_submit_button(
        "Login",
        use_container_width=True
    )

# Create account button
signup_button = st.button(
    "Create an Account",
    use_container_width=True
)

# Send the user to the signup page
if signup_button:
    st.switch_page("pages/signup.py")

# Check login information
if loginbutton:

    # Make sure both fields are filled out
    if not emailinput or not passinput:
        st.error(
            "Please enter both your email and password."
        )

    # Check if the email has a valid format
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

                # Save login status
                st.session_state["logged_in"] = True

                # Save user information
                st.session_state["user"] = data.user

                # Send user to the main app
                st.switch_page("app.py")

            else:
                st.error("Login failed.")

        except Exception:
            # Show an error if the email or password is incorrect
            st.error(
                "Incorrect email or password."
            )
