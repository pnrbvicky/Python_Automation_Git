import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# URLs
DMS_URL = "http://127.0.0.1:5000"
#LOGIN_URL = f"{DMS_URL}/login"
LOGIN_URL = f"{DMS_URL}"

# Credentials (later load from env)
USERNAME = "admin"
PASSWORD = "admin"

# Paths
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# API
# MERLIN_API_URL = "https://merlin-api/upload"
MERLIN_API_URL = "http://127.0.0.1:6000/upload"

# Email
# SMTP_SERVER = "smtp.gmail.com"
# SMTP_PORT = 587
# EMAIL_FROM = "bot@company.com"
# EMAIL_TO = ["ops@company.com"]

#SMTP_SERVER = "smtp.gmail.com"
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587

SENDER_EMAIL = "pnrbvicky@yahoo.in"
APP_PASSWORD = ""   # Yahoo app password

RECIPIENTS = [
    "pnrbvicky@gmail.com"
]
