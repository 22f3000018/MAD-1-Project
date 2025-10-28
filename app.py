from flask import Flask, render_template, request, flash, redirect, url_for
from application.database import db
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

def create_app():
  app = Flask(__name__)
  app.debug = True
  app.app_context().push()
  # Configure SQLite database
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.sqlite3'
  db.init_app(app)
  return app

hospital_app = create_app()
# Only after creating the current_app in controllers.py will be available
from application.controllers import *

@hospital_app.route('/')
@hospital_app.route('/login', methods=['GET', 'POST']) 
def hospital_home():
  # Route for the home page (default method is GET).
  if request.method == 'GET': 
    print("GET request received")
    return render_template('login.html', msg="Please log in to continue.")
  if request.method == 'POST':
    print("POST request received")
    return "login successful"

@hospital_app.route('/register', methods = ['GET', 'POST'])
def register_page_fn():
    if request.method == 'GET': 
      print("GET request received")
      return render_template('register.html', msg="Please register to continue.")
    if request.method == 'POST':
      action = request.form.get('register_action') # "Register"
      print("POST request received")
      if action == 'Register':
        # handle registration fields (remember to add name attributes to username/email/password inputs)
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        # process registration...
        return "registration successful"


if __name__ == "__main__":
  hospital_app.run()