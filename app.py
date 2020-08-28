from flask import Flask, render_template, request, redirect
import os
import session_items as session
import requests

app = Flask(__name__)
app.config.from_object('flask_config.Config')

TRELLO_KEY = os.environ.get('TRELLO_KEY')
TRELLO_TKN = os.environ.get('TRELLO_TKN')

TRELLO_BOARD = '5f48fa1737fa77134ffe1e17'
TRELLO_URL_BASE = 'https://api.trello.com/1/'


@app.route('/')
def index():
    params = {'key': TRELLO_KEY, 'token': TRELLO_TKN}
    full_list = requests.get(TRELLO_URL_BASE + 'boards/' + TRELLO_BOARD + '/cards', data=params).json()
    # print full_list
    return render_template('index.html', list=trimCardsList(full_list))


@app.route('/add-list-item', methods=['POST'])
def addListItem():
    print("Adding Item!")
    print('Title=' + request.form.get('textbox'))
    session.add_item(request.form.get('textbox'))
    return redirect("/")


@app.route('/completeditem', methods=['POST'])
def updateListItem():
    print("Updating Item!")
    print(request.form.get('id'))
    item_to_update = session.get_item(request.form.get('id'))
    print(item_to_update)
    item_to_update['status'] = 'Done!'
    session.save_item(item_to_update)
    return redirect("/")

def trimCardsList(list_of_cards):
    trimmed_result = []
    for card in list_of_cards:
        trimmed_result.append({
            'name': card['name'],
            'done': 'Complete!' if card['closed'] else 'Incomplete'
        })
    return trimmed_result

if __name__ == '__main__':
    app.run()
