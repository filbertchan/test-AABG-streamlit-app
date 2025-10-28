import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import requests
import base64
from urllib.parse import urlencode

st.set_page_config(page_title="Prompt Squad Uploader", page_icon="🚀")

st.title("🚀 Prompt Squad Document Uploader")
st.subheader("Direct upload to S3")

# ----------------------
# Cognito login setup
# ----------------------
COGNITO_DOMAIN = "https://us-east-1qitbxlp6m.auth.us-east-1.amazoncognito.com"
CLIENT_ID = st.secrets["APP_CLIENT_ID"]
CLIENT_SECRET = st.secrets["APP_CLIENT_SECRET"]
REDIRECT_URI = "https://test-aabg-app-app-ubaxx4rffpfjc96ed39swa.streamlit.app/upload"
TOKEN_URL = f"{COGNITO_DOMAIN}/oauth2/token"

# Encode client_id:client_secret for Basic Auth
auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

# Construct LOGIN_URL
login_params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "scope": "email openid",
    "redirect_uri": REDIRECT_URI
}
LOGIN_URL = f"{COGNITO_DOMAIN}/login/continue?{urlencode(login_params)}"

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "id_token" not in st.session_state:
    st.session_state.id_token = None

# ----------------------
# Handle Cognito redirect with code
# ----------------------
code = st.query_params.get("code")
if code and not st.session_state.logged_in:
    code = code[0]  # extract the code string
    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {auth_header}"
    }
    try:
        response = requests.post(TOKEN_URL, data=data, headers=headers)
        if response.status_code != 200:
            st.error(f"❌ Login failed: {response.status_code} - {response.text}")
        else:
            tokens = response.json()
            st.session_state.logged_in = True
            st.session_state.id_token = tokens["id_token"]
            st.success("✅ Logged in successfully via Cognito!")
            st.experimental_set_query_params()  # remove ?code from URL
    except Exception as e:
        st.error(f"❌ Login failed: {e}")

# ----------------------
# Show login button if not logged in
# ----------------------
if not st.session_state.logged_in:
    st.warning("Please log in with Cognito to upload files.")
    # Option 1: clickable link styled as a button (works reliably on Streamlit Cloud)
    st.markdown(
        f'<a href="{LOGIN_URL}" target="_top" '
        'style="display:inline-block; padding:8px 16px; background-color:#4CAF50; color:white; '
        'text-decoration:none; border-radius:4px;">Login with Cognito</a>',
        unsafe_allow_html=True
    )
    st.stop()

# ----------------------
# AWS S3 upload
# ----------------------
AWS_ACCESS_KEY = st.secrets["AWS_ACCESS_KEY_ID"]
AWS_SECRET_KEY = st.secrets["AWS_SECRET_ACCESS_KEY"]
AWS_REGION = "us-east-1"   # change if needed
BUCKET_NAME = "aws-architect-agent-requirement"

s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

uploaded_file = st.file_uploader("Upload PDF, DOCX, or TXT file", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    st.info(f"📁 Selected: {uploaded_file.name}")
    if st.button("Upload to S3"):
        try:
            s3.upload_fileobj(uploaded_file, BUCKET_NAME, f"documents/{uploaded_file.name}")
            st.success("✅ File uploaded successfully to S3!")
        except NoCredentialsError:
            st.error("❌ AWS credentials not found.")
        except Exception as e:
            st.error(f"❌ Upload failed: {e}")

st.markdown("---")
