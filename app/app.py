from datetime import datetime
from twilio.rest import TwilioRestClient
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
app.config['SECRET_KEY'] = 'a_very_long_secret_key'
app.config['STORMPATH_API_KEY_FILE'] = 'apiKey.properties'
app.config['STORMPATH_APPLICATION'] = 'sweethapp'

stormpath_manager = StormpathManager(app)

#These are the handlers that respond to requests from web browsers
#In Flask handlers are written as Python functions
#Each handler is mapped to one or more request URLs

@app.route('/')
@app.route('/home')
def home():
	#user = {'name':'mpampis'}
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

			flash('Hello, you are now logged in.')
			return redirect(url_for('home'))

		except StormpathError, err:
			error = err.message

	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	logout_user()
	flash('You were logged out.')





@app.route("/submit-form/", methods = ['POST'])
def submit_number():
	#todo -> I should be able to set a custom SMS message
	#todo -> I should be able to set a different country code
	# Twilio AccountSID and AuthToken here
	client = TwilioRestClient (
						  "AC2c82991611b1d8e1f8275f3c9e5f1d4b",
						  "9e69ad7ffc914b39e5abf1417306c7a2"
							  )
	# Your Twilio number
	twilio_number = "+17472217045"


	number = request.form['number']
	# Switch to your country code of choice
	formatted_number = "+30" + number
	client.messages.create(
						to    =formatted_number,
						from_ = twilio_number,
						body  = "I  see u ..."
	)
	redirect("/form")
	#flash("Your message was sent! :]")
	#return redirect('/messages/')

#the function returns the responces of our friends to our SMSs
# and sends them to the messages.html page
@app.route("/messages/")
def list_messages():
	messages = client.messages.list(to=twilio_number)
	return render_template('messages.html', messages = messages)

if __name__ == '__main__':
	app.run( port = 5000, debug = app.config['DEBUG'] )
