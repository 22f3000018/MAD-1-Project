from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask import current_app as hospital_app
from application.models import Admin, Doctor, Patient, PatientHistory, Appointment
from application.database import db

@hospital_app.route('/doctor_dashboard')
def doctor_dashboard_fn():
    if session.get('role') != 'doctor':
        flash(message='Please log in as doctor to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    doc = Doctor.query.filter_by(username=session['username']).first()
    return render_template('dashboard_doctor.html', doc=doc)


