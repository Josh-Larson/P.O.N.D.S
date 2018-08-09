import flask
import flask_login
import UserAuth
from flask import request

app = flask.Flask(__name__, static_folder='web_files')

app.secret_key = b'_5#y2L"F4QJJajejsdJz\n\xec]/'
login_manager = flask_login.LoginManager()

login_manager.init_app(app)

unauth_user = UserAuth.User("admin", "passwordd")
print(unauth_user.is_authenticated())

@app.route('/<path:filename>')
def send_file(filename):
    return flask.send_from_directory(app.static_folder, filename)


@app.route('/login', methods=['POST'])
def authenticate():
    username = request.form.get('username')
    password = request.form.get('password')
    
    unauth_user = UserAuth.User(username, password)
    if unauth_user.is_authenticated():
        #Gets a cookie with remember=True sent to the User.
        flask_login.login_user(unauth_user, remember=True)
        return flask.redirect('/admin')
    else:
        return flask.abort(401)

@app.route('/admin')
@flask_login.login_required
def serveSecurePage():
    return 'Hello admin!'


#Required to manage multiple users.
@login_manager.user_loader
def load_user(id):
    return UserAuth.User.allUsers[id]
