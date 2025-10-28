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

# Create a link styled as a button that opens in the same tab
st.markdown(
    f'<a href="{cognito_url}" target="_self" style="text-decoration:none;">'
    f'<button style="padding:10px 20px; font-size:16px;">Login to Cognito</button></a>',
    unsafe_allow_html=True
)
