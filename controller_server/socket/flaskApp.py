import flask, flask_login, UserAuth, os
from flask import request

app = flask.Flask(__name__, static_folder='web_files')

app.secret_key = b'_5#y2L"F4QJJajejsdJz\n\xec]/'
login_manager = flask_login.LoginManager()

login_manager.init_app(app)

@app.route('/')
def send_index():
    return flask.send_from_directory(app.static_folder, 'index.html')

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
    return flask.send_from_directory(app.static_folder, 'admin.html')

@app.route('/login')
def servePage():
    return flask.send_from_directory(app.static_folder, 'login.html')



@app.route('/js/<filename>')
def send_js(filename):
    return flask.send_from_directory(app.static_folder+'/js', filename)
@app.route('/css/<filename>')
def send_css(filename):
    return flask.send_from_directory(app.static_folder+'/css', filename)

@app.route('/img/<filename>')
def send_img(filename):
    return flask.send_from_directory(app.static_folder+'/img', filename)








#Required to manage multiple users.
@login_manager.user_loader
def load_user(id):
    return UserAuth.User.allUsers[id]

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=os.environ['HTTP_PORT'])


