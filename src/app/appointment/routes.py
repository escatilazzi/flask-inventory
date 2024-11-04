from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from ..models import db, Patient, Appointment
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz


appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/appointments', methods=['GET', 'POST'])
def appointments():
    all_appointments = db.session.query(Appointment, Patient).join(Patient, Appointment.patient_id == Patient.id).all()
    patients = Patient.query.all()
    events = []
    
    recurrence_end_limit = datetime.now() + timedelta(weeks=52) 
    argentina_tz = pytz.timezone('America/Argentina/Buenos_Aires')

    for appointment, patient in all_appointments:
        # Evento inicial
        event = {
            'id': appointment.id,
            'title': f'Turno con {patient.name} {patient.lastname}',
            'start': argentina_tz.localize(datetime.combine(appointment.date, appointment.time)).isoformat(),
            'recurrence_type': appointment.recurrence_type,
            'recurrence_days': appointment.recurrence_days,
            'end_recurrence': recurrence_end_limit.strftime('%Y-%m-%d')
        }
        events.append(event)

    return render_template('appointments.html', events=events, patients=patients)


@appointment_bp.route('/appointments/create', methods=['POST'])
def create():
    try:
        date = request.form.get('date')
        time = request.form.get('time')
        patient_id = request.form.get('patient_id')
        recurrence_type = request.form.get('recurrence_type')
        recurrence_days = ','.join(request.form.getlist('recurrence_days'))

        if not patient_id or not date or not time:
            return jsonify({"error": "Missing required fields"}), 400

        appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
        appointment_time = datetime.strptime(time, '%H:%M').time()
        recurrence_end = appointment_date + timedelta(weeks=52)

        # Guardar la cita sin crear múltiples filas en la base de datos
        new_appointment = Appointment(
            patient_id=patient_id,
            date=appointment_date,
            time=appointment_time,
            recurrence_type=recurrence_type,
            recurrence_days=recurrence_days,
            recurrence_end=recurrence_end
        )
        db.session.add(new_appointment)
        db.session.commit()

        return redirect(url_for('appointment.appointments'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500