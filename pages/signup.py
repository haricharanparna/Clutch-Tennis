import streamlit as st
import re
from supabase import create_client

st.set_page_config(
    page_title="Clutch Tennis | Sign Up",
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
st.header("Create Your Account")

st.write("Sign up to get started.")

# Signup form
# Pressing Enter inside the form will submit it
with st.form("signup_form"):

    nameinput = st.text_input(
        "Enter Your Full Name"
    )

    emailinput = st.text_input(
        "Enter Your Email"
    )

    passwordinput = st.text_input(
        "Enter Your Password",
        type="password"
    )

    confirmpassword = st.text_input(
        "Confirm Password",
        type="password"
    )

    # Works when clicking Create Account or pressing Enter
    createacc = st.form_submit_button(
        "Create Account",
        use_container_width=True
    )

# Back to Login button
login_button = st.button(
    "Back to Login",
    use_container_width=True
)

# Send the user back to Login
if login_button:
    st.switch_page("pages/login.py")

# Create the account
if createacc:

    # Make sure all fields are filled out
    if (
        not nameinput
        or not emailinput
        or not passwordinput
        or not confirmpassword
    ):
        st.error("Please fill out all fields.")

    # Check if the email has a valid format
    elif not re.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        emailinput
    ):
        st.error("Please enter a valid email address.")

    # Check that the passwords match
    elif passwordinput != confirmpassword:
        st.error("Passwords do not match.")

    # Check password length
    elif len(passwordinput) < 6:
        st.error("Password must be at least 6 characters.")

    else:

        try:
            # Create the account in Supabase
            data = supabase.auth.sign_up({
                "email": emailinput,
                "password": passwordinput,
                "options": {
                    "data": {
                        "full_name": nameinput
                    }
                }
            })

            # Check if the account was created
            if data.user:

                st.success(
                    "Account created successfully! 🎾"
                )

                st.info(
                    "You can now log in with your email and password."
                )

                st.switch_page("pages/login.py")

            else:
                st.error(
                    "Account could not be created."
                )

        except Exception as e:
            st.error(
                "Something went wrong. Please try again."
            )
