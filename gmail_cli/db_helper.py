import sqlite3

from settings import EMAILS_DB_PATH, EMAIL_TABLE_NAME

CREATE_EMAIL_TABLE = '''CREATE TABLE IF NOT EXISTS {email_table_name} (
    message_id TEXT PRIMARY KEY,
    subject TEXT,
    snippet TEXT,
    date TEXT
)'''

INSERT_EMAILS = '''INSERT OR IGNORE INTO {email_table_name} (
    message_id,
    subject,
    snippet,
    date
) VALUES (?, ?, ?, ?)'''

SELECT_EMAILS = '''SELECT * FROM {email_table_name}'''

EMAIL_QUERIES = {
    "CREATE_EMAIL_TABLE": CREATE_EMAIL_TABLE,
    "INSERT_EMAILS": INSERT_EMAILS,
    "SELECT_EMAILS": SELECT_EMAILS,
}


class EmailDBHelper:
    def __init__(self, db_path='', table_name='') -> None:
        self.db_path = db_path or EMAILS_DB_PATH
        self.table_name = table_name or EMAIL_TABLE_NAME

    def get_db_instance(self):
        return sqlite3.connect(self.db_path)

    def create_emails_table(self):
        conn = self.get_db_instance()
        cursor = conn.cursor()
        cursor.execute(EMAIL_QUERIES['CREATE_EMAIL_TABLE'].format(
            email_table_name=self.table_name))
        conn.commit()
        conn.close()

    def insert_emails_into_table(self, email_data):
        self.create_emails_table()
        conn = self.get_db_instance()
        cursor = conn.cursor()
        for email in email_data:
            cursor.execute(EMAIL_QUERIES['INSERT_EMAILS'].format(
                email_table_name=self.table_name), (
                email['message_id'],
                email['subject'],
                email['snippet'],
                email['date'])
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
        return emails
