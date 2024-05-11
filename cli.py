from argparse import ArgumentParser

from gmail_cli.automate import EmailAutomation
from gmail_cli.db_helper import EmailDBHelper
from gmail_cli.api_client import GmailClient
from gmail_cli.utils import tabulate_emails, write_emails_to_csv


def main():
    parser = ArgumentParser(description='Automate gmail processing')
    subparsers = parser.add_subparsers(dest='command')

    list_parser = subparsers.add_parser(
        'list', help='List all the emails')
    list_parser.add_argument(
        '--db-path',
        type=str, default='', help='Path to the database file')
    list_parser.add_argument(
        '--table-name',
        type=str, default='', help='Name of the table in the database')
    list_parser.add_argument(
        '--credentials-file-path',
        type=str, help='Path to the credentials file')
    list_parser.add_argument(
        '--token-file-path',
        type=str, default='', help='Path to the token file')
    list_parser.add_argument(
        '--write-to-csv-path',
        type=str, default='', help='Path to write emails to a CSV file')
    list_parser.add_argument(
        '--force-retrieve',
        action='store_true', help='Force retrieve emails from Gmail')

    automate_parser = subparsers.add_parser(
        'automate', help='Automate email processing')
    automate_parser.add_argument(
        'schema', type=str, help='Path to the schema file')
    automate_parser.add_argument(
        '--db-path',
        type=str, default='', help='Path to the database file')
    automate_parser.add_argument(
        '--table-name',
        type=str, default='', help='Name of the table in the database')
    automate_parser.add_argument(
        '--credentials-file-path',
        type=str, default='', help='Path to the credentials file')
    automate_parser.add_argument(
        '--token-file-path',
        type=str, default='', help='Path to the token file')
    automate_parser.add_argument(
        '--force-retrieve',
        action='store_true', help='Force retrieve emails from Gmail')
    args = parser.parse_args()

    if args.command not in ['list', 'automate']:
        parser.print_help()
        return

    if args.command == 'list':
        email_db_helper = EmailDBHelper(args.db_path, args.table_name)
        if args.force_retrieve:
            gmail_client = GmailClient(
                args.credentials_file_path,
                args.token_file_path
            )
            emails = gmail_client.fetch_emails()
            email_db_helper.insert_emails_into_table(emails)

        emails = email_db_helper.fetch_emails_from_table()
        if args.write_to_csv_path:
            write_emails_to_csv(emails, args.write_to_csv_path)
        else:
            tabulate_emails(emails)
        return

    if args.command == 'automate':
        email_automation = EmailAutomation(
            args.schema,
            db_path=args.db_path,
            table_name=args.table_name,
            credentials_file_path=args.credentials_file_path,
            token_file_path=args.token_file_path
        )
        email_automation.run(force_retrieve=args.force_retrieve)
        print('Email automation rules applied successfully')
        return


if __name__ == "__main__":
    main()
