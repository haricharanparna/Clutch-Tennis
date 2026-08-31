import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="Clutch Tennis | Sign Up",
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
# SIGN UP PAGE
# -----------------------------
st.title("Clutch Tennis 🎾")
st.header("Create Your Account")

nameinput = st.text_input("Enter Your Full Name")

emailinput = st.text_input("Enter Your Email")

passwordinput = st.text_input(
    "Enter Your Password",
    type="password"
)

confirmpassword = st.text_input(
    "Confirm Password",
    type="password"
)

createacc = st.button(
    "Create Account",
    use_container_width=True
)

login_button = st.button(
    "Back to Login",
    use_container_width=True
)

# -----------------------------
# BACK TO LOGIN
# -----------------------------
if login_button:
    st.switch_page("pages/login.py")

# -----------------------------
# CREATE ACCOUNT
# -----------------------------
if createacc:

    if not nameinput or not emailinput or not passwordinput or not confirmpassword:
        st.error("Please fill out all fields.")

    elif passwordinput != confirmpassword:
        st.error("Passwords do not match.")

    elif len(passwordinput) < 6:
        st.error("Password must be at least 6 characters.")

    else:

        try:

            data = supabase.auth.sign_up({
                "email": emailinput,
                "password": passwordinput,
                "options": {
                    "data": {
                        "full_name": nameinput
                    }
                }
            })

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

        except Exception:
            st.error(
                "Something went wrong. Please try again."
            )
