from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


from .settings import CREDENTIALS_FILE_PATH, TOKEN_FILE_PATH, GMAIL_SCOPES
from .exceptions import CredentialsFileNotFound


class GmailClient:
    '''
    A client to interact with the Gmail API.
    '''
    def __init__(self, credential_file_path='', token_file_path=''):
        self.credential_file_path = (
            credential_file_path or
            CREDENTIALS_FILE_PATH
        )
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
            response = service.users().messages().list(userId='me').execute()
            messages = response.get('messages', [])

            emails = []
            for message in messages:
                message_id = message['id']
                msg = service.users().messages().get(
                    userId='me',
                    id=message_id
                ).execute()
                payload = msg['payload']
                headers = payload.get('headers', [])
                subject = next(
                    (
                        header['value'] for header in headers
                        if header['name'] == 'Subject'
                    ), None)
                date = next(
                    (
                        header['value'] for header in headers
                        if header['name'] == 'Date'
                    ), None)
                sender = next(
                    (
                        header['value'] for header in headers
                        if header['name'] == 'From'
                    ), None)
                recipient = next(
                    (
                        header['value'] for header in headers
                        if header['name'] == 'To'
                    ), None)
                snippet = msg.get('snippet', '')

                email_info = {
                    'message_id': message_id,
                    'subject': subject,
                    'snippet': snippet,
                    'date': date,
                    'from': sender,
                    'to': recipient
                }
                emails.append(email_info)

            return emails

        except Exception as e:
            print(f'An error occurred while fetching emails: {str(e)}')
            print(e)
            return []

    def list_mailboxes(self):
        '''
        List all the mailboxes in the user's Gmail account.
        '''
        service = self.get_service()
        try:
            response = service.users().labels().list(userId='me').execute()
            labels = response.get('labels', [])
            return labels
        except Exception as e:
            print(f'An error occurred while listing mailboxes: {str(e)}')
            print(e)
            return []

    def mark_as_read(self, message_id):
        '''
        Mark an email as read.
        '''
        service = self.get_service()
        try:
            service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
        except Exception as e:
            print(f'An error occurred while marking email as read: {str(e)}')
            print(e)
            return False

        return True

    def mark_as_unread(self, message_id):
        '''
        Mark an email as unread.
        '''
        service = self.get_service()
        try:
            service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': ['UNREAD']}
            ).execute()
        except Exception as e:
            print(f'An error occurred while marking email as unread: {str(e)}')
            print(e)
            return False

        return True

    def move_to_mailbox(self, message_id, mailbox):
        '''
        Move an email to a specific mailbox.
        '''
        labels = self.list_mailboxes()
        for label in labels:
            if label['name'] == mailbox:
                mailbox_id = label['id']
                break
        else:
            raise ValueError(f'Mailbox "{mailbox}" not found')

        service = self.get_service()
        try:
            service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'addLabelIds': [mailbox_id]}
            ).execute()
        except Exception as e:
            print(f'An error occurred while moving email to mailbox: {str(e)}')
            print(e)
            return False

        return True
