from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import db, User

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        registration = request.form['registration']
        password = request.form['password']
        
        user = User(name=name, lastname=lastname, email=email, registration=registration)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # Redirect to the main page of the application

        flash('Invalid credentials', 'danger')
    
    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))