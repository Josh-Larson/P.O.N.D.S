
import uuid, os

class User:

    allUsers = {}

    def __init__(self, username, password):
        self.unique_id = str(uuid.uuid4())
        self.username = username
        self.password = password
        print(os.environ['WEB_USER'])
        if self.is_authenticated():
            User.allUsers[self.unique_id] = self
    def is_authenticated(self):
        if self.username == os.environ['WEB_USER'] and self.password == os.environ['WEB_PASS']:
            return True
        else:
            return False

    def is_active():
        if self.is_authenticated():
            return True
        else:
            return False
    def is_anonymous():
        return False
    def get_id(self):
        return self.unique_id
