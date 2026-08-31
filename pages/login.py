import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="Clutch Tennis | Login",
    page_icon="🎾"
)

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

if st.session_state.get("logged_in", False):
    st.switch_page("app.py")

st.title("Clutch Tennis 🎾")
st.header("Welcome Back")

st.write("Log in to continue.")

with st.form("login_form"):
    emailinput = st.text_input("Enter Your Email")

    passinput = st.text_input(
        "Enter Your Password",
        type="password"
    )

    loginbutton = st.form_submit_button(
        "Login",
        use_container_width=True
    )

signup_button = st.button(
    "Create an Account",
    use_container_width=True
)

if signup_button:
    st.switch_page("pages/signup.py")

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
                st.session_state["logged_in"] = True
                st.session_state["user"] = data.user

                st.switch_page("app.py")

            else:
                st.error("Login failed.")

        except Exception:
            st.error("Incorrect email or password.")
```
