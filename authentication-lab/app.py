from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

Config = {
  "apiKey": "AIzaSyCYWZwMd_HIoOTqsjAF9Il4t4NAycwDERM",
  "authDomain": "fir-11-d4c93.firebaseapp.com",
  "projectId": "fir-11-d4c93",
  "storageBucket": "fir-11-d4c93.appspot.com",
  "messagingSenderId": "948091112650",
  "appId": "1:948091112650:web:a1d07cb460fa473ef13833",
  "measurementId": "G-TSKSZFZR1T",
  "databaseURL":"https://fir-11-d4c93-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


#@app.route('/', methods=['GET', 'POST'])
#def signin():
  #  return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'],)
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user = {'name':request.form["name"],'email':request.form["email"],'username':request.form["username"],'password':request.form['password']}
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            db.child("user").child(login_session['user']['localId']).set(user)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
            return render_template("signup.html")
    return render_template("signup.html")


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
            return render_template("signin.html")
    return render_template("signin.html")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        print("banana")
        tweet = {'Title':request.form["Title"],'post':request.form["post"],"uid": login_session['user']['localId']}
        db.child("tweet").push(tweet)
    return render_template("add_tweet.html")

@app.route('/all_tweets')
def all_tweets():
    return render_template("tweets.html",tweet = db.child('tweet').get().val())




if __name__ == '__main__':
    app.run(debug=True)