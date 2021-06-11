from flask import Flask, render_template, request, redirect
from flask_login import login_required, current_user
from auth import init_auth, github_login
from ViewModel import TodoListViewModel
import board_utils
import pymongo
from bson.objectid import ObjectId
import datetime
import os


def create_app():
    app = Flask(__name__)
    if os.environ.get('LOGIN_DISABLED') is None or os.environ.get('LOGIN_DISABLED') != 'True':
        app.config['LOGIN_DISABLED'] = False
    else:
        app.config['LOGIN_DISABLED'] = True
    init_auth(app)

    mongo_manager = MongoConnectionManager()

    @app.route('/')
    @login_required
    def index():
        print('getting all cards!!!')
        full_list = get_all_cards()
        v_model = TodoListViewModel(board_utils.mapCardsToLocalRepresentation(full_list),
                                    current_user_role_if_login_enabled())
        return render_template('index.html', v_model=v_model)

    @app.route('/add-list-item', methods=['POST'])
    @login_required
    def addListItem():
        if current_user_role_if_login_enabled() == "writer":
            print("Adding Item!")
            card_title = request.form.get('new_card_textbox')
            card = {
                'name': card_title,
                'dateLastActivity': datetime.datetime.now().isoformat()
            }
            devops_database = mongo_manager.get_database()
            inserted_id = devops_database[board_utils.MONGO_LIST_TODO].insert_one(card).inserted_id
            print('Created card with ID: ' + str(inserted_id))
        else:
            print('User with role: ' + current_user_role_if_login_enabled() + ' does not have permission to add items')
        return redirect("/")

    @app.route('/completeditem', methods=['POST'])
    @login_required
    def updateListItem():
        if current_user_role_if_login_enabled() == "writer":
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
        else:
            print('User with role: ' + current_user_role_if_login_enabled() + ' does not have permission to update items')
        return redirect("/")

    @app.route('/login/callback', methods=['GET'])
    def login_callback():
        auth_code = request.args.get('code')
        auth_state = request.args.get('state')
        github_login(auth_code, auth_state)
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

    def current_user_role_if_login_enabled():
        print('Login Disabled: ' + str(app.config['LOGIN_DISABLED']))
        if app.config['LOGIN_DISABLED']:
            return "writer"
        else:
            return current_user.role


    return app


class MongoConnectionManager:
    MONGO_PASS = board_utils.MONGO_PASS
    MONGO_USER = board_utils.MONGO_USER

    mongo_client = None

    def get_database(self):
        if self.mongo_client is None:
            self.mongo_client = pymongo.MongoClient(
                "mongodb://"
                + self.MONGO_USER
                + ":" + self.MONGO_PASS
                + "@george-devops.mongo.cosmos.azure.com:10255/DefaultDatabase" +
                  "?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@george-devops@")
            # mongodb://george-devops:zhiuZ41nCgPHgwVSwQpmQcpnPKMCFpWooPGeXxKbWDsj4BWZZg5PzTIKUTYTP4Y9LOxnpBX6zK4cT5f1bA3QGg==@george-devops.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@george-devops@
        return self.mongo_client['DefaultDatabase']


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0')
