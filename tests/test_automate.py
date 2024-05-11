import pytz

from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import patch

from gmail_cli.automate import EmailAutomation
from gmail_cli.settings import TIME_ZONE


class TestAutomate(TestCase):
    def setUp(self):
        self.automate_1 = EmailAutomation(
            "samples/automate_1.json",
            db_path="test.db",
            table_name="emails"
        )

    def test_retrieve_emails(self):
        emails = self.automate_1.db_helper.create_emails_table(
            remove_existing=True)
        emails = self.automate_1.retrieve_emails()
        self.assertListEqual(emails, [])

    @patch("gmail_cli.automate.GmailClient.fetch_emails")
    def test_retrieve_emails_with_force(self, mock_fetch_emails):
        self.automate_1.db_helper.create_emails_table(remove_existing=True)
        mock_fetch_emails.return_value = [
            {
                'message_id': '1',
                'subject': 'Test Subject',
                'snippet': 'Test Snippet',
                'date': "Thu, 01 Jul 2021 00:00:00 +0000",
                'to': 'Maria <maria.maria.com>',
                'from': 'abc@abc.com'
            }
        ]

        emails = self.automate_1.retrieve_emails(force=True)
        expected_emails = [
            {
                'message_id': '1',
                'subject': 'Test Subject',
                'snippet': 'Test Snippet',
                'date': datetime.strptime(
                    'Thu, 01 Jul 2021 00:00:00 +0000',
                    "%a, %d %b %Y %H:%M:%S %z"
                ).astimezone(pytz.timezone(TIME_ZONE)),
                'to': 'Maria <maria.maria.com>',
                'from': 'abc@abc.com'
            }
        ]
        self.assertListEqual(emails, expected_emails)

    def test_match_string_type(self):
        field_value = 'abc'
        operator_value = 'eq'
        value = 'abc'
        self.assertTrue(self.automate_1.match_string_type(field_value, operator_value, value))

        field_value = 'abc'
        operator_value = 'eq'
        value = 'xyz'
        self.assertFalse(self.automate_1.match_string_type(field_value, operator_value, value))

        field_value = 'abc'
        operator_value = 'neq'
        value = 'xyz'
        self.assertTrue(self.automate_1.match_string_type(field_value, operator_value, value))

        field_value = 'abc'
        operator_value = 'neq'
        value = 'abc'
        self.assertFalse(self.automate_1.match_string_type(field_value, operator_value, value))

        field_value = 'abc'
        operator_value = 'contains'
        value = 'b'
        self.assertTrue(self.automate_1.match_string_type(field_value, operator_value, value))

        field_value = 'abc'
        operator_value = 'contains'
        value = 'x'
        self.assertFalse(self.automate_1.match_string_type(field_value, operator_value, value))

        field_value = 'abc'
        operator_value = 'ncontains'
        value = 'x'
        self.assertTrue(self.automate_1.match_string_type(field_value, operator_value, value))

        field_value = 'abc'
        operator_value = 'ncontains'
        value = 'b'
        self.assertFalse(self.automate_1.match_string_type(field_value, operator_value, value))

    def test_match_email_type(self):
        field_value = 'abc <abc@abc.com>'
        operator_value = 'eq'
        value = 'abc@abc.com'
        self.assertTrue(self.automate_1.match_email_type(field_value, operator_value, value))

        field_value = 'abc@abc.com'
        operator_value = 'eq'
        value = field_value
        self.assertTrue(self.automate_1.match_email_type(field_value, operator_value, value))

        field_value = 'abc@abc.com'
        operator_value = 'neq'
        value = field_value
        self.assertFalse(self.automate_1.match_email_type(field_value, operator_value, value))

        field_value = 'abc@abc.com'
        operator_value = 'contains'
        value = 'abc'
        self.assertTrue(self.automate_1.match_email_type(field_value, operator_value, value))

        field_value = 'abc@abc.com'
        operator_value = 'contains'
        value = 'xyz'
        self.assertFalse(self.automate_1.match_email_type(field_value, operator_value, value))

    def test_datetime_type(self):
        field_value = datetime.now().astimezone(pytz.timezone(TIME_ZONE))
        operator_value = 'lt'
        value = 2
        self.assertTrue(self.automate_1.match_datetime_type(field_value, operator_value, value))

        field_value = datetime.now().astimezone(pytz.timezone(TIME_ZONE)) - timedelta(days=1)  # Less than 2 days ago
        operator_value = 'lt'
        value = 2
        self.assertTrue(self.automate_1.match_datetime_type(field_value, operator_value, value))

        field_value = datetime.now().astimezone(pytz.timezone(TIME_ZONE)) + timedelta(days=1, hours=24)
        operator_value = 'lt'
        value = 2
        self.assertTrue(self.automate_1.match_datetime_type(field_value, operator_value, value))

        field_value = datetime.now().astimezone(pytz.timezone(TIME_ZONE))
        operator_value = 'gt'
        value = 2
        self.assertFalse(self.automate_1.match_datetime_type(field_value, operator_value, value))

        field_value = datetime.now().astimezone(pytz.timezone(TIME_ZONE)) - timedelta(days=3)
        operator_value = 'gt'
        value = 2
        self.assertTrue(self.automate_1.match_datetime_type(field_value, operator_value, value))

        field_value = datetime.now().astimezone(pytz.timezone(TIME_ZONE)) - timedelta(days=1)
        operator_value = 'gt'
        value = 2
        self.assertFalse(self.automate_1.match_datetime_type(field_value, operator_value, value))

        field_value = datetime.now().astimezone(pytz.timezone(TIME_ZONE))
        operator_value = 'eq'
        value = field_value.strftime("%d-%m-%Y")
        self.assertTrue(self.automate_1.match_datetime_type(field_value, operator_value, value))

        field_value = datetime.now().astimezone(pytz.timezone(TIME_ZONE))
        operator_value = 'eq'
        value = field_value.strftime("%d-%m-%Y %H:%M:%S")
        self.assertTrue(self.automate_1.match_datetime_type(field_value, operator_value, value))

        field_value = datetime.now().astimezone(pytz.timezone(TIME_ZONE))
        operator_value = 'neq'
        value = field_value.strftime("%d-%m-%Y")
        self.assertFalse(self.automate_1.match_datetime_type(field_value, operator_value, value))

        field_value = datetime.now().astimezone(pytz.timezone(TIME_ZONE))
        operator_value = 'neq'
        value = field_value.strftime("%d-%m-%Y %H:%M:%S")
        self.assertFalse(self.automate_1.match_datetime_type(field_value, operator_value, value))
