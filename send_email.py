from flask import Flask, render_template, request, redirect, flash
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import os, base64, random

app = Flask(__name__)
app.secret_key = 'secret'  # Needed for flash messages

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)

def create_message(sender, to, subject, body):
    message = MIMEText(body)
    message["to"] = to
    message["from"] = sender
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw}

def generate_otp():
    # Generate a random 6-digit OTP
    return str(random.randint(100000, 999999))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        to = request.form["to"]
        subject = "Your OTP Code"  # Set the subject directly in the code
        otp = generate_otp()
        body = f"Your OTP code is: {otp}"
        
        try:
            service = get_gmail_service()
            message = create_message("me", to, subject, body)
            service.users().messages().send(userId="me", body=message).execute()
            flash("OTP sent successfully!", "success")
        except Exception as e:
            flash(f"Failed to send OTP: {e}", "danger")
    return render_template("index.html")

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=8080, debug=True)
