from datetime import datetime

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask.ext.stormpath import (
    StormpathError,
    StormpathManager,
    User,
    login_required,
    login_user,
    logout_user,
    user,
)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'hjdfhjdfhjdfhjdfhjdfhjdfhjdfhjdfhjdfgdjfj'
app.config['STORMPATH_API_KEY_FILE'] = 'apiKey.properties'
app.config['STORMPATH_APPLICATION'] = 'sweethapp'

stormpath_manager = StormpathManager(app)

@app.route('/')
def home():
  return render_template("home.html")

@app.route('/about')
def about():
  return render_template("about.html")

@app.route('/form')
def form():
  return render_template("form.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        try:
            _user = User.from_login(
                request.form['email'],
                request.form['password'],
            )
            login_user(_user, remember=True)
            flash('You were logged in.')

            return redirect(url_for('show_posts'))
        except StormpathError, err:
            error = err.message

    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out.')



if __name__ == '__main__':
    app.run( port = 5000, debug = app.config['DEBUG'] )
