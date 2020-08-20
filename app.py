from flask import Flask, render_template, request, redirect, url_for
import session_items as session

app = Flask(__name__)
app.config.from_object('flask_config.Config')

@app.route('/')
def index():
    full_list = session.get_items()
    return render_template('index.html', list=full_list)

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

if __name__ == '__main__':
    app.run()
