from flask import Flask, render_template, request, flash, redirect, url_for
from application.database import db

def create_app():
  app = Flask(__name__)
  app.debug = True
  app.secret_key = 'your-secret-key-here-change-in-production'
  app.app_context().push()
  # Configure SQLite database
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.sqlite3'
  db.init_app(app)
  return app

hospital_app = create_app()
# Only after creating the app, current_app in will be available in controllers.py
from application.admin_functionalities import *
from application.doctor_functionalities import *
from application.registration_functions import * 


if __name__ == "__main__":
  db.create_all()
  # Execute the following code only once for Admin registration
  # Roles & Functionalities : 1. a. Admin is the pre-existing superuser of the application
  # from application.models import Admin
  # user1 = Admin(username="admin123",email="admin@myhospital.com",password="12345",first_name="Adi",last_name="Saba")
  # db.session.add(user1)
  # db.session.commit()
  hospital_app.run()