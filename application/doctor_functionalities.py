from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask import current_app as hospital_app
from application.models import Doctor, Patient, PatientHistory, Appointment, DoctorAvailability
from application.database import db
from sqlalchemy import or_

@hospital_app.route('/doctor_dashboard')
def doctor_dashboard_fn():
    if session.get('role') != 'doctor':
        flash(message='Please log in as doctor to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    if request.method == 'GET':
      # Retrieve current username from session and using username identify the doctor
      doctor = Doctor.query.filter_by(username=session['username']).first()
      
    list_of_all_appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    # Get only future appointments (date is stored as string 'DD-MM-YYYY')
    from datetime import datetime, timedelta
    today = datetime.today().date()
    next_7_days = today + timedelta(days=7)
    future_booked_appointments = [appt for appt in list_of_all_appointments
                            if today <= datetime.strptime(appt.date, '%d-%m-%Y').date() <= next_7_days
                            and appt.status == 'Booked']

    # Get patient IDs from appointments
    patient_ids = {appt.patient_id for appt in list_of_all_appointments}
    list_of_patients = Patient.query.filter(Patient.id.in_(patient_ids)).all()

    return render_template('dashboard_doctor.html', doc=doctor, 
                          treated_patients=list_of_patients,
                          upcoming_appointments=future_booked_appointments)


@hospital_app.route('/view-patient-treatment-history/<int:patient_id>', methods=['GET'])
def patient_details_fn(patient_id):
    if session.get('role') != 'doctor':
        flash(message='Please log in as doctor to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    if request.method == 'GET':
      patient = Patient.query.filter_by(id=patient_id).first()
      if patient is None:
          flash(message='Patient not found', category='danger')
          return redirect(url_for('doctor_dashboard_fn'))
      
      patient_history = PatientHistory.query.filter_by(patient_id=patient_id).all()
      return render_template('patient_treatment_history.html', patient=patient, patient_history=patient_history)
    

@hospital_app.route('/update-patient-treatment-details/<int:appointment_id>/<int:patient_id>', methods=['GET', 'POST'])
def update_patient_treatment_fn(appointment_id, patient_id):
    if session.get('role') != 'doctor':
        flash(message='Please log in as doctor to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    if request.method == 'GET':
        patient = Patient.query.filter_by(id=patient_id).first()
        appointment = Appointment.query.filter_by(id=appointment_id).first()
        if patient is None:
            flash(message='Patient not found', category='danger')
            return redirect(url_for('doctor_dashboard_fn'))
        return render_template('update_patient_treatment.html', patient=patient, appointment=appointment)
    if request.method == 'POST':
        diagnosis = request.form.get('treatment_form_Input1')
        prescription = request.form.get('treatment_form_Input2')
        notes = request.form.get('treatment_form_Input3')

        new_treatment_entry = PatientHistory(patient_id=patient_id, appointment_id=appointment_id,
                                            diagnosis=diagnosis,
                                            prescription=prescription, notes=notes)
        db.session.add(new_treatment_entry)
        db.session.commit()
        flash(message='Patient treatment details updated successfully!', category='success')
        return redirect(url_for('doctor_dashboard_fn'))
    

@hospital_app.route('/mark-complete/<int:appointment_id>', methods=['GET'])
def mark_appointment_complete_fn(appointment_id):
    if session.get('role') != 'doctor':
        flash(message='Please log in as doctor to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if appointment is None:
        flash(message='Appointment not found', category='danger')
        return redirect(url_for('doctor_dashboard_fn'))
    appointment.status = 'Completed'
    db.session.commit()
    flash(message='Appointment marked as complete.', category='success')
    return redirect(url_for('doctor_dashboard_fn'))


@hospital_app.route('/cancel-appointment/<int:appointment_id>', methods=['GET'])
def cancel_appointment_fn(appointment_id):
    if session.get('role') != 'doctor':
        flash(message='Please log in as doctor to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if appointment is None:
        flash(message='Appointment not found', category='danger')
        return redirect(url_for('doctor_dashboard_fn'))
    appointment.status = 'Cancelled'
    db.session.commit()
    flash(message='Appointment has been canceled.', category='success')
    return redirect(url_for('doctor_dashboard_fn'))


