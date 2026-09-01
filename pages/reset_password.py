import streamlit as st
from supabase import create_client
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Clutch Tennis | Reset Password",
    page_icon="🎾"
)

# Connect to Supabase
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# Read the Supabase recovery tokens from the URL
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

        st.error(
            "Your password reset link is invalid or expired."
        )

# Page
st.title("Clutch Tennis 🎾")
st.header("Reset Your Password")

st.write("Enter your new password below.")

# Password fields
newpassword = st.text_input(
    "Enter Your New Password",
    type="password"
)

confirmpassword = st.text_input(
    "Confirm Your New Password",
    type="password"
)

resetbutton = st.button(
    "Reset Password",
    use_container_width=True
)

# Reset password
if resetbutton:

    if not st.session_state.get(
        "recovery_session",
        False
    ):

        st.error(
            "Your password reset session is invalid. "
            "Please request a new reset email."
        )

    elif not newpassword or not confirmpassword:

        st.error(
            "Please fill out both password fields."
        )

    elif newpassword != confirmpassword:

        st.error(
            "Passwords do not match."
        )

    elif len(newpassword) < 6:

        st.error(
            "Password must be at least 6 characters."
        )

    else:

        try:

            response = supabase.auth.update_user({
                "password": newpassword
            })

            if response.user:

                st.success(
                    "Password updated successfully! 🎾"
                )

                st.info(
                    "You can now log in with your new password."
                )

                st.switch_page(
                    "pages/login.py"
                )

            else:

                st.error(
                    "Password could not be updated."
                )

        except Exception:

            st.error(
                "Unable to reset your password. "
                "Please request a new reset email."
            )
