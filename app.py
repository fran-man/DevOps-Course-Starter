from flask import Flask, render_template, request, redirect
from ViewModel import TodoListViewModel
import requests
import trello_utils
import pymongo


def create_app():
    app = Flask(__name__)

    TRELLO_BOARD = trello_utils.TRELLO_BOARD
    TRELLO_URL_BASE = trello_utils.TRELLO_URL_BASE

    DEFAULT_PARAMS = trello_utils.DEFAULT_PARAMS

    MONGO_PASS = trello_utils.MONGO_PASS

    all_lists = requests.get(TRELLO_URL_BASE + 'boards/' + TRELLO_BOARD + '/lists', data=DEFAULT_PARAMS).json()

    mongo_client = pymongo.MongoClient("mongodb+srv://GEORGE_DEVOPS:" + MONGO_PASS +"@cluster0.wyf78.mongodb.net/DevopsEx?retryWrites=true&w=majority")
    devops_database = mongo_client['DevopsEx']

    @app.route('/')
    def index():
        full_list = get_all_cards()
        v_model = TodoListViewModel(trello_utils.mapTrelloCardsToLocalRepresentation(full_list))
        return render_template('index.html', v_model=v_model)

    @app.route('/add-list-item', methods=['POST'])
    def addListItem():
        print("Adding Item!")
        card_title = request.form.get('new_card_textbox')
        query_url = TRELLO_URL_BASE + 'cards'
        params = {'name': card_title, 'idList': get_todo_list_id()}
        params.update(DEFAULT_PARAMS)
        requests.post(query_url, data=params).json()
        return redirect("/")

    @app.route('/completeditem', methods=['POST'])
    def updateListItem():
        print("Updating Item!")
        print(request.form.get('id'))
        card_id = request.form.get('id')
        query_url = TRELLO_URL_BASE + 'cards/' + card_id
        params = {'idList': get_done_list_id()}
        params.update(DEFAULT_PARAMS)
        requests.put(query_url, data=params)
        return redirect("/")

    def get_todo_list_id():
        for trello_list in all_lists:
            if trello_list['name'] == 'Things To Do':
                return trello_list['id']

    def get_done_list_id():
        for trello_list in all_lists:
            if trello_list['name'] == 'Done':
                return trello_list['id']

    def get_all_cards():
        to_do_items = devops_database['to_do'].find()
        doing_items = devops_database['doing'].find()
        done_items = devops_database['done'].find()
        return {
            trello_utils.MONGO_LIST_TODO: to_do_items,
            trello_utils.MONGO_LIST_DOING: doing_items,
            trello_utils.MONGO_LIST_DONE: done_items
        }

    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0')
