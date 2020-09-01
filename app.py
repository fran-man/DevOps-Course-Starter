from flask import Flask, render_template, request, redirect
import session_items as session
import requests
import trello_utils

app = Flask(__name__)
app.config.from_object('flask_config.Config')

TRELLO_KEY = trello_utils.TRELLO_KEY
TRELLO_TKN = trello_utils.TRELLO_TKN

TRELLO_BOARD = trello_utils.TRELLO_BOARD
TRELLO_URL_BASE = trello_utils.TRELLO_URL_BASE

DEFAULT_PARAMS = {'key': TRELLO_KEY, 'token': TRELLO_TKN}


@app.route('/')
def index():
    full_list = requests.get(TRELLO_URL_BASE + 'boards/' + TRELLO_BOARD + '/cards', data=DEFAULT_PARAMS).json()
    # print full_list
    return render_template('index.html', list=trello_utils.trimCardsList(full_list))


@app.route('/add-list-item', methods=['POST'])
def addListItem():
    print("Adding Item!")
    card_title = request.form.get('textbox')
    query_url = TRELLO_URL_BASE + 'cards'
    params = {'name': card_title, 'idList': trello_utils.TRELLO_TODO_LIST}
    params.update(DEFAULT_PARAMS)
    requests.post(query_url, data=params)
    return redirect("/")


@app.route('/completeditem', methods=['POST'])
def updateListItem():
    print("Updating Item!")
    print(request.form.get('id'))
    card_id = request.form.get('id')
    query_url = TRELLO_URL_BASE + 'cards/' + card_id
    params = {'idList': trello_utils.TRELLO_DONE_LIST}
    params.update(DEFAULT_PARAMS)
    requests.put(query_url, data=params)
    return redirect("/")

if __name__ == '__main__':
    app.run()
