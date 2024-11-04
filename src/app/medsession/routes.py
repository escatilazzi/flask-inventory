from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from ..models import db, User, Patient,Session
from flask_mail import Message
from werkzeug.utils import secure_filename
import os


medsession_bp = Blueprint('medsession',__name__)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allow(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@medsession_bp.route('/manage_session', methods = ['GET','POST'])
def manage_session():
    if request.method == 'POST':
        if 'create' in request.form:
            session_note = request.form['session_note']
            session_date = request.form['session_date']
            session_type = request.form['session_type']
            assist = request.form['assit']
            pay = request.form['pay']
            patient_id = request.form['patient_id']
            user_id = request.form['user_id']
            appointment_id = request.form['appointment_id']

            db.session.add(session_note=session_note,session_date=session_date,session_type=session_type,assist=assist,pay=pay,patient_id=patient_id,user_id=user_id,appointment_id=appointment_id)
            db.session.commit
        return redirect(url_for('medsession.medical_record'))
            
@medsession_bp.route('/upload', methods =['GET','POST'])
def upload_file():
    if request.methid == 'POST':
        if 'file' not in request.files:
            flash('NO file part')
            return
        file = request.files['file']
        if file.filename == '':
            flash('No selected File')
            return
        if file and allow(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            flash('Save sucessfully')
            
@medsession_bp.route('/medrecord', methods =['GET','POST'])
def medrecord():
    user_id = session['id'] 
    sess_patient = db.session.query(Session.session_note, Session.assist, Session.pay, Patient.name, Patient.lastname  ).join(Patient).filter(User.id == user_id).all()
    return render_template('medical_record.html', sess_patient=sess_patient)
