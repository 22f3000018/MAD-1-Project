from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask import current_app as hospital_app
from application.models import Admin, Doctor, Patient, PatientHistory, Appointment
from application.database import db


@hospital_app.route('/patient_dashboard')
def patient_dashboard_fn():
    if session.get('role') != 'patient':
        flash(message='Please log in as patient to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    pat = Patient.query.filter_by(username=session['username']).first()
    return render_template('dashboard_patient.html', patient=pat)