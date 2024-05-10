from gmail_cli.api_client import GmailClient


def main():
    client = GmailClient()
    client.fetch_emails()


if __name__ == "__main__":
    main()
