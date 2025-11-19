from flask import render_template, request, flash, redirect, session, url_for
from flask import current_app as hospital_app
from application.models import Admin, Doctor, Patient

@hospital_app.route('/')
@hospital_app.route('/login', methods=['GET', 'POST']) 
def hospital_home_and_login():
  # Route for the home page (default method is GET).
  if request.method == 'GET': 
    print("GET request received")
    return render_template('login.html', msg="Please log in to continue.")
  if request.method == 'POST':
    print("POST request received")
    username = request.form.get("login_form_Input1")
    password = request.form.get("login_form_Input2")
    admin = Admin.query.filter_by(username=username, password=password).first()
    doc = Doctor.query.filter_by(username=username, password=password, blacklisted=False).first()
    pat = Patient.query.filter_by(username=username, password=password, blacklisted=False).first()
    
    if admin:
        session['username'] = username
        session['user_id'] = admin.username
        session['role'] = 'admin'
        return redirect(url_for('admin_dashboard_fn'))
    elif doc:
        session['username'] = username
        session['user_id'] = doc.id
        session['role'] = 'doctor'
        return redirect(url_for('doctor_dashboard_fn'))
    elif pat:
        session['username'] = username
        session['user_id'] = pat.id
        session['role'] = 'patient'
        return redirect(url_for('patient_dashboard_fn'))
    
    flash(message='Invalid username or password', category='danger')
    return redirect(url_for('hospital_home_and_login'))