from flask_login import LoginManager, login_user
from flask import redirect
import requests
from TodoUser import TodoUser
from oauthlib.oauth2 import WebApplicationClient
import random, string
from board_utils import MONGO_USER, MONGO_LIST_USERS
import os

from MongoConnectionManager import MongoConnectionManager

OAUTH_ID = os.environ.get('OAUTH_ID')
OAUTH_SECRET = os.environ.get('OAUTH_SECRET')
SECRET_KEY = os.environ.get('secret_key')


def init_auth(app):
    login_mgr = LoginManager()

    app.secret_key = SECRET_KEY

    mongo_manager = MongoConnectionManager()

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
        user_id_int = int(user_id)
        user = mongo_manager.get_database()[MONGO_LIST_USERS].find_one({'github_id': user_id_int})
        if user is None:
            return TodoUser(user_id_int, 'reader')
        else:
            return TodoUser(user_id_int, user['role'])

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


def github_login(code, state, mongo_manager):
    access_token = get_access_token(code, state)
    user_request_headers = {'Authorization': 'bearer ' + access_token}
    user_id = requests.get('https://api.github.com/user', headers=user_request_headers).json()['id']
    print('Loading user from the DB for id: ' + str(user_id))
    mongo_user = mongo_manager.get_database()[MONGO_LIST_USERS].find_one({'github_id': int(user_id)})
    if mongo_user is None:
        print('Creating a new user')
        user = TodoUser(int(user_id), 'reader')
        mongo_manager.get_database()[MONGO_LIST_USERS].insert_one(user.to_mongo_format())
    else:
        print('Building existing user from DB representation')
        user = TodoUser(mongo_user['github_id'], mongo_user['role'])
    login_user(user)
