# Email Assistant

The aim of the the project is to create a simple voice commande assistant to help manage Gmail Mailbox.

Initial features are :
- *Delete spam messages* 
- *Read titles of emails received*
- *At later stage, emaiu;'s reply suggestion will be implemented using ChatGPT*

The first step is to get hands on Gmail API, it is pretty well documented on Google website here: https://developers.google.com/gmail/api/quickstart/python

Then I created a speech to text and text to speech functions to communicate with the assistant.
I used for that pyttsx3 and speech_recognition libraries. Those are in the file *voice.py*

The next step is to create the functions that will handle reading emails.