from flask import Flask, render_template, Response, request, session, flash, redirect, url_for, abort, send_file, send_from_directory, jsonify

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'



@app.route("/")
def index():
  return render_template('index.html')


