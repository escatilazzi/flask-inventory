from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models import db, Patient, SocialSecurity

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/patients', methods=['GET', 'POST'])
def manage_patients():
    query = request.args.get('query')  # Obtener el término de búsqueda
    
    if query:
        patients = Patient.query.filter(
            (Patient.name.ilike(f'%{query}%')) |
            (Patient.lastname.ilike(f'%{query}%')) |
            (Patient.number.ilike(f'%{query}%')) |
            (Patient.email.ilike(f'%{query}%'))
        ).all()
    else:
        patients = Patient.query.all()

    if request.method == 'POST':
        # Crear nuevo paciente
        user_id = session['id'] 
        if 'create' in request.form:
            name = request.form['name']
            lastname = request.form['lastname']
            age = request.form['age']
            number = request.form['number']
            email = request.form['email']
            country = request.form['country']
            social_id = request.form['social_id']            
            new_patient = Patient(name=name, lastname=lastname, age=age, number=number, email=email, country=country, social_id=social_id, is_active='yes', user_id=user_id )
            db.session.add(new_patient)
            db.session.commit()
            flash('Paciente creado exitosamente!', 'success')
    
        elif 'update' in request.form:
            patient_id = request.form['patient_id']
            patient = Patient.query.get(patient_id)
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

        elif 'delete' in request.form:
            patient_id = request.form['patient_id']
            patient = Patient.query.get(patient_id)
            db.session.delete(patient)
            db.session.commit()
            flash('Paciente eliminado exitosamente!', 'success')
    
    # Obtener lista de pacientes
    user_id = session['id']
    #patients = Patient.query.filter_by(user_id=user_id).all()
    patients = db.session.query(Patient.name, Patient.lastname, Patient.number, SocialSecurity.name.label('social_name')).join(SocialSecurity).all()
    socials = SocialSecurity.query.all()
    return render_template('patients.html', patients=patients, socials=socials)

@patient_bp.route('/patients/search', methods=['GET'])
def search_patients():
    query = request.args.get('query') 
    
    if query:
        patients = Patient.query.filter(
            (Patient.name.ilike(f'%{query}%')) |
            (Patient.lastname.ilike(f'%{query}%')) |
            (Patient.number.ilike(f'%{query}%')) |
            (Patient.email.ilike(f'%{query}%'))
        ).all()

    return render_template('patients.html', patients=patients)
