from flask import Flask
from duffel_api import Duffel
from flask_mail import Mail
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
app.config['MAIL_USERNAME'] = 'g.ajaygg@gmail.com'
app.config['MAIL_PASSWORD'] = 'oiocqtghvwjkiprf'
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