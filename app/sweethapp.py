from flask import Flask , render_template , request, redirect
from twilio.rest import TwilioRestClient 

# Creating the Flask app
app = Flask(__name__)

# Paste in your AccountSID and AuthToken here
client = TwilioRestClient (
                      "AC2c82991611b1d8e1f8275f3c9e5f1d4b", 
                      "9e69ad7ffc914b39e5abf1417306c7a2"
                          ) 
# Your Twilio number
twilio_number = "+17472217045" 

# When you go to top page of app, this is what it will execute
@app.route("/") 
def main():
    return render_template('form.html')
  
@app.route("/submit-form/", methods = ['POST']) 
def submit_number():
    number = request.form['number']
    # Switch to your country code of choice
    formatted_number = "+30" + number 
    client.messages.create(
                        to    =formatted_number, 
                        from_ = twilio_number, 
                        body  = "I  see u ..."
    ) 
    return redirect('/messages/')
  
@app.route("/messages/")
def list_messages():
    messages = client.messages.list(to=twilio_number)
    return render_template('messages.html', messages = messages)
    
## If we're executing this app from the command line
#if __name__ == '__main__':
#    app.run("0.0.0.0", port = 3000, debug = True)
