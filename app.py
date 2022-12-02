from flask import Flask, render_template, Response, request,  session
import requests, json
from datetime import datetime
from firebase_admin import credentials, firestore, initialize_app
from duffel_api import Duffel
from flask_mail import Mail, Message
from flask_session import Session
import requests

app = Flask(__name__)

app.secret_key = 'BAD_SECRET_KEY_SDA_PROJECT'

#Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#email
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

#duffel api
access_token = 'duffel_test_kJLcDXpH11bKR78Y5Kxu7MFMck1D1Xlx0cHWwAgxmb8'
client = Duffel(access_token = access_token)


#fliapi
fliapi = "https://airlabs.co/api/v9/cities?name=Singapore&api_key=961e45ec-e4c1-4ce8-99ef-c9411dde97e2"
data = requests.get(fliapi).json()
data = data['response']

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('Logcred')



# Register new account
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

# Index page
@app.route('/', methods = ['GET', 'POST'])
def index():
  session['username'] = 0
  if session['username'] in session and session['username']!=0:
    return render_template('main.html')
  else:
    return render_template('login.html')

# Login 
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

# Logout
@app.route('/logout')
def logout():
  # remove the username from the session if it is there
  session.pop('username', None)
  return render_template('login.html')

@app.route('/land', methods = ['GET', 'POST'])
def land():
  return render_template('main.html')

#getting IATA code from fliapi
def get_code(name):
  msg = "not name"
  for i in data:
    if i['name'] == name:
      return i['city_code']
  return msg

#search logic
@app.route('/flights', methods = ['GET', 'POST'])
def flights():
  msg = "Enter correct city name"
  dname = request.form["dest"].capitalize() #capitalizing inputs
  oname = request.form["ori"].capitalize() #capitalizing inputs
  destination = get_code(dname)
  origin = get_code(oname)
  departure_date = request.form["date"]
  #storing city/IATA codes in database
  ddocs = db.collection('City').where("IATA", "==",destination).get()
  if len(ddocs) == 0:
    db.collection('City').add({'IATA': destination, 'cityname':dname })
  odocs = db.collection('City').where("IATA", "==",origin).get()
  if len(odocs) == 0:
    db.collection('City').add({'IATA': origin, 'cityname':oname })
#sending error message if city names are not correctly entered
  if destination=="not name" or origin == "not name":
    return render_template("main.html", msg = msg)
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
  return render_template('payment.html')

@app.route('/paymentroute', methods = ['GET', 'POST'])
def paymentroute():
  return render_template('payment.html')

@app.route('/payment', methods = ['GET', 'POST'])
def payment():
  uname = request.form["firstname"]
  email = request.form["email"]
  address = request.form["address"]
  city = request.form["city"]
  province = request.form["pro"]
  zip = request.form["zcode"]

  cname = request.form["cardname"]
  cnum = request.form["cardnumber"]
  emonth = request.form["expmonth"]
  eyear = request.form["expyear"]
  cvv = request.form["cvv"]

  pdata = {'Namecredit':cname, 'Cardno':cnum, 'Expmonth': emonth, 'Expyear': eyear, 'CVV': cvv} 
  pay = db.collection('Payment').add(pdata)
  pid = pay[1].id

  cdata = {'Address':address, 'City':city, 'Email':email, 'Name':uname, 'Payment id':pid, 'Province': province, 'Zip':zip}
  db.collection('Contact info').add(cdata)

  
  db.collection('History').add({'Username':session['username'], 'Airline':session['airline'], 'Flight No': session['flight'], 'Departure Date': session['depart'], 'Arrival Date': session['arrdate'], 'Price': session['price'], 'Payment id': pid})
  #poping session after storing in db to reduce overhead
  session.pop('airline', None)
  session.pop('flight', None)
  session.pop('depart', None)
  session.pop('arrdate', None)
  session.pop('price', None)
  return render_template('main.html')
  
#email logic
@app.route('/emailing', methods = ['GET', 'POST'])
def emailing():
  email = request.form["email1"]
  msg = Message('ARS-Flight Ticket Confirmation', sender = 'ajay.21cs@licet.ac.in', recipients = [email])
  msg.body = "Your Flight Ticket has been confirmed\n"+"airlines:"+session['airline']+"\t"+"flight no:"+session['flight']+"\t"+"departure:"+session['depart']+"\t"+"Arrival:"+session['arrdate']+"\t"+"Price:"+session['price']
  mail.send(msg)
  return render_template('history.html')


@app.route('/history', methods = ['GET', 'POST'])
def history():
  username = session['username']
  docs = db.collection('History').where("Username", "==", username).get()
  files = []
  for doc in docs:
    key = doc.id
    usdoc =  doc.to_dict()
    files.append([key, usdoc["Airline"], usdoc["Flight No"], usdoc["Departure Date"], usdoc["Arrival Date"]])
  return render_template('history.html', files = files)

@app.route('/cancel', methods = ['GET', 'POST'])
def cancel():
  bid = request.form["bookingid"]
  try:
    db.collection('History').document(bid).delete()
    return render_template('main.html')
    
  except Exception as e:
    return f"An Error Occured: {e}"




