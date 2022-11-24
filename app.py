from flask import Flask, render_template, Response, request,  session, flash, redirect, url_for, abort, send_file, send_from_directory, jsonify
import requests, json
from firebase_admin import credentials, firestore, initialize_app
from duffel_api import Duffel
from flask_mail import Mail, Message
from flask_session import Session

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY_SDA_PROJECT'

#Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#email
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'g.ajaygg@gmail.com'
app.config['MAIL_PASSWORD'] = 'oiocqtghvwjkiprf'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#duffel api
access_token = 'duffel_test_kJLcDXpH11bKR78Y5Kxu7MFMck1D1Xlx0cHWwAgxmb8'
client = Duffel(access_token = access_token)
from datetime import datetime


#fliapi
iata_code = [{'YYZ':'Toronto Pearson International Airport'}, {'YYT':'St. John\'s International Airport'}, {'YYC':'Calgary International Airport'}, {'YWG':'Winnipeg International Airport'}, {'YVR':'Vancouver International Airport'}, {'YUL':'Montréal Trudeau International Airport'}, {'YQX':'Gander International Airport'}, {'YQM':'Greater Moncton Roméo LeBlanc International Airport'}, {'YQB':'Québec/Jean Lesage International Airport'}, {'YOW':'Ottawa Macdonald Cartier International Airport'}, 	{'YHZ':'Halifax Stanfield International Airport'}, {'YFC':'Fredericton International Airport'}, {'YEG':'Edmonton International Airport'}]
fliapi = "https://airlabs.co/api/v9/cities?name=Singapore&api_key=961e45ec-e4c1-4ce8-99ef-c9411dde97e2"
data = requests.get(fliapi).json()
data = data['response']


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
      msg = "username already exists"
      return render_template('login.html', msg = msg)
    else:
      db.collection('Logcred').add({'Username':username, 'Password':password})
      msg = "account created"
      return render_template('login.html', msg = msg) 
    
  return render_template('login.html')

@app.route('/', methods = ['GET', 'POST'])
def index():
  session['username'] = 0
  if session['username'] in session and session['username']!=0:
    return render_template('main.html')
  else:
    return render_template('login.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
  # create session from login information
  if request.method == 'POST':
    username = request.form['username']
    password = request.form['password']
    docs = db.collection('Logcred').where("Username", "==", username).get()
    if not docs:
      msg = "invalid user or password"
      return render_template('login.html', msg = msg)
    else:
      for doc in docs:
        usdoc =  doc.to_dict()
      if usdoc["Username"] == username and usdoc["Password"] == password:
        session['username'] = usdoc["Username"]
        return render_template('main.html')
      else:
        msg = "invalid user or password"
        return render_template('login.html', msg = msg)  
    
  return render_template('login.html')


@app.route('/logout')
def logout():
  # remove the username from the session if it is there
  session.pop('username', None)
  return render_template('index.html')

@app.route('/land', methods = ['GET', 'POST'])
def land():
  return render_template('main.html')


def get_code(name):
  for i in data:
    if i['name'] == name:
      return i['city_code']

@app.route('/flights', methods = ['GET', 'POST'])
def flights():
  
  destination = get_code(request.form["dest"])
  origin = get_code(request.form["ori"])
  departure_date = request.form["date"]

  slices = [
        {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
        },
    ]
  offer_request = (
        client.offer_requests.create()
        .passengers([{"type": "adult"}])
        .slices(slices)
        .return_offers()
        .execute()
    )
  offers = offer_request.offers

  files = []
  for offer in offers:
    files.append([offer.owner.name, offer.owner.iata_code, offer.slices[0].segments[0].operating_carrier_flight_number, offer.slices[0].segments[0].departing_at, offer.slices[0].segments[0].arriving_at, offer.total_amount])

  return render_template('info.html', files = files )

@app.route('/booking', methods = ['GET', 'POST'])
def booking():
  airline = request.form["airlinei"]
  flight = request.form["flighti"]
  depdate = request.form["depdatei"]
  arrdate = request.form["arrdatei"]
  price = request.form["pricei"]
  session['airline'] = airline
  session['flight'] = flight
  session['depart'] = depdate
  session['arrdate'] = arrdate
  session['price'] = price
  db.collection('history').add({'Username':session['username'], 'Airline':airline, 'Flight No': flight, 'Departure Date': depdate, 'Arrival Date': arrdate, 'Price': price})


  return render_template('payment.html')

@app.route('/payment', methods = ['GET', 'POST'])
def payment():
  return render_template('payment.html')

@app.route('/emailing', methods = ['GET', 'POST'])
def emailing():
  email = request.form["email1"]
  msg = Message('ARS-Flight Ticket Confirmation', sender = 'ajay.21cs@licet.ac.in', recipients = [email])
  msg.body = "Your Flight Ticket has been confirmed\n"+"airlines:"+session['airline']+"\t"+"flight no:"+session['flight']+"\t"+"departure:"+session['depart']+"\t"+"Arrival:"+session['arrdate']+"\t"+"Price:"+session['price']
  mail.send(msg)
  session.pop('airline', None)
  session.pop('flight', None)
  session.pop('depart', None)
  session.pop('arrdate', None)
  session.pop('price', None)
  return render_template('history.html')



@app.route('/history', methods = ['GET', 'POST'])
def history():
  username = session['username']
  docs = db.collection('history').where("Username", "==", username).get()
  files = []
  for doc in docs:
    usdoc =  doc.to_dict()
    files.append([usdoc["Airline"], usdoc["Flight No"], usdoc["Departure Date"], usdoc["Arrival Date"]])
  return render_template('history.html', files = files)

@app.route('/cancel', methods = ['GET', 'POST'])
def cancel():
  todo_id = request.form["flightid"]
  try:
    db.collection('history').document(todo_id).delete()
    return render_template('main.html')
    
  except Exception as e:
    return f"An Error Occured: {e}"
  



