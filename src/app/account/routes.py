from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models import db, User
from flask_mail import Message
from app import mail
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
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

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email=request.form['email']
        password=request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['id'] = user.id
            session['email'] = user.email
            session['name'] = user.name
            session['lastname'] = user.lastname
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid password', 401  # Si la contraseña es incorrecta

    return render_template('login.html')

@auth_bp.route('/reset_password_request', methods=['GET','POST'])
def reset_password_request():
    if request.method == 'POST':
        email=request.form['email']
        email = User.query.filter_by(email=email).first()
        if email:
            send_reset_email(email)
            flash('Se ha enviado un enlace de restablecimiento a tu correo electrónico', 'info')
        else:
            flash('El correo electrónico no está registrado', 'warning')
    return redirect(url_for('auth.login'))

def send_reset_email(user):
    token = user.get_reset_token()  # Debes crear un método para generar un token de restablecimiento
    msg = Message('Restablece tu contraseña', sender='noreply@yourapp.com', recipients=[user.email])
    msg.body = f'''Para restablecer tu contraseña, haz clic en el siguiente enlace:
{url_for('auth.reset_password', token=token, _external=True)}

Si no solicitaste este cambio, por favor ignora este correo.
'''
    mail.send(msg)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.verify_reset_token(token)
    if not user:
        flash('Token inválido o expirado', 'warning')
        return redirect(url_for('auth.reset_password_request'))

    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            error = 'Las contraseñas no coinciden.'
            return render_template('reset_password.html', token=token, error=error)
        
        user.set_password(password)  # Método que encripta la nueva contraseña
        db.session.commit()
        flash('Tu contraseña ha sido actualizada.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('reset_password.html', token=token)

@auth_bp.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('name', None)
    session.pop('lastname', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


