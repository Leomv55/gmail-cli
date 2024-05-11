import csv
from tabulate import tabulate

def tabulate_emails(emails):
    '''
    Print the emails in a tabular format.
    '''
    if not emails:
        print('No emails found')
        return

    headers = emails[0].keys()
    rows = [list(email.values()) for email in emails]
    print(tabulate(rows, headers=headers, tablefmt='grid'))


def write_emails_to_csv(emails, file_path):
    '''
    Write the emails to a CSV file.
    '''
    headers = [
        'message_id',
        'subject',
        'snippet',
        'date',
        'from',
        'to'
    ]
    try:
        with open(file_path, 'w', newline='') as fp:
            csv_writer = csv.DictWriter(fp, fieldnames=headers)
            for email in emails:
                csv_writer.writerow(email)
            print(f'Emails written to {file_path}')

    except Exception as e:
        print(f'An error occurred while writing emails to CSV: {str(e)}')
