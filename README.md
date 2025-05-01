# OTP Service Integration

This repository provides a service to generate and send OTPs (One-Time Passwords) via email. Developers can integrate this service into their own applications to send OTPs to users. This service uses Gmail's API and Flask to handle requests.

## Features
- Generates random 6-digit OTPs.
- Sends OTPs via email using Gmail's API.
- Can be integrated easily into any web application.

## Requirements
- Python 3.x
- Flask
- Google API Client Libraries
- A Gmail account for sending OTPs
- A database to store OTPs and their expiration time (for validation)

## Installation & Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/tarakantaacharya/otp-service.git
cd otp-service
```

### Step 2: Install Dependencies

Make sure you have Python 3.x installed. Then install the required dependencies:

```bash
pip install -r requirements.txt
```

### Step 3: Setup Google API Credentials

To use Gmail's API, you'll need to set up OAuth 2.0 credentials.

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing project.
3. Enable the Gmail API for your project.
4. Create OAuth 2.0 credentials and download the `credentials.json` file.
5. Place the `credentials.json` file in the root of the project.

### Step 4: Setup Database

You'll need to set up a database to store the OTPs and their expiration times. Here's a simple example using SQLite (you can replace it with any database of your choice):

1. **Create the Database Schema**:
   
```sql
CREATE TABLE otps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    otp TEXT NOT NULL,
    expiration_time DATETIME NOT NULL
);
```

2. **Configure Database Connection**:
   Update the `send_email.py` file to connect to your database and store OTPs.

### Step 5: Run the Application

```bash
python send_email.py
```

By default, the service will run on `http://127.0.0.1:8080`. You can modify the host and port in the `send_email.py` file if needed.

### Step 6: Integrating into Your Website

In your web application, create a form where users can input their email address to receive an OTP. Once the email is submitted, your backend should call this OTP service to send the OTP.

Example of integration in Flask:

```python
import requests

@app.route("/send-otp", methods=["POST"])
def send_otp():
    email = request.form["email"]
    otp_service_url = "http://your-otp-service-url"
    response = requests.post(otp_service_url, data={"to": email})
    if response.status_code == 200:
        flash("OTP sent successfully!", "success")
    else:
        flash("Failed to send OTP", "danger")
    return redirect(url_for("index"))
```

### Step 7: Testing OTPs

1. After the OTP is sent to the user's email, store the OTP along with the expiration time in your database.
2. When the user enters the OTP, validate it by checking if it matches the stored OTP and if it is not expired.

### Step 8: Deploying

If you want to deploy this service on Google Cloud Run or any other cloud provider, follow the deployment steps.

For **Google Cloud Run**, make sure to:
- Build and push the Docker image.
- Deploy it using the `gcloud` command.

```bash
gcloud run deploy my-otp-app \
  --image gcr.io/your-project-id/my-otp-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

## `.gitignore`

Make sure sensitive files such as `credentials.json` and `token.json` are not pushed to GitHub by adding them to the `.gitignore` file.

```gitignore
credentials.json
token.json
*.pyc
*.log
.vscode/
.idea/
env/
```

## Troubleshooting

If you encounter issues:
- Ensure the correct permissions are set for Gmail API credentials.
- Check your Cloud Run service logs to view any errors.

[Cloud Run Logs](https://console.cloud.google.com/logs/viewer?project=your-project-id)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

### Notes for Developers:
- **OTP Expiry**: You should store OTPs with an expiration time (e.g., 5 minutes). This can be checked during OTP verification to ensure it’s still valid.
- **Database**: While SQLite is used for this example, you can replace it with any database of your choice like MySQL, PostgreSQL, or NoSQL databases.
