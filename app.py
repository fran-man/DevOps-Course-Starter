from flask import Flask, render_template, request, redirect
from flask_login import login_required, current_user
from auth import init_auth, github_login
from ViewModel import TodoListViewModel
import board_utils
from MongoConnectionManager import MongoConnectionManager
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
        if user_can_write():
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
        if user_can_write():
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

    def user_can_write():
        return current_user_role_if_login_enabled() in ['writer','admin']

    def current_user_role_if_login_enabled():
        if app.config['LOGIN_DISABLED']:
            return "writer"
        else:
            return current_user.role


    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0')
