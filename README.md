Takes a sentence input and attempts to create a Spotify playlist with corresponding words.

SETUP:
- install dependencies from requirements.txt
- go to https://developer.spotify.com/dashboard and create an app
- in the Basic Information Tab
  - set Redirect URIs to http://127.0.0.1:5000/callback
  - in creds.py change client_id to the Client ID for your app
  - in creds.py change client_secret to the Client Secret for your app
- in the User Management Tab
  - add the email account(s) you will be using to User Management

RUNNING:
- run main.py

CONFIG:
- you can change FILLER_WORDS in word_manipulation.py
