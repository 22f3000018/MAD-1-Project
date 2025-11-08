from flask import current_app as hospital_app
from flask import Flask, render_template, request, flash, redirect, url_for
from application.models import Doctor, Patient
from application.database import db

@hospital_app.route('/register', methods = ['GET', 'POST'])
def patient_register_fn():
  if request.method == 'GET': 
    print("GET request received")
    return render_template('register.html', msg="Please register to continue.")
  if request.method == 'POST':
    print("POST request received")
    # handle registration fields (remember to add name attributes to username/email/password inputs)
    username = request.form.get('register_form_Input1')
    email = request.form.get('register_form_Input2')
    password = request.form.get('register_form_Input3')
    first_name = request.form.get('register_form_Input4')
    last_name = request.form.get('register_form_Input5')
    phone = request.form.get('register_form_Input6')
    age = request.form.get('register_form_Input7')
    gender = request.form.get('register_form_Input8') 

    # Check if username already exists
    existing_patient = Patient.query.filter_by(username=username).first()
    if existing_patient != None:
      return render_template('patient_already_exists.html', username=username)

    new_patient = Patient(username=username,email=email,password=password,first_name=first_name,
                          last_name=last_name,phone=phone,age=age,gender=gender)
    db.session.add(new_patient)
    db.session.commit()
    flash(message='Registration successful! Please log in.', category='success')
    return redirect(url_for('hospital_home_and_login'))
  

@hospital_app.route('/doctor_register', methods = ['GET', 'POST'])
def doctor_register_fn():
  if request.method == 'GET': 
    print("GET request received")
    return render_template('doctor_register.html')
  if request.method == 'POST':
    print("POST request received")
    # handle registration fields (remember to add name attributes to username/email/password inputs)
    usr_name = request.form.get('register_form_Input1')
    mail_id = request.form.get('register_form_Input2')
    pwd = request.form.get('register_form_Input3')
    first_name = request.form.get('register_form_Input4')
    last_name = request.form.get('register_form_Input5')
    dept_id = request.form.get('register_form_Input6')
    specialization = request.form.get('register_form_Input7')
    experience_years = request.form.get('register_form_Input8')
    gender = request.form.get('register_form_Input9')

    # Check if doctor's username exists
    existing_doctor = Doctor.query.filter_by(username=usr_name).first()
    if existing_doctor != None:
      return render_template('doctor_already_exists.html', username=usr_name)
    
    new_doctor = Doctor(username=usr_name,email=mail_id,password=pwd,first_name=first_name,
                          last_name=last_name,department_id=dept_id,specialization=specialization,
                          experience_years=experience_years, gender=gender)
    db.session.add(new_doctor)
    db.session.commit()
    flash(message='Doctor Registration successful!', category='success')
    return redirect(url_for('admin_dashboard_fn'))