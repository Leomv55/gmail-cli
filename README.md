# Gmail CLI

This package provides a command-line interface (CLI) to automate processing emails in Gmail. It allows users to list all emails, apply automation rules to process emails, and perform various actions such as marking emails as read, moving emails to folders, and more.

## Installation

To install the package, you can use [Poetry](https://python-poetry.org/), a dependency management and packaging tool for Python.

First, clone the repository:

```bash
git clone https://github.com/your-username/gmail-cli.git
cd gmail-cli
```

Then, install the package using Poetry:

```bash
poetry install
poetry build
```
Newly built package will be available in the `dist` directory.

Finally, install the generated wheel file:
```bash
pip install dist/gmail_cli-0.1.0-py3-none-any.whl
```

## Usage
Once installed, you can use the command-line interface provided by this package to automate Gmail processing. The CLI provides two main commands: list and automate.

### List Command
The `list` command is used to list all the emails in the Gmail inbox.
    
```bash
gmailcli list [options]
```

#### Options:
- `--db-path`: Path to the database file.
- `--table-name`: Name of the table in the database.
- `--credentials-file-path`: Path to the credentials file.
- `--token-file-path`: Path to the token file.
- `--write-to-csv-path`: Path to write emails to a CSV file.
- `--force-retrieve`: Force retrieve emails from Gmail.

### Automate Command
The `automate` command is used to apply automation rules to process emails in the Gmail inbox.

```bash
gmailcli automate [schema] [options]
```
#### Environment Variables:
- `EMAILS_DB_PATH`: Path to the database file. default: `emails.db`
- `EMAIL_TABLE_NAME`: Name of the table in the database. default: `emails`
- `CREDENTIALS_FILE_PATH`: Path to the credentials file. default: `credentials.json`
- `TOKEN_FILE_PATH`: Path to the token file. default: `token.json`
- `TIME_ZONE` : Time zone to be used for the timestamps in the database. default: `Asia/Kolkata`

### Arguments:
- `schema`: Path to the schema file.
#### Options:
-`--db-path`: Path to the database file.
- `--table-name`: Name of the table in the database.
- `--credentials-file-path`: Path to the credentials file.
- `--token-file-path`: Path to the token file.
- `--force-retrieve`: Force retrieve emails from Gmail.

## Example
Here is an example of how to use the `gmailcli` package to list all emails in the Gmail inbox and apply automation rules to process emails.

### List Emails
To list all emails in the Gmail inbox, you can use the following command:

- Fetches emails from DB and displays them in the terminal.

```bash 
gmailcli list
```

- Fetches emails from Gmail and stores them in the DB. Also displays them in the terminal.

```bash
gmailcli list  --force-retrieve
```

```bash
gmailcli list --db-path my_database.db --table-name emails --credentials-file-path credentials.json --token-file-path token.json --write-to-csv-path emails.csv
```


### Automate Emails
To apply automation rules to process emails in the Gmail inbox, you can use the following command:

- Apply automation rules to process emails which are already in the DB.
```bash
gmailcli automate rules.json
```

- Apply automation rules to process emails which are fetched from Gmail.
```bash
gmailcli automate rules.json --db-path my_database.db --table-name emails --credentials-file-path credentials.json --token-file-path token.json --force-retrieve

```

The `rules.json` file contains the automation rules to be applied to the emails. The schema file should be in the following format:

```json
{
        "name": "Rule 1",
        "description": "Move all emails with subject containing 'your code always' to movies mailbox and mark as read",
        "predicate": "all",
        "conditions": [
            {
                "field": "subject",
                "operator": "contains",
                "value": "your code always"
            }
        ],
        "actions": [
            {
                "action": "mark_as_read"
            }
        ]
}
```
Example schema file: `samples/automate_1.json`

## Contributing
Contributions are welcome! Please feel free to submit any issues or pull requests.

## License
This project is licensed under the MIT License

