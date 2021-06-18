from flask_login import LoginManager, login_user
from flask import redirect
import requests
from TodoUser import TodoUser
from oauthlib.oauth2 import WebApplicationClient
import random, string
import os

OAUTH_ID = os.environ.get('OAUTH_ID')
OAUTH_SECRET = os.environ.get('OAUTH_SECRET')
SECRET_KEY = os.environ.get('secret_key')


def init_auth(app):
    login_mgr = LoginManager()

    app.secret_key = SECRET_KEY

    @login_mgr.unauthorized_handler
    def unauthorised():
        state = ''.join(random.choices(string.ascii_lowercase, k=16))
        auth_client = WebApplicationClient(OAUTH_ID)
        auth_uri = auth_client.prepare_request_uri(
            'https://github.com/login/oauth/authorize',
            state=state
        )
        return redirect(auth_uri)

    @login_mgr.user_loader
    def load_user(user_id):
        return TodoUser(user_id)

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
    return token_params['access_token']


def github_login(code, state):
    access_token = get_access_token(code, state)
    user_request_headers = {'Authorization': 'bearer ' + access_token}
    user_id = requests.get('https://api.github.com/user', headers=user_request_headers).json()['id']
    user = TodoUser(user_id)
    login_user(user)
