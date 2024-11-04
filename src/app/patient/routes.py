from flask import Blueprint, render_template, request, redirect, url_for, flash, session,current_app
from ..models import db, Patient, SocialSecurity, Session, Appointment
from werkzeug.utils import secure_filename
from datetime import datetime

patient_bp = Blueprint('patient', __name__)


@patient_bp.route('/patients', methods=['GET', 'POST'])
def patients():

    patients = db.session.query(Patient).join(SocialSecurity, Patient.social_id == SocialSecurity.id).all()
    socials = SocialSecurity.query.all()
    return render_template('patients.html', patients=patients, socials=socials)

@patient_bp.route('/patients/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
            user_id = session['id'] 
            name = request.form['name']
            lastname = request.form['lastname']
            age = request.form['age']
            number = request.form['number']
            email = request.form['email']
            country = request.form['country']
            social_id = request.form['social_id']            

            new_patient = Patient(name=name, lastname=lastname, age=age, number=number, email=email, country=country, social_id=social_id, is_active='yes', user_id=user_id)
            db.session.add(new_patient)
            db.session.commit()
            flash('Paciente creado exitosamente!', 'success')
        
            return redirect(url_for('patient.patients'))
    
@patient_bp.route('/patients/edit/<int:id>', methods=['GET','POST'])
def edit():
    patient = Patient.query.get(id)
    patient.name = request.form['name']
    patient.lastname = request.form['lastname']
    patient.age = request.form['age']
    patient.number = request.form['number']
    patient.email = request.form['email']
    patient.country = request.form['country']
    patient.social_id = request.form['social_id']   
    patient.is_active = request.form['is_active']        
    db.session.commit()
    flash('Paciente actualizado exitosamente!', 'success')

    return redirect(url_for('patient.patients'))

    
@patient_bp.route('/patients/delete/<int:id>', methods=['GET','POST'])
def delete():
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('patient.patients'))

@patient_bp.route('/patients/search', methods=['GET'])
def search_patients():
    query = request.args.get('query') 
    
    if query:
        search = Patient.query.filter(
            (Patient.name.ilike(f'%{query}%')) |
            (Patient.lastname.ilike(f'%{query}%')) |
            (Patient.number.ilike(f'%{query}%')) |
            (Patient.email.ilike(f'%{query}%'))
        ).all()
    
    return render_template('patients.html', search=search)

@patient_bp.route('/patients/<int:id>/history', methods=['GET','POST'])
def patients_history(id):
    patient = Patient.query.get(id)
    sessions = Session.query.filter_by(patient_id=id).all()
    return render_template('patients_history.html', patient= patient, sessions= sessions)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allow(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@patient_bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return None
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return filename

@patient_bp.route('/patients/<int:id>/session', methods = ['GET','POST'])
def patients_session(id):
    patient = Patient.query.get_or_404(id)
    if request.method == 'POST':
        session_note = request.form['session_note']
        session_date_str = request.form['session_date']
        session_type = request.form['session_type']
        assist = request.form['assist']
        pay = request.form['pay']
        session_file = upload_file()
        session_date = datetime.strptime(session_date_str, '%Y-%m-%d %H:%M')
         

        new_session = Session(
            patient_id=id,
            session_note=session_note,
            session_date=session_date,
            session_type= session_type,
            assist=assist,
            pay=pay,
            session_file=session_file,
            user_id = session['id']
 
        )
        db.session.add(new_session)
        db.session.commit()
        
        flash('Sesión creada exitosamente')
        return redirect(url_for('patient.patients_history', id=id))


    appointments= Appointment.query.filter_by(patient_id=id).all()

    return render_template('patients_session.html',patient=patient, appointments=appointments)
            
