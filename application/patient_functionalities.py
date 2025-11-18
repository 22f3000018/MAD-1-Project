from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask import current_app as hospital_app
from application.models import Admin, Doctor, Patient, PatientHistory, Appointment, Department, DoctorAvailability
from application.database import db


@hospital_app.route('/patient_dashboard')
def patient_dashboard_fn():
    if session.get('role') != 'patient':
        flash(message='Please log in as patient to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))

    department_id = request.args.get('dep_id')
    doctor_name = request.args.get('doctor_name')

    if department_id and doctor_name:
        list_of_doctors = Doctor.query.filter(
            Doctor.department_id == int(department_id),
            (Doctor.first_name.ilike(f'%{doctor_name}%')) |
            (Doctor.last_name.ilike(f'%{doctor_name}%'))
        ).all()
    elif department_id:
        list_of_doctors = Doctor.query.filter(Doctor.department_id == int(department_id)).all()
    elif doctor_name:
        list_of_doctors = Doctor.query.filter(
            (Doctor.first_name.ilike(f'%{doctor_name}%')) |
            (Doctor.last_name.ilike(f'%{doctor_name}%'))
        ).all()
    else:
        list_of_doctors = Doctor.query.all()
        
    pat = Patient.query.filter_by(username=session['username']).first()
    department_list = Department.query.with_entities(Department.id, Department.department_name).all()
    upcoming_appointments = Appointment.query.filter_by(patient_id=pat.id, status='Booked').all()
    return render_template('dashboard_patient.html', patient=pat, all_departments=department_list, upcoming_appointments=upcoming_appointments, search_results=list_of_doctors)

@hospital_app.route('/patient/profile', methods=['GET', 'POST'])
def patient_profile_fn():
    if session.get('role') != 'patient':
        flash(message='Please log in as patient to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    if request.method == 'GET':
      pat = Patient.query.filter_by(username=session['username']).first()
      return render_template('patient_profile.html', patient=pat)
    if request.method == 'POST':
      pat = Patient.query.filter_by(username=session['username']).first()
      # Update patient details
      pat.username = request.form.get('username')
      pat.email = request.form.get('email')
      pat.password = request.form.get('password') if request.form.get('password') else pat.password
      pat.first_name = request.form.get('first_name')
      pat.last_name = request.form.get('last_name')
      pat.phone = request.form.get('phone')
      pat.age = request.form.get('age')
      pat.gender = request.form.get('gender')
      db.session.commit()
      flash(message='Profile updated successfully', category='success')
      return redirect(url_for('patient_dashboard_fn'))


@hospital_app.route('/patient/history', methods=['GET'])
def patient_history_fn():
    if session.get('role') != 'patient':
        flash(message='Please log in as patient to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    pat = Patient.query.filter_by(username=session['username']).first()
    patient_history = PatientHistory.query.filter_by(patient_id=pat.id).all()
    return render_template('patient_history.html', patient=pat, patient_history=patient_history)


@hospital_app.route('/departments/<int:department_id>', methods=['GET'])
def view_department_fn(department_id):
    if session.get('role') != 'patient':
        flash(message='Please log in as patient to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    department = Department.query.filter_by(id=department_id).first()
    if department is None:
        flash(message='Department not found', category='danger')
        return redirect(url_for('patient_dashboard_fn'))
    doctors_in_department = Doctor.query.filter_by(department_id=department_id).all()
    return render_template('department_details.html', department=department, doctors=doctors_in_department)

@hospital_app.route('/check-availability/<int:doctor_id>', methods=['GET'])
def check_doctor_availability_fn(doctor_id):
    if session.get('role') != 'patient':
        flash(message='Please log in as patient to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    
    doctor = Doctor.query.filter_by(id=doctor_id).first()
    if doctor is None:
        flash(message='Doctor not found', category='danger')
        return redirect(url_for('patient_dashboard_fn'))
    
    availability_slots = doctor.availability_slots.all()
    if not availability_slots:
        flash(message='No availability slots found for this doctor.', category='info')
        return redirect(url_for('patient_dashboard_fn'))
    
    return render_template('show_doctor_availability.html', doctor=doctor, availability_slots=availability_slots)

@hospital_app.route('/book-appointment', methods=['POST'])
def book_appointment_fn():
    if session.get('role') != 'patient':
        flash(message='Please log in as patient to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))

    book_slot = request.form.get('book_slot')
    if not book_slot:
        flash(message='Invalid booking request.', category='danger')
        return redirect(url_for('patient_dashboard_fn'))

    doctor_id, date, slot_type = book_slot.split('|')
    # Map slot_type to time range
    if slot_type == 'morning':
        time = '09:00 AM - 12:00 PM'
    else:
        time = '02:00 PM - 05:00 PM'

    pat = Patient.query.filter_by(username=session['username']).first()
    if not pat:
        flash(message='Patient not found.', category='danger')
        return redirect(url_for('patient_dashboard_fn'))

    new_appointment = Appointment(
        patient_id=int(pat.id), doctor_id=int(doctor_id), date=date, time=time, status='Booked'
    )
    doc_availability = DoctorAvailability.query.filter_by(doctor_id=int(doctor_id), date=date).first()
    if doc_availability:
        if slot_type == 'morning':
            doc_availability.morning_time = False
        else:
            doc_availability.evening_time = False
    
    db.session.add(new_appointment)
    db.session.commit()

    flash(message='Appointment booked successfully!', category='success')
    return redirect(url_for('patient_dashboard_fn'))


@hospital_app.route('/doctor-details/<int:doctor_id>', methods=['GET'])
def doctor_details_fn(doctor_id):
    if session.get('role') != 'patient':
        flash(message='Please log in as patient to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    
    doctor = Doctor.query.filter_by(id=doctor_id).first()
    if doctor is None:
        flash(message='Doctor not found', category='danger')
        return redirect(url_for('patient_dashboard_fn'))
    
    return render_template('doctor_details.html', doctor=doctor)


@hospital_app.route('/patient/appointments/<int:appointment_id>/cancel', methods=['GET'])
def cancel_appointment_fn_patient(appointment_id):
    if session.get('role') != 'patient':
        flash(message='Please log in as patient to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if appointment is None:
        flash(message='Appointment not found', category='danger')
        return redirect(url_for('patient_dashboard_fn'))
    
    appointment.status = 'Cancelled'
    doc_availability = DoctorAvailability.query.filter_by(doctor_id=int(appointment.doctor_id), date=appointment.date).first()
    if doc_availability:
        if appointment.time == '09:00 AM - 12:00 PM':
            doc_availability.morning_time = True
        else:
            doc_availability.evening_time = True
    db.session.commit()
    flash(message='Appointment has been canceled.', category='success')
    return redirect(url_for('patient_dashboard_fn'))