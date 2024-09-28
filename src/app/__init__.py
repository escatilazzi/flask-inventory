import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from .models import db
from .account.routes import auth_bp
from .patient.routes import patient_bp
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Nueva123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Nueva123@db:5432/flask_psychology'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    db.init_app(app)  

    migrate = Migrate(app, db) 
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)

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