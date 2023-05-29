from __future__ import print_function

import base64
import os.path

from base64 import urlsafe_b64decode

import html2text

from google_authenticate import gmail_authenticate

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




# Check if lable exists

results = service.users().labels().list(userId='me').execute()
labels = results.get('labels', [])


# if not labels:
#     print('No labels found.')
# for i in labels:
#         print(i['name'])


# Deleting messages

messages = search_messages(service, label= 'INBOX',
                           q="in: category:primary is:unread" )
for message in messages:
    msg =service.users().messages().get(userId='me',
                                        id=message['id']).execute()

    email_data = msg['payload']['headers']
    for values in email_data:
        name = values['name']
        if name.lower() == 'from':
            from_name = values['value']
            print(from_name)
        if name == 'Subject':
            subject = values['value']
            for part in msg['payload']['parts']:
                print(part)
                # try:
                mimeType = part['mimeType']
                data = part['body']["data"]
                byte_code = base64.urlsafe_b64decode(data)
                if mimeType == 'text/plain':
                    text = byte_code.decode()
                    print("This is the from name: " + from_name)
                    print("This is the message: " + str(text))
                elif mimeType == 'text/html':
                    text = html2text.html2text(byte_code)
                    print("This is htm")
                    print(from_name)
                    print(subject)
                    print(str(text))

                    # mark the message as read (optional)
                    # msg = service.users().messages().modify(userId='me', id=message['id'],
                    #                                         body={'removeLabelIds': ['UNREAD']}).execute()
                # except BaseException as error:
                #     pass

