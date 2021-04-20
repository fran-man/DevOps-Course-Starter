from flask import Flask, render_template, request, redirect
from ViewModel import TodoListViewModel
import trello_utils
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime


def create_app():
    app = Flask(__name__)

    MONGO_PASS = trello_utils.MONGO_PASS

    mongo_client = MongoClient("mongodb+srv://GEORGE_DEVOPS:" + MONGO_PASS +"@cluster0.wyf78.mongodb.net/DevopsEx?retryWrites=true&w=majority")
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
        card = {
            'name': card_title,
            'dateLastActivity': datetime.datetime.now().isoformat()
        }
        inserted_id = devops_database[trello_utils.MONGO_LIST_TODO].insert_one(card).inserted_id
        print('Created card with ID: ' + str(inserted_id))
        return redirect("/")

    @app.route('/completeditem', methods=['POST'])
    def updateListItem():
        print('Updating Item!')
        print(request.form.get('id'))
        card_id = request.form.get('id')
        card_old_list = trello_utils.MONGO_LIST_TODO
        completed_card = devops_database[trello_utils.MONGO_LIST_TODO].find_one({'_id': ObjectId(card_id)})
        if completed_card is None:
            card_old_list = trello_utils.MONGO_LIST_DOING
            completed_card = devops_database[trello_utils.MONGO_LIST_DOING].find_one({'_id': ObjectId(card_id)})
            if completed_card is None:
                print('No card to update with ID: ' + card_id)
                return redirect("/")
        devops_database[card_old_list].delete_one({'_id': completed_card['_id']})
        devops_database[trello_utils.MONGO_LIST_DONE].insert_one(completed_card)
        return redirect("/")

    def get_all_cards():
        to_do_items = devops_database['to_do'].find()
        doing_items = devops_database['doing'].find()
        done_items = devops_database['done_items'].find()
        return {
            trello_utils.MONGO_LIST_TODO: to_do_items,
            trello_utils.MONGO_LIST_DOING: doing_items,
            trello_utils.MONGO_LIST_DONE: done_items
        }

    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0')
