import pytz

from datetime import datetime
from unittest import TestCase

from gmail_cli.db_helper import EmailDBHelper
from gmail_cli.settings import TIME_ZONE
from gmail_cli.exceptions import DoesNotExist


class TestDBHelper(TestCase):
    def setUp(self) -> None:
        self.db_helper = EmailDBHelper("test.db", "emails")

    def test_db_instance(self):
        self.assertIsNotNone(self.db_helper.get_db_instance())

    def test_create_table(self):
        table_structure = [
            (0, 'message_id', 'TEXT', 0, None, 1),
            (1, 'subject', 'TEXT', 0, None, 0),
            (2, 'snippet', 'TEXT', 0, None, 0),
            (3, 'date', 'TEXT', 0, None, 0),
            (4, 'recipient', 'TEXT', 0, None, 0),
            (5, 'sender', 'TEXT', 0, None, 0)
        ]
        self.assertEqual(self.db_helper.create_emails_table(), table_structure)

    def test_insert_emails(self):
        self.db_helper.create_emails_table(remove_existing=True)
        emails_1 = [
            {
                'message_id': '1',
                'subject': 'Test Subject',
                'snippet': 'Test Snippet',
                'date': '2021-07-01',
                'to': 'Maria <maria@maria.com>',
                'from': 'leo@mv3@gmail.com'
            }
        ]
        self.assertRaises(
            Exception, self.db_helper.insert_emails_into_table, emails_1)
        emails_2 = [
            {
                'message_id': '1',
                'subject': 'Test Subject',
                'snippet': 'Test Snippet',
                'date': 'Thu, 01 Jul 2021 00:00:00 +0000',
                'to': 'Maria <maria@maria.com>',
                'from': 'leo@mv3@gmail.com'
            }
        ]
        self.db_helper.insert_emails_into_table(emails_2)
        emails = self.db_helper.fetch_emails_from_table()
        expected_emails_data = [
            {
                'message_id': '1',
                'subject': 'Test Subject',
                'snippet': 'Test Snippet',
                'date': datetime.strptime(
                    "Thu, 01 Jul 2021 00:00:00 +0000",
                    "%a, %d %b %Y %H:%M:%S %z"
                ).astimezone(pytz.timezone(TIME_ZONE)),
                'to': 'Maria <maria@maria.com>',
                'from': 'leo@mv3@gmail.com'
            }
        ]
        self.assertListEqual(emails, expected_emails_data)

    def test_fetch_email(self):
        self.db_helper.create_emails_table(remove_existing=True)
        emails = self.db_helper.fetch_emails_from_table()
        self.assertEqual(emails, [])
        emails = [
            {
                'message_id': '1',
                'subject': 'Test Subject',
                'snippet': 'Test Snippet',
                'date': 'Thu, 01 Jul 2021 00:00:00 +0000',
                'to': 'Maria <maria@maria.com>',
                'from': 'leo@mv3@gmail.com'
            }
        ]
        self.db_helper.insert_emails_into_table(emails)
        email_1 = self.db_helper.fetch_email_by_id('1')
        expected_email_1 = {
            'message_id': '1',
            'subject': 'Test Subject',
            'snippet': 'Test Snippet',
            'date': datetime.strptime(
                "Thu, 01 Jul 2021 00:00:00 +0000",
                "%a, %d %b %Y %H:%M:%S %z"
            ).astimezone(pytz.timezone(TIME_ZONE)),
            'to': 'Maria <maria@maria.com>',
            'from': 'leo@mv3@gmail.com'
        }
        self.assertDictEqual(email_1, expected_email_1)
        self.assertRaises(DoesNotExist, self.db_helper.fetch_email_by_id, '2')
