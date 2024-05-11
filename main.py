from gmail_cli.automate import EmailAutomation


def main():
    automation = EmailAutomation(schema_path='automate.json')
    automation.run()


if __name__ == "__main__":
    main()
