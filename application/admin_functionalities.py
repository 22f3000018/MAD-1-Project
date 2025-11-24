from flask import render_template, request, flash, redirect, session, url_for
from flask import current_app as hospital_app
from application.models import Admin, Doctor, Patient, PatientHistory, Appointment, DoctorAvailability
from application.database import db
from sqlalchemy import or_
  

@hospital_app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard_fn():
    if session.get('role') != 'admin':
        flash(message='Please log in as admin to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    if request.method == 'GET':
      admin = Admin.query.filter_by(username=session['username']).first()
      
      # Handle search
      search_query = request.args.get('search_form', '').strip()
      
      if search_query:
          search_pattern = f'%{search_query}%'
          
          list_of_doctors = Doctor.query.filter(or_(Doctor.first_name.ilike(search_pattern),
                                                    Doctor.last_name.ilike(search_pattern))).all()
          if search_query.isdigit():
              # search by patient ID
              list_of_patients = Patient.query.filter_by(id=int(search_query)).all()
          else:
              list_of_patients = Patient.query.filter(or_(
                  Patient.first_name.ilike(search_pattern),
                  Patient.last_name.ilike(search_pattern),
                  Patient.email.ilike(search_pattern),
                  Patient.phone.ilike(search_pattern)
              )).all()
          future_appointments = []
          old_appointments = []
      else:
          # Show all if no search query
          list_of_doctors = Doctor.query.all()
          list_of_patients = Patient.query.all()

          # future appointments
          from datetime import datetime
          today = datetime.today().date()
          future_appointments = [appt for appt in Appointment.query.all() 
                                 if datetime.strptime(appt.date, '%d-%m-%Y').date() >= today]
          old_appointments = [appt for appt in Appointment.query.all() 
                                 if datetime.strptime(appt.date, '%d-%m-%Y').date() < today]

      return render_template('dashboard_admin.html', admin_name=admin.last_name, 
                            registered_doctors=list_of_doctors, 
                            registered_patients=list_of_patients,
                            upcoming_appointments=future_appointments,
                            past_appointments=old_appointments,
                            search_query=search_query)


@hospital_app.route('/view-doctor/<int:doctor_id>', methods=['GET'])
def view_doctor_fn(doctor_id):
    if session.get('role') != 'admin':
        flash(message='Please log in as admin to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    if request.method == 'GET':
      doctor = Doctor.query.filter_by(id=doctor_id).first()
      if doctor is None:
          flash(message='Doctor not found', category='danger')
          return redirect(url_for('admin_dashboard_fn'))
      return render_template('view_doctor.html', doctor=doctor)


@hospital_app.route('/view-patient/<int:patient_id>', methods=['GET'])
def view_patient_fn(patient_id):
    if session.get('role') != 'admin':
        flash(message='Please log in as admin to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    if request.method == 'GET':
      patient = Patient.query.filter_by(id=patient_id).first()
      if patient is None:
          flash(message='Patient not found', category='danger')
          return redirect(url_for('admin_dashboard_fn'))
      
      patient_history = PatientHistory.query.filter_by(patient_id=patient_id).all()
      
      return render_template('view_patient.html', patient=patient, pat_his=patient_history)


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

@hospital_app.route('/update-patient/<int:patient_id>', methods=['GET', 'POST'])
def update_patient_fn(patient_id):
    if session.get('role') != 'admin':
        flash(message='Please log in as admin to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    if request.method == 'GET':
        patient = Patient.query.filter_by(id=patient_id).first()
        if patient is None:
            flash(message='Patient not found', category='danger')
            return redirect(url_for('admin_dashboard_fn'))
        return render_template('update_patient.html', patient=patient)
    if request.method == 'POST':
        patient = Patient.query.filter_by(id=patient_id).first()
        patient.username = request.form.get('register_form_usrname')
        patient.email = request.form.get('register_form_mail')
        patient.first_name = request.form.get('register_form_f_name')
        patient.last_name = request.form.get('register_form_l_name')
        patient.phone = request.form.get('register_form_phone')
        patient.age = request.form.get('register_form_age')
        patient.gender = request.form.get('register_form_Input9')
        db.session.commit()
        flash(message='Patient updated successfully', category='success')
        return redirect(url_for('admin_dashboard_fn'))
    
@hospital_app.route('/delete-doctor/<int:doctor_id>', methods=['GET'])
def delete_doctor_fn(doctor_id):
    if session.get('role') != 'admin':
        flash(message='Please log in as admin to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    doctor = Doctor.query.filter_by(id=doctor_id).first()
    if doctor is None:
        flash(message='Doctor not found', category='danger')
        return redirect(url_for('admin_dashboard_fn'))
    db.session.delete(doctor)
    db.session.commit()
    flash(message='Doctor deleted successfully', category='success')
    return redirect(url_for('admin_dashboard_fn'))

@hospital_app.route('/delete-patient/<int:patient_id>', methods=['GET'])
def delete_patient_fn(patient_id): 
    if session.get('role') != 'admin':
        flash(message='Please log in as admin to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    patient = Patient.query.filter_by(id=patient_id).first()
    if patient is None:
        flash(message='Patient not found', category='danger')
        return redirect(url_for('admin_dashboard_fn'))

    # Cancel all appointments for this patient and update doctor availability
    appointments = Appointment.query.filter_by(patient_id=patient_id, status='Booked').all()
    for appointment in appointments:
        appointment.status = 'Cancelled'
        doc_availability = DoctorAvailability.query.filter_by(doctor_id=int(appointment.doctor_id), date=appointment.date).first()
        if doc_availability:
            if appointment.time == '09:00 AM - 12:00 PM':
                doc_availability.morning_time = True
            else:
                doc_availability.evening_time = True

    db.session.delete(patient)
    db.session.commit()
    flash(message='Patient deleted successfully', category='success')
    return redirect(url_for('admin_dashboard_fn'))

@hospital_app.route('/blacklist-doctor/<int:doctor_id>', methods=['GET'])
def blacklist_doctor_fn(doctor_id):
    if session.get('role') != 'admin':
        flash(message='Please log in as admin to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    doctor = Doctor.query.filter_by(id=doctor_id).first()
    if doctor is None:
        flash(message='Doctor not found', category='danger')
        return redirect(url_for('admin_dashboard_fn'))
    
    doctor.blacklisted = True
    db.session.commit()
    flash(message='Doctor has been blacklisted successfully', category='success')
    return redirect(url_for('admin_dashboard_fn'))

@hospital_app.route('/blacklist-patient/<int:patient_id>', methods=['GET'])
def blacklist_patient_fn(patient_id):
    if session.get('role') != 'admin':
        flash(message='Please log in as admin to access this page', category='warning')
        return redirect(url_for('hospital_home_and_login'))
    patient = Patient.query.filter_by(id=patient_id).first()
    if patient is None:
        flash(message='Patient not found', category='danger')
        return redirect(url_for('admin_dashboard_fn'))
    
    patient.blacklisted = True
    db.session.commit()
    flash(message='Patient has been blacklisted successfully', category='success')
    return redirect(url_for('admin_dashboard_fn'))