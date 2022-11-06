from flask import Flask, render_template, Response, request, session, flash, redirect, url_for, abort, send_file, send_from_directory, jsonify
from firebase_admin import credentials, firestore, initialize_app

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'



# Initialize Firestore DB
cred = credentials.Certificate('D:\proj\key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('Logcred')

@app.route("/")
def index():
  return render_template('index.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
  # get form entries and add to databse
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    docs = db.collection('Logcred').where("Username", "==", username).get()
    if docs:
      flash('username already exists')
    else:
      db.collection('Logcred').add({'Username':username, 'Password':password})
      flash('account created')  
    
  return render_template('login.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
  # create session from login information
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    docs = db.collection('Logcred').where("Username", "==", username).get()
    if not docs:
      flash('invalid user or pass')
    else:
      for doc in docs:
        usdoc =  doc.to_dict()
      if usdoc["Username"] == username and usdoc["Password"] == password:
        session['username'] = usdoc["Username"]
        return redirect(url_for('index'))
      else:
        flash('invalid user or pass')  
    
  return render_template('login.html')


@app.route('/logout')
def logout():
  # remove the username from the session if it is there
  session.pop('username', None)
  return redirect(url_for('index'))
