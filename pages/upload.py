import streamlit as st
import boto3
from botocore.exceptions import NoCredentialsError
import requests
import base64

st.set_page_config(page_title="Prompt Squad Uploader", page_icon="🚀")

st.title("🚀 Prompt Squad Document Uploader")
st.subheader("Direct upload to S3")

# ----------------------
# Cognito login setup
# ----------------------
COGNITO_DOMAIN = "https://us-east-1qitbxlp6m.auth.us-east-1.amazoncognito.com"
CLIENT_ID =  st.secrets["APP_CLIENT_ID"]
CLIENT_SECRET = st.secrets["APP_CLIENT_SECRET"]
REDIRECT_URI = "https://test-aabg-app-app-ubaxx4rffpfjc96ed39swa.streamlit.app/upload"
TOKEN_URL = f"{COGNITO_DOMAIN}/oauth2/token"

a = """LOGIN_URL = (
    f"{COGNITO_DOMAIN}/login?client_id={CLIENT_ID}"
    f"&response_type=code&scope=email+openid&redirect_uri={REDIRECT_URI}"
)"""

LOGIN_URL = "https://us-east-1qitbxlp6m.auth.us-east-1.amazoncognito.com/login/continue?client_id=45hcn8a97al4j4hmmdhgsgvtvf&redirect_uri=https%3A%2F%2Ftest-aabg-app-app-ubaxx4rffpfjc96ed39swa.streamlit.app%2Fupload&response_type=code&scope=email+openid"

auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

#LOGIN_URL = f"https://us-east-1qitbxlp6m.auth.us-east-1.amazoncognito.com/login/continue?client_id={CLIENT_ID}&redirect_uri=https%3A%2F%2Facn-solutions-architect-agent-webapp.streamlit.app%2Fupload&response_type=code&scope=email+openid+phone)%22%3E%27"

st.toast("initialize session_state")
# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "id_token" not in st.session_state:
    st.session_state.id_token = None

# Check if Cognito redirected back with a code
code = st.query_params.get("code")
st.toast("check session_state")
if code and not st.session_state.logged_in:
    st.toast("not logged in")
    code = code[0]  # Get the actual code string
    # Exchange code for tokens
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
    except Exception as e:
        st.error(f"❌ Login failed: {e}")

# Show login button if not logged in
st.toast("not logged in") 
if not st.session_state.logged_in:
    st.warning("Please log in with Cognito to upload files.")
    st.markdown(
        f'<a href="{LOGIN_URL}" target="_self">'
        '<button style="background-color:#4CAF50;color:white;padding:8px 16px;border:none;border-radius:4px;">'
        'Login with Cognito</button></a>',
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
