from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
config = {
  "apiKey": "AIzaSyDwdBIKm59pWBEFZZBe1Em0MtVjx9IcdT0",
  "authDomain": "wardabdotheg.firebaseapp.com",
  "projectId": "wardabdotheg",
  "storageBucket": "wardabdotheg.appspot.com",
  "messagingSenderId": "189554470673",
  "appId": "1:189554470673:web:1a6a781c9cfaa7f4c6e6b0",
  "measurementId": "G-Q74YRW35LR",
  "databaseURL":""
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
@app.route('/', methods=['GET', 'POST'])
def signup():
   Error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('signin'))
       except:
            Error = "Authentication failed"
   return render_template("signup.html",Error=Error)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
   Error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
       except:
            Error = "Authentication failed"
   return render_template("signin.html",Error=Error)




@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)