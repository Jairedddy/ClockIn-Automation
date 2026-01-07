import os
import base64
from email.message import EmailMessage

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_gmail_service():
    creds = None
    
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
            
        with open("token.json", "w") as token:
            token.write(creds.to_json())
            
    return build("gmail", "v1", credentials = creds)


def send_email(subject, body, attachments=None):
    if attachments is None:
        attachments = []
        
    service = get_gmail_service()
    
    message = EmailMessage()
    message["To"] = "jaishukreddy7@gmail.com"
    message["Subject"] = subject
    message.set_content(body)
    
    for file_path in attachments:
        with open(file_path, "rb") as f:
            data = f.read()
            message.add_attachment(
                data,
                maintype="image",
                subtype="png",
                filename=os.path.basename(file_path),
            )
            
    encoded_message = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()
    
    service.users().messages().send(
        userId="me",
        body={"raw": encoded_message},
    ).execute()