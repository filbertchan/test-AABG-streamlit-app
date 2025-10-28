import streamlit as st

st.set_page_config(page_title="Prompt Squad Uploader", page_icon="🚀")
st.title("🚀 Prompt Squad Document Uploader")

cognito_url = (
    "https://us-east-1qitbxlp6m.auth.us-east-1.amazoncognito.com/login/continue"
    "?client_id=45hcn8a97al4j4hmmdhgsgvtvf"
    "&redirect_uri=https%3A%2F%2Ftest-aabg-app-app-ubaxx4rffpfjc96ed39swa.streamlit.app%2Fupload"
    "&response_type=code"
    "&scope=email+openid"
)

if st.button("Login to Cognito"):
    st.components.v1.html(f"""
        <script>
            window.location.href = "{cognito_url}";
        </script>
    """, height=0)
