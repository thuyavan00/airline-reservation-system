from flask import Flask, render_template, Response, request,  session, flash, redirect, url_for, abort, send_file, send_from_directory, jsonify
import requests, json
from firebase_admin import credentials, firestore, initialize_app
YOUR_ACCESS_KEY = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI0IiwianRpIjoiYjViOTNjMzcyMWY1MTg5MmQyMTkxYzYxZjAwODYyYTE1MmM4NWE1NjJkZjBjOThlNTQwYmMzOTFmYjc2NmZjODhhMWRmNmViOWI3ZGFjZjkiLCJpYXQiOjE2Njc1MzEwODcsIm5iZiI6MTY2NzUzMTA4NywiZXhwIjoxNjk5MDY3MDg3LCJzdWIiOiIxNzAxNCIsInNjb3BlcyI6W119.zPhkok_aNilgFZoSsz7IyVXJ4D97wq31_eHEKETlRmyGi0C9d5UXj49o6rtTW5ThX0vGeUwZy-CVv0CuUInREA"
#fliapi = "https://app.goflightlabs.com/flights?access_key="+YOUR_ACCESS_KEY+"&depIata=LGA"+"&araIata=YYZ"+"&departureDate=2022-11-07"
fliapi = "https://app.goflightlabs.com/search-all-flights?access_key="+YOUR_ACCESS_KEY+"&adults=1&origin=LGA&destination=YYZ&departureDate=2022-11-09"

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'



# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('Logcred')



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

@app.route('/', methods = ['GET', 'POST'])
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

@app.route('/flights')
def flights():
  data = requests.get(fliapi).json()
  data = data['data']['results']
  return data[0]