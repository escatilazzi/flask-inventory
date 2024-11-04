import datetime
from flask import current_app 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import Serializer

db = SQLAlchemy()

class User(db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    matricula = db.Column(db.Integer, unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    # Relación con la tabla de sesiones
    sessions = db.relationship('Session', backref='user', lazy=True)
    # Relación con los pacientes (si un psicólogo maneja múltiples pacientes)
    patients = db.relationship('Patient', backref='assigned_psychologist', lazy=True)


    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
class Patient(db.Model):
    __tablename__= 'patients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    number= db.Column(db.String(15), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(120))
    is_active = db.Column(db.String(3), nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    social_id = db.Column(db.Integer, db.ForeignKey('socialsecurities.id'))
    sessions = db.relationship('Session', backref='patient', lazy=True)
    social = db.relationship('SocialSecurity', backref='assigned_patients', uselist=False)



class Session(db.Model):
    __tablename__= 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    session_note = db.Column(db.Text, nullable=False)
    session_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)
    session_type = db.Column(db.String(2000), nullable=False)
    assist = db.Column(db.String(6), nullable=False)
    pay = db.Column(db.String(6), default='NULL')
    session_file = db.Column(db.String(500), nullable=True)
    # Claves foráneas
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'))



class SocialSecurity(db.Model):
    __tablename__='socialsecurities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), nullable=False)


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    recurrence_type = db.Column(db.String(30), nullable=False, default="Only")
    recurrence_interval = db.Column(db.Integer, nullable=True)
    recurrence_end = db.Column(db.Date, nullable=True)
    recurrence_days = db.Column(db.String(20), nullable=True) 
    patient = db.relationship('Patient', backref='appointments')
