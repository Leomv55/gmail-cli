from os import environ

# Gmail API settings
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
]

# File paths
CREDENTIALS_FILE_PATH = environ.get("CREDENTIALS_FILE_PATH",
                                    "credentials.json")
TOKEN_FILE_PATH = environ.get("TOKEN_FILE_PATH", "token.json")

# Database settings
EMAILS_DB_PATH = environ.get("EMAILS_DB_PATH", "emails.db")
EMAIL_TABLE_NAME = environ.get("EMAIL_TABLE_NAME", "emails")
TIME_ZONE = environ.get("TIME_ZONE", "Asia/Kolkata")
