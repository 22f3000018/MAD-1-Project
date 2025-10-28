from flask import Flask, render_template, request, flash, redirect, url_for
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

hospital_app = Flask(__name__)

@ hospital_app.route('/', methods=['GET', 'POST']) 
@ hospital_app.route('/login', methods=['GET', 'POST']) 
def hospital_home():
  # Route for the home page (default method is GET).
  if request.method == 'GET': 
    print("GET request received")
    return render_template('login.html', msg="Please log in to continue.")
  if request.method == 'POST':
    print("POST request received")
    return "login successful"

@ hospital_app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET': 
      print("GET request received")
      return render_template('register.html', msg="Please register to continue.")
    if request.method == 'POST':
      print("POST request received")
      flash('Registration successful! Please login to continue!', 'success')
      return redirect(url_for('login'))
    
if __name__ == "__main__":
  hospital_app.run(debug=True)