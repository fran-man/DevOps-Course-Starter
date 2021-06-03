from flask_login import UserMixin


class TodoUser(UserMixin):
    def __init__(self, github_id, role):
        self.id = github_id
        self.role = role
        print("User ID: " + str(github_id) + " has been assigned the role " + self.role)

    def to_mongo_format(self):
        return {'github_id': self.id, 'role': self.role}
