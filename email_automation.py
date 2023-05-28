from __future__ import print_function
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


if not labels:
    print('No labels found.')
for i in labels:
        print(i['name'])


# Deleting messages

messages = search_messages(service, label= 'INBOX',
                           q="in: category:primary is:unread" )
print(len(messages))
# if len(messages) =g= 0:
#     speak("There are no spams")
# else:
#     speak("there are spams!!, we delete them")
#     delete_spam(service, label)





