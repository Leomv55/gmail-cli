from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


from settings import CREDENTIALS_FILE_PATH, TOKEN_FILE_PATH, GMAIL_SCOPES
from .exceptions import CredentialsFileNotFound


class GmailClient:
    def __init__(self, credential_file_path='', token_file_path=''):
        self.credential_file_path = (credential_file_path or
                                     CREDENTIALS_FILE_PATH)
        self.token_file_path = token_file_path or TOKEN_FILE_PATH

    def authenticate(self):
        '''
        Authenticate using OAuth2 and return Credentials object.
        '''
        credentials = None
        try:
            with open(self.credential_file_path, 'r') as token:
                credentials = Credentials.from_authorized_user_file(
                    self.token_file_path, GMAIL_SCOPES)
        except FileNotFoundError:
            pass

        if not credentials or not credentials.valid:
            if (
                credentials and
                credentials.expired and
                credentials.refresh_token
            ):
                credentials.refresh(Request())
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credential_file_path, GMAIL_SCOPES)
                    credentials = flow.run_local_server(port=0)
                except FileNotFoundError:
                    raise CredentialsFileNotFound(
                        'Credentials file not found.'
                        'Please provide a valid path to the credentials file.'
                    )

            with open(self.token_file_path, 'w') as token:
                token.write(credentials.to_json())

        return credentials

    def get_service(self):
        '''
        Create a Gmail service object.
        '''
        credentials = self.authenticate()
        return build('gmail', 'v1', credentials=credentials)

    def fetch_emails(self):
        '''
        Fetch the most recent emails from the user's Gmail inbox.
        '''
        service = self.get_service()

        try:
            response = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
            messages = response.get('messages', [])

            emails = []
            for message in messages:
                message_id = message['id']
                msg = service.users().messages().get(userId='me', id=message_id).execute()
                payload = msg['payload']
                headers = payload.get('headers', [])
                subject = next((header['value'] for header in headers if header['name'] == 'Subject'), None)
                date = next((header['value'] for header in headers if header['name'] == 'Date'), None)
                snippet = msg.get('snippet', '')

                email_info = {
                    'message_id': message_id,
                    'subject': subject,
                    'snippet': snippet,
                    'date': date,
                }
                emails.append(email_info)

            return emails

        except Exception as e:
            print(f'An error occurred while fetching emails: {str(e)}')
            return []
