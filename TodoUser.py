from flask_login import UserMixin

writer_users = [3250652]


class TodoUser(UserMixin):
    def __init__(self, github_id):
        self.id = github_id
        if int(github_id) in writer_users:
            self.role = "writer"
        else:
            self.role = "reader"
        print("User ID: " + str(github_id) + " has been assigned the role " + self.role)
