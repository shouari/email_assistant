from __future__ import print_function
from voice import speak

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://mail.google.com/']
my_email = 'salim.houari@gmail.com'

def gmail_authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "google_credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('gmail', 'v1', credentials=creds)

    except HttpError as error:
        print(f'An error occured: {error}')

    return service
def search_messages(service, label, q=None):
    result = service.users().messages().list(userId='me',labelIds=label).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages


def delete_spam(service, label, q=None):
    messages_to_delete = search_messages(service, label)
    return service.users().messages().batchDelete(
        userId = 'me',
        body = {
            'ids': [msg['id'] for msg in messages_to_delete]
        }
    ).execute()

service = gmail_authenticate()
label='SPAM'

# Check if lable exists

# results = service.users().labels().list(userId='me').execute()
# labels = results.get('labels', [])
#
# if not labels:
#     print('No labels found.')
# for i in labels:
#     if i["name"] == label:
#         if input('Correct lable, do you want to to delete the content: Y/N? \n') == "Y":
#             delete_message(service, label)
#
#     else:
#         print("lable entered not found")


# Deleting messages

messages = search_messages(service, label)
if len(messages) == 0:
    speak("There are no spams")
else:
    speak("there are spams!!, we delete them")
    delete_spam(service, label)





