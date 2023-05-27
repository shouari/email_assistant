# Email Assistant

The aim of the the project is to create a simple voice commande assistant to help manage Gmail Mailbox.

Initial features are :
- *Delete spam messages* 
- *Read titles of emails received*
- *At later stage, emaiu;'s reply suggestion will be implemented using ChatGPT*

The first step was to get hends on Gmail API, it is pretty well documented on Google website here: https://developers.google.com/gmail/api/quickstart/python

Then I created a speech to text and text to speech functions to communicate with the assistant.
I used for that pyttsx3 and speech_recognition libraries.