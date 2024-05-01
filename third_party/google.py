from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from rest_framework import serializers
from authentication.languages.en.authenticate import *


class Google:
    CLIENT_ID = settings.GOOGLE_AUTH_CLIENT_ID
    # CLIENT_ID = "236025958894-l05tha7iovc0ool81upch4i6gi91npe8.apps.googleusercontent.com"

    def login(self, token):
        # idinfo = id_token.verify_oauth2_token(token, requests.Request(), self.CLIENT_ID)
        # print(idinfo);
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(
                token, requests.Request(), self.CLIENT_ID)

            # print(idinfo)
            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            print(id)
            return idinfo['sub']
        except ValueError as e:
            print(e)
            raise serializers.ValidationError([e])
