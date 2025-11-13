from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask import current_app as hospital_app
from application.models import Admin, Doctor, Patient, PatientHistory, Appointment, Department
from application.database import db


@hospital_app.route('/patient_dashboard')
def patient_dashboard_fn():
    if session.get('role') != 'patient':
        flash(message='Please log in as patient to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    pat = Patient.query.filter_by(username=session['username']).first()
    department_list = Department.query.with_entities(Department.id).all()
    upcoming_appointments = Appointment.query.filter_by(patient_id=pat.id, status='Booked').all()
    return render_template('dashboard_patient.html', patient=pat, all_departments=department_list, upcoming_appointments=upcoming_appointments)

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