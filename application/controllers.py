from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask import current_app as hospital_app
from application.models import Admin, Doctor, Patient
from application.database import db

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
    doc = Doctor.query.filter_by(username=username, password=password).first()
    pat = Patient.query.filter_by(username=username, password=password).first()
    
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
  

@hospital_app.route('/admin_dashboard')
def admin_dashboard_fn():
    if session.get('role') != 'admin':
        flash(message='Please log in as admin to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    admin = Admin.query.filter_by(username=session['username']).first()
    list_of_doctors = Doctor.query.all()
    list_of_patients = Patient.query.all()
    return render_template('dashboard_admin.html', admin_name=admin.last_name, registered_doctors=list_of_doctors, 
                           registered_patients=list_of_patients)


@hospital_app.route('/doctor_dashboard')
def doctor_dashboard_fn():
    if session.get('role') != 'doctor':
        flash(message='Please log in as doctor to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    doc = Doctor.query.filter_by(username=session['username']).first()
    return render_template('dashboard_doctor.html', doc=doc)


@hospital_app.route('/patient_dashboard')
def patient_dashboard_fn():
    if session.get('role') != 'patient':
        flash(message='Please log in as patient to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    pat = Patient.query.filter_by(username=session['username']).first()
    return render_template('dashboard_patient.html', patient=pat)


@hospital_app.route('/update-doctor/<int:doctor_id>', methods=['GET', 'POST'])
def update_doctor_fn(doctor_id):
    if session.get('role') != 'admin':
        flash(message='Please log in as admin to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    if request.method == 'GET':
        doctor = Doctor.query.filter_by(id=doctor_id).first()
        if doctor is None:
            flash(message='Doctor not found', category='danger')
            return redirect(url_for('admin_dashboard_fn'))
        return render_template('update_doctor.html', doctor=doctor)
    if request.method == 'POST':
        doctor = Doctor.query.filter_by(id=doctor_id).first()
        doctor.username = request.form.get('register_form_usrname')
        doctor.email = request.form.get('register_form_mail')
        doctor.first_name = request.form.get('register_form_f_name')
        doctor.last_name = request.form.get('register_form_l_name')
        doctor.department_id = request.form.get('register_form_dep_id')
        doctor.specialization = request.form.get('register_form_specialization')
        doctor.experience_years = request.form.get('register_form_experience')
        doctor.gender = request.form.get('register_form_Input9')
        db.session.commit()
        flash(message='Doctor updated successfully', category='success')
        return redirect(url_for('admin_dashboard_fn'))