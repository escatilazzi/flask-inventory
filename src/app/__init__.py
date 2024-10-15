import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from .models import db, User
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

mail=Mail()
def create_app():
    app = Flask(__name__)
    UPLOAD_FOLDER = '/app/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = b'Psicologia'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Nueva123@db:5432/flask_psychology'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['MAIL_SERVER'] = 'mailhog'
    app.config['MAIL_PORT'] = 1025
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = None
    app.config['MAIL_PASSWORD'] = None


    db.init_app(app)  
    mail = Mail(app)
    migrate = Migrate(app, db) 
    from .account.routes import auth_bp
    from .patient.routes import patient_bp
    from .medsession.routes import medsession_bp
    from .socialsecurity.routes import social_bp
    from .appointment.routes import appointment_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(medsession_bp)
    app.register_blueprint(social_bp)
    app.register_blueprint(appointment_bp)


    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/dashboard')
    def dashboard():
        if 'email' in session:
            return render_template('dashboard.html', email=session['email'], name=session['name'], lastname=session['lastname'])
        else:
            flash('You must be logged in to view this page','warning')
            return redirect(url_for('auth.login'))
        

    return app