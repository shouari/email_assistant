from __future__ import print_function

import os

from base64 import urlsafe_b64decode

from google_authenticate import gmail_authenticate

import html2text

service = gmail_authenticate()

def search_messages(service, label, q=None):
    result = service.users().messages().list(userId='me',
                                             labelIds=label, includeSpamTrash=False
                                             , q=q).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',labelIds=label,
                                                 pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    return messages

def delete_spam(service, label, q=None):
    messages_to_delete = search_messages(service, label='SPAM')
    return service.users().messages().batchDelete(
        userId = 'me',
        body = {
            'ids': [msg['id'] for msg in messages_to_delete]
        }
    ).execute()

results = service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])


def parse_parts(service, parts, folder_name, message):
    """
    Utility function that parses the content of an email partition
    """
    if parts:
        for part in parts:
            filename = part.get("filename")
            mimeType = part.get("mimeType")
            body = part.get("body")
            data = body.get("data")
            file_size = body.get("size")
            part_headers = part.get("headers")
            if part.get("parts"):
                # recursively call this function when we see that a part
                # has parts inside
                parse_parts(service, part.get("parts"), folder_name, message)
            if mimeType == "text/plain":
                # if the email part is text plain
                if data:
                    text = urlsafe_b64decode(data).decode()

            elif mimeType == "text/html":
                # if the email part is an HTML content
                # convert HTML to TXT
                text = html2text.html2text(urlsafe_b64decode(data).decode())
                print("This is html")
                print(text)
            else:
                pass

def read_message(service, message):
    """
    This function takes Gmail API `service` and the given `message_id` and does the following:
        - Downloads the content of the email
        - Prints email basic information (To, From, Subject & Date) and plain/text parts
        - Creates a folder for each email based on the subject
        - Downloads text/html content (if available) and saves it under the folder created as index.html
        - Downloads any file that is attached to the email and saves it in the folder created
    """
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    # parts can be the message body, or attachments
    payload = msg['payload']
    headers = payload.get("headers")
    parts = payload.get("parts")
    folder_name = "email"
    has_subject = False
    if headers:
        # this section prints email basic info & creates a folder for the email
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                # we print the From address
                print("From:", value)
            if name.lower() == "to":
                # we print the To address
                print("To:", value)
            if name.lower() == "subject":
                # make our boolean True, the email has "subject"
                has_subject = True
                print("Subject:", value)
            if name.lower() == "date":
                # we print the date when the message was sent
                print("Date:", value)
    if not has_subject:
        pass
        # if the email does not have a subject, then make a folder with "email" name
        # since folders are created based on subjects
    parse_parts(service, parts, folder_name, message)
    print("="*50)
messages = search_messages(service, label= 'INBOX',
                           q="in: category:primary is:unread" )
for msg in messages:
    read_message(service, msg)
