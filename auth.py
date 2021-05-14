from flask_login import LoginManager
from flask import redirect
import requests
from oauthlib.oauth2 import WebApplicationClient
import random, string
import os

OAUTH_ID = os.environ.get('OAUTH_ID')
OAUTH_SECRET = os.environ.get('OAUTH_SECRET')


def init_auth(app):
    login_mgr = LoginManager()

    @login_mgr.unauthorized_handler
    def unauthorised():
        state = ''.join(random.choices(string.ascii_lowercase, k=16))
        auth_client = WebApplicationClient(OAUTH_ID)
        auth_uri = auth_client.prepare_request_uri(
            'https://github.com/login/oauth/authorize',
            redirect_uri='http://127.0.0.1:5000/login/callback',
            state=state
        )
        return redirect(auth_uri)

    @login_mgr.user_loader
    def load_user(user_id):
        return None

    login_mgr.init_app(app)


def get_access_token(code, state):
    auth_client = WebApplicationClient(OAUTH_ID)
    token_request = auth_client.prepare_token_request(
        'https://github.com/login/oauth/access_token',
        client_id=OAUTH_ID,
        client_secret=OAUTH_SECRET,
        code=code,
        state=state
    )
    print(token_request)
    token_request[1]['Accept'] = 'application/json'
    access_token_response = requests.post(token_request[0], data=token_request[2], headers=token_request[1]).content
    token_params = auth_client.parse_request_body_response(access_token_response)
    access_token_string = token_params['access_token']

    user_request_headers = {'Authorization':'bearer ' + access_token_string}

    print(requests.get('https://api.github.com/user', headers=user_request_headers).json())

    return 'a'