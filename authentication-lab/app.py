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
  "databaseURL":"https://wardabdotheg-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'



@app.route('/', methods=['GET', 'POST'])
def signup():
   error = ""
   if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name= request.form['full_name']
        username= request.form['username']
        bio= request.form['bio']
       #try:
        login_session['user'] = auth.create_user_with_email_and_password(email, password)
        UID = login_session['user']['localId']
        account={"username":username,"password":password,"full_name":full_name,"email":email,"bio":bio}
        db.child('Users').child(UID).set(account)
        return redirect(url_for('signin'))
       #except:
            #error = "Authentication failed"
   return render_template("signup.html",error=error)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        full_name= request.form['full_name']
        username= request.form['username']
        bio= request.form['bio']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html",error=error)




@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    error = ""
    if request.method == 'POST':
        title= request.form['title']
        text = request.form['text']
        try:
            tweet={"title":title,"text":text}
            db.child('Tweets').push(tweet)
            return redirect(url_for('all_tweets'))
        except:
            error = "Authentication failed"
    return render_template("add_tweet.html", error = error)

@app.route('/all_tweets')
def all_tweets():
    tweets=db.child('Tweets').get().val()
    return render_template("all_tweets.html",tweets=tweets)

@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

if __name__ == '__main__':
    app.run(debug=True)