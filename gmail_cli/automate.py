import pytz
import re

from datetime import datetime, timedelta

from .db_helper import EmailDBHelper
from .api_client import GmailClient
from .validate import AutomationSchemaValidation
from .settings import TIME_ZONE


class EmailAutomation:
    '''
    Email automation class to automate the email processing.
    '''
    def __init__(
        self,
        schema_path,
        db_path='',
        table_name='',
        credentials_file_path='',
        token_file_path=''
    ) -> None:
        self.schema = AutomationSchemaValidation(schema_path)
        self.db_helper = EmailDBHelper(db_path, table_name)
        self.gmail_client = GmailClient(credentials_file_path, token_file_path)

    def retrieve_emails(self, force=False):
        '''
        Fetch emails from Gmail and insert them into the database.
        Args:
            force (bool): If True, fetch emails from Gmail and insert them
            into the database.
        '''
        if force:
            emails = self.gmail_client.fetch_emails()
            self.db_helper.insert_emails_into_table(emails)

        return self.db_helper.fetch_emails_from_table()

    def run(self, force_retrieve=False):
        '''
        Start the email automation process.
        Args:
            force_retrieve (bool): If True, fetch emails from Gmail and
            insert them into the database.
        '''
        rules = self.schema.validate()
        emails = self.retrieve_emails(force=force_retrieve)
        for rule in rules:
            self.apply_rule(rule, emails)

    def apply_rule(self, rule, emails):
        '''
        Apply the rule to the emails.
        '''
        conditions = rule['conditions']
        actions = rule['actions']
        predicate = rule['predicate']

        for email in emails:
            if self.match_conditions(email, conditions, predicate):
                self.perform_actions(email, actions)

    def match_conditions(self, email, conditions, predicate):
        '''
        Match the conditions with the email.
        '''
        if predicate == 'all':
            return self.match_all_conditions(email, conditions)
        elif predicate == 'any':
            return self.match_any_condition(email, conditions)
        else:
            raise ValueError('Invalid predicate')

    def match_all_conditions(self, email, conditions):
        '''
        Match all conditions with the email.
        '''
        for condition in conditions:
            if not self.match_condition(email, condition):
                return False
        return True

    def match_any_condition(self, email, conditions):
        '''
        Match any condition with the email.
        '''
        for condition in conditions:
            if self.match_condition(email, condition):
                return True
        return False

    def match_condition(self, email, condition):
        '''
        Match a single condition with the email.
        '''
        field = condition['field']
        value = condition['value']
        operator = condition['operator']
        field_value = email[field]

        if field in ('to', 'from'):
            return self.match_email_type(field_value, operator, value)
        elif field == 'subject':
            return self.match_string_type(field_value, operator, value)
        elif field == 'date_received':
            return self.match_datetime_type(field_value, operator, value)
        else:
            raise ValueError('Invalid field')

    def match_email_type(self, field_value, operator, value):
        '''
        Match to condition with the email.
        '''
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        match = re.search(pattern, field_value)
        if not match:
            return False

        email_address = match.group()
        return self.match_string_type(email_address, operator, value)

    def match_string_type(
        self,
        field_value: str,
        operator: str,
        value: str
    ) -> bool:
        '''
        Match string type condition with the email.
        '''
        if operator == 'eq':
            return field_value.strip() == value.strip()
        elif operator == 'neq':
            return field_value.strip() != value.strip()
        elif operator == 'contains':
            return value.strip() in field_value.strip()
        elif operator == 'ncontains':
            return value.strip() not in field_value.strip()
        else:
            raise ValueError('Invalid operator')

    def match_datetime_type(
        self,
        field_value: datetime,
        operator: str,
        value
    ) -> bool:
        '''
        Match datetime type condition with the email.
        '''
        server_timezone = pytz.timezone(TIME_ZONE)
        if operator == 'eq':
            try:
                dt_obj = datetime.strptime(value, "%d-%m-%Y")
            except ValueError:
                dt_obj = datetime.strptime(value, "%d-%m-%Y %H:%M:%S")
            return field_value.date() == dt_obj.date()
        elif operator == 'neq':
            try:
                dt_obj = datetime.strptime(value, "%d-%m-%Y")
            except ValueError:
                dt_obj = datetime.strptime(value, "%d-%m-%Y %H:%M:%S")
            return field_value.date() != dt_obj.date()
        elif operator == 'gt':  # Received more than 2 days ago
            request_date = (
                datetime.now().astimezone(server_timezone) -
                timedelta(days=value)
            )
            return field_value < request_date
        elif operator == 'lt':  # Received 2 days ago
            request_date = (
                datetime.now().astimezone(server_timezone) -
                timedelta(days=value)
            )
            return field_value >= request_date
        else:
            raise ValueError('Invalid operator')

    def perform_actions(self, email, actions):
        '''
        Perform actions on the email.
        '''
        for action in actions:
            self.perform_action(email, action)

    def perform_action(self, email, action):
        '''
        Perform a single action on the email.
        '''
        action_type = action['action']
        if action_type == 'mark_as_read':
            self.gmail_client.mark_as_read(email['message_id'])
        elif action_type == 'mark_as_unread':
            self.gmail_client.mark_as_unread(email['message_id'])
        elif action_type == 'move_to_mailbox':
            self.gmail_client.move_to_mailbox(
                email['message_id'], action['mailbox'])
        else:
            raise ValueError('Invalid action type')
