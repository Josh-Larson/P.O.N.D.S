import flask
import flask_login
import UserAuth

app = flask.Flask(__name__)
app.secret_key = b'_5#y2L"F4QJJajejsdJz\n\xec]/'
login_manager = flask_login.LoginManager()

login_manager.init_app(app)

unauth_user = UserAuth.User("admin", "passwordd")
print(unauth_user.is_authenticated())


@app.route('/')
def authenticate():

    unauth_user = UserAuth.User("admin", "password")
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
