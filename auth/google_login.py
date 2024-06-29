import os
import webbrowser
from requests_oauthlib import OAuth2Session

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # For testing only

class GoogleLogin:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = 'http://localhost:8080/'
        self.authorization_base_url = 'https://accounts.google.com/o/oauth2/auth'
        self.token_url = 'https://accounts.google.com/o/oauth2/token'
        self.scope = ["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]
        self.oauth = OAuth2Session(self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)

    def login(self):
        authorization_url, state = self.oauth.authorization_url(self.authorization_base_url, access_type="offline")
        webbrowser.open(authorization_url)
        redirect_response = input('Paste the full redirect URL here: ')
        self.oauth.fetch_token(self.token_url, client_secret=self.client_secret, authorization_response=redirect_response)

        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        response = self.oauth.get(userinfo_url)
        return response.json()
