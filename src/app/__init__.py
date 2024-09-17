import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from .models import db
from .account.routes import auth_blueprint

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Nueva123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Nueva123@db:5432/flask_psychology'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(auth_blueprint)

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