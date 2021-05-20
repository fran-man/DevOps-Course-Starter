from flask import Flask, render_template, request, redirect
from ViewModel import TodoListViewModel
import board_utils
import pymongo
from bson.objectid import ObjectId
import datetime


def create_app():
    app = Flask(__name__)

    mongo_manager = MongoConnectionManager()

    @app.route('/')
    def index():
        print('getting all cards!!!')
        full_list = get_all_cards()
        v_model = TodoListViewModel(board_utils.mapCardsToLocalRepresentation(full_list))
        return render_template('index.html', v_model=v_model)

    @app.route('/add-list-item', methods=['POST'])
    def addListItem():
        print("Adding Item!")
        card_title = request.form.get('new_card_textbox')
        card = {
            'name': card_title,
            'dateLastActivity': datetime.datetime.now().isoformat()
        }
        devops_database = mongo_manager.get_database()
        inserted_id = devops_database[board_utils.MONGO_LIST_TODO].insert_one(card).inserted_id
        print('Created card with ID: ' + str(inserted_id))
        return redirect("/")

    @app.route('/completeditem', methods=['POST'])
    def updateListItem():
        print('Updating Item!')
        print(request.form.get('id'))
        card_id = request.form.get('id')
        card_old_list = board_utils.MONGO_LIST_TODO

        devops_database = mongo_manager.get_database()

        completed_card = devops_database[board_utils.MONGO_LIST_TODO].find_one({'_id': ObjectId(card_id)})
        if completed_card is None:
            card_old_list = board_utils.MONGO_LIST_DOING
            completed_card = devops_database[board_utils.MONGO_LIST_DOING].find_one({'_id': ObjectId(card_id)})
            if completed_card is None:
                print('No card to update with ID: ' + card_id)
                return redirect("/")
        devops_database[card_old_list].delete_one({'_id': completed_card['_id']})
        devops_database[board_utils.MONGO_LIST_DONE].insert_one(completed_card)
        return redirect("/")

    def get_all_cards():
        devops_database = mongo_manager.get_database()
        to_do_items = devops_database['to_do'].find()
        doing_items = devops_database['doing'].find()
        done_items = devops_database['done_items'].find()
        return {
            board_utils.MONGO_LIST_TODO: to_do_items,
            board_utils.MONGO_LIST_DOING: doing_items,
            board_utils.MONGO_LIST_DONE: done_items
        }

    return app


class MongoConnectionManager:
    MONGO_PASS = board_utils.MONGO_PASS
    MONGO_USER = board_utils.MONGO_USER

    mongo_client = None

    def get_database(self):
        if self.mongo_client is None:
            self.mongo_client = pymongo.MongoClient(
                "mongodb+srv://" + self.MONGO_USER + ":" + self.MONGO_PASS + "@cluster0.wyf78.mongodb.net/DevopsEx?retryWrites=true&w=majority")
        return self.mongo_client['DevopsEx']


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0')
