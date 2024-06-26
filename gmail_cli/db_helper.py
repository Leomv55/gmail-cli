import sqlite3
import pytz

from datetime import datetime

from .settings import EMAILS_DB_PATH, EMAIL_TABLE_NAME, TIME_ZONE
from .exceptions import DoesNotExist

CREATE_EMAIL_TABLE = '''CREATE TABLE IF NOT EXISTS {email_table_name} (
    message_id TEXT PRIMARY KEY,
    subject TEXT,
    snippet TEXT,
    date TEXT,
    recipient TEXT,
    sender TEXT
)'''

INSERT_EMAILS = '''INSERT OR IGNORE INTO {email_table_name} (
    message_id,
    subject,
    snippet,
    date,
    recipient,
    sender
) VALUES (?, ?, ?, ?, ?, ?)'''

SELECT_EMAILS = '''SELECT * FROM {email_table_name}'''
SELECT_EMAILS_BY_ID = 'SELECT * FROM {email_table_name} WHERE message_id = ?'
DROP_EMAIL_TABLE = 'DROP TABLE IF EXISTS {email_table_name}'

EMAIL_QUERIES = {
    "CREATE_EMAIL_TABLE": CREATE_EMAIL_TABLE,
    "INSERT_EMAILS": INSERT_EMAILS,
    "SELECT_EMAILS": SELECT_EMAILS,
    "SELECT_EMAILS_BY_ID": SELECT_EMAILS_BY_ID,
    "DROP_EMAIL_TABLE": DROP_EMAIL_TABLE
}


class EmailDBHelper:
    ''''
    Email database helper class to interact
    with the SQLite database.
    '''
    def __init__(self, db_path='', table_name='') -> None:
        self.db_path = db_path or EMAILS_DB_PATH
        self.table_name = table_name or EMAIL_TABLE_NAME

    def get_db_instance(self):
        return sqlite3.connect(self.db_path)

    def create_emails_table(self, remove_existing=False):
        conn = self.get_db_instance()
        cursor = conn.cursor()

        if remove_existing:
            cursor.execute(EMAIL_QUERIES['DROP_EMAIL_TABLE'].format(
                email_table_name=self.table_name))
            conn.commit()

        cursor.execute(EMAIL_QUERIES['CREATE_EMAIL_TABLE'].format(
            email_table_name=self.table_name))
        conn.commit()

        # Fetch table structure
        cursor.execute("PRAGMA table_info({})".format(self.table_name))
        table_structure = cursor.fetchall()
        conn.close()
        return table_structure

    def _validate_date(self, date_str):
        date_str = date_str.split('(')[0].strip()
        if not date_str:
            raise ValueError('Invalid date')

        date_obj = datetime.strptime(
            date_str, "%a, %d %b %Y %H:%M:%S %z")
        return date_obj

    def insert_emails_into_table(self, email_data):
        self.create_emails_table()
        conn = self.get_db_instance()
        cursor = conn.cursor()
        for email in email_data:
            try:
                self._validate_date(email['date'])
            except ValueError:
                continue

            cursor.execute(EMAIL_QUERIES['INSERT_EMAILS'].format(
                email_table_name=self.table_name), (
                email['message_id'],
                email['subject'],
                email['snippet'],
                email['date'],
                email['to'],
                email['from'])
            )

        conn.commit()
        conn.close()

    def fetch_emails_from_table(self):
        conn = self.get_db_instance()
        cursor = conn.cursor()
        cursor.execute(EMAIL_QUERIES['SELECT_EMAILS'].format(
            email_table_name=self.table_name))
        emails = cursor.fetchall()
        conn.close()

        email_list = []
        for email in emails:
            date_str = email[3].split('(')[0].strip()
            if not date_str:
                continue

            try:
                server_timezone = pytz.timezone(TIME_ZONE)
                date_obj = datetime.strptime(
                    date_str, "%a, %d %b %Y %H:%M:%S %z")

                email_list.append({
                    "message_id": email[0],
                    "subject": email[1],
                    "snippet": email[2],
                    "date": date_obj.astimezone(server_timezone),
                    "to": email[4],
                    "from": email[5]
                })
            except ValueError:
                continue

        return email_list

    def fetch_email_by_id(self, message_id):
        '''
        Fetch an email by its message ID.
        '''
        conn = self.get_db_instance()
        cursor = conn.cursor()
        cursor.execute(EMAIL_QUERIES['SELECT_EMAILS_BY_ID'].format(
            email_table_name=self.table_name), (message_id,))
        email = cursor.fetchone()

        if not email:
            raise DoesNotExist(
                f'Email with pk {message_id} does not exist.')

        conn.close()

        date_obj = self._validate_date(email[3])
        return {
            "message_id": email[0],
            "subject": email[1],
            "snippet": email[2],
            "date": date_obj.astimezone(pytz.timezone(TIME_ZONE)),
            "to": email[4],
            "from": email[5]
        }
