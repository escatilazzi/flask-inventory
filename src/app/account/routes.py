from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models import db, User

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        matricula = request.form['matricula']
        password = request.form['password']
        
        user = User(name=name, lastname=lastname, email=email, matricula=matricula)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()

        flash('Registration successful!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            session['name'] = user.name
            session['lastname'] = user.lastname
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid password', 401  # Si la contraseña es incorrecta

    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    session.pop('lastname', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))