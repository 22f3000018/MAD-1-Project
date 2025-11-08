from .database import db

class Admin(db.Model):
    __tablename__ = 'admin'
  
    username = db.Column(db.String(80), unique=True, nullable=False, index=True, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), unique=True,nullable=False)
    last_name = db.Column(db.String(50), unique=True,nullable=False)


class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id', ondelete='RESTRICT'), nullable=False)
    specialization = db.Column(db.String(100), nullable=False, index=True)
    experience_years = db.Column(db.Integer, db.CheckConstraint('experience_years >= 0'))
    gender = db.Column(db.String(10), db.CheckConstraint("gender IN ('male', 'female')"))

    # Relationship
    department = db.relationship('Department', backref=db.backref('doctors', lazy='dynamic'))
    
    # create property name = full name
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f"<Doctor {self.username}: {self.specialization}>"

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(15))
    age = db.Column(db.Integer, db.CheckConstraint('age > 0 AND age <= 150'))
    gender = db.Column(db.String(10), db.CheckConstraint("gender IN ('male', 'female')"))
    
    def __repr__(self):
        return f"<Patient {self.username}>"

class Appointment(db.Model):
    __tablename__ = 'appointment'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id', ondelete='CASCADE'), nullable=False, index=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Booked')
    
    # Relationships
    patient = db.relationship('Patient', backref=db.backref('appointments', lazy='dynamic', cascade='all, delete-orphan'))
    doctor = db.relationship('Doctor', backref=db.backref('appointments', lazy='dynamic', cascade='all, delete-orphan'))
    
    # Unique constraint to prevent double booking
    __table_args__ = (
        db.UniqueConstraint('doctor_id', 'date', 'time', name='unique_doctor_appointment'),
        db.CheckConstraint("status IN ('Booked', 'Completed', 'Cancelled')", name='valid_status')
    )
    
    @property
    def is_booked(self):
        return self.status == 'Booked'
    
    @property
    def is_completed(self):
        return self.status == 'Completed'
    
    @property 
    def is_cancelled(self):
        return self.status == 'Cancelled'
    
    def __repr__(self):
        return f"<Appointment {self.id}: {self.patient.username} -> {self.doctor.username}>"

class Department(db.Model):
    __tablename__ = 'department'
    
    id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    doctors_registered = db.Column(db.Integer, default=0)

class DoctorAvailability(db.Model):
    __tablename__ = 'doctor_availability'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id', ondelete='CASCADE'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    morning_time = db.Column(db.String(50))  # e.g., "9:00 AM - 12:00 PM"
    evening_time = db.Column(db.String(50))  # e.g., "2:00 PM - 5:00 PM"
    
    # Relationship
    doctor = db.relationship('Doctor', backref=db.backref('availability_slots', lazy='dynamic', cascade='all, delete-orphan'))
    
    # Unique constraint - one availability record per doctor per date
    __table_args__ = (db.UniqueConstraint('doctor_id', 'date', name='unique_doctor_date_availability'),)

class Treatment(db.Model):
    __tablename__ = 'treatment'
    
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id', ondelete='CASCADE'), nullable=False, index=True)
    diagnosis = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text)
    notes = db.Column(db.Text)
    
    # Relationship lazy == 'dynamic' to load treatments slowly
    appointment = db.relationship('Appointment', backref=db.backref('treatments', lazy='dynamic', cascade='all, delete-orphan'))
    
    @property
    def has_prescription(self):
        return bool(self.prescription and self.prescription.strip())