from os import environ

GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]

CREDENTIALS_FILE_PATH = environ.get("CREDENTIALS_FILE_PATH",
                                    "credentials.json")
TOKEN_FILE_PATH = environ.get("TOKEN_FILE_PATH", "token.json")
