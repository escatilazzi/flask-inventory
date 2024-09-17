from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models import db, Patient

patient_bp = Blueprint('patient', __name__)


@patient_bp.route('/patients', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        age = request.form['age']
        contact = request.form['contact']
        email = request.form['email']
        country = request.form['country']
        
        patient = Patient(name=name, lastname=lastname, age=age, contact=contact, email=email, country=country, is_active='yes')
        
        db.session.add(patient)
        db.session.commit()

        flash('Patient created successfully!', 'success')
        return redirect(url_for('patient.create'))
    return render_template('/patients')

@patient_bp.route('/patients/<int:id>', methods=['GET', 'POST'])
def update(id):
    patient = Patient.query.get(id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.lastname = request.form['lastname']
        patient.age = request.form['age']
        patient.contact = request.form['contact']
        patient.email = request.form['email']
        patient.country = request.form['country']
        
        db.session.commit()

        flash('Patient updated successfully!', 'success')
        return redirect(url_for('patient.update', id=id))
    return render_template('/patients')

@patient_bp.route('/patients/<int:id>', methods=['GET'])
def delete(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted successfully!', 'success')
    return redirect(url_for('patient.delete'))

@patient_bp.route('/patients', methods=['GET'])
def get_all():
    patients = Patient.query.all()
    return render_template('/patients', patients=patients)
