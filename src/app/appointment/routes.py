from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from ..models import db, Patient, SocialSecurity, Appointment
from datetime import datetime, timedelta

appointment_bp = Blueprint('appointment', __name__)


@appointment_bp.route('/appointments', methods=['GET', 'POST'])
def appointments():
    # Realiza un join entre las tablas 'appointments' y 'patients'
    all_appointments = db.session.query(Appointment, Patient).join(Patient, Appointment.patient_id == Patient.id).all()
    patients = Patient.query.all()
    events = []
    
    # Fecha límite para evitar una generación infinita de turnos recurrentes
    recurrence_end_limit = datetime.now() + timedelta(weeks=52)  # Limita la recurrencia a 1 año

    for appointment, patient in all_appointments:
        # Crear evento para el turno original
        event = {
            'id': appointment.id,
            'title': f'Turno con {patient.name} {patient.lastname}',
            'start': f'{appointment.date}T{appointment.time}',
            'status': appointment.status
        }
        events.append(event)

        # Manejar recurrencias si están presentes
        if appointment.recurrence_interval and appointment.recurrence_type:
            current_date = datetime.combine(appointment.date, appointment.time)
            # Mientras no se sobrepase la fecha límite
            while current_date < recurrence_end_limit:
                # Actualiza current_date según el tipo de recurrencia
                if appointment.recurrence_type == 'Weekly':
                    current_date += timedelta(weeks=appointment.recurrence_interval)
                elif appointment.recurrence_type == 'Monthly':
                    current_date += timedelta(weeks=4 * appointment.recurrence_interval)  # Aproximado a 1 mes
                
                # Verificar que no se sobrepase el límite de recurrencia
                if current_date >= recurrence_end_limit:
                    break
                
                event_recurring = {
                    'id': f'{appointment.id}-recurring-{current_date.strftime("%Y%m%d%H%M%S")}',  # Un identificador único para el evento recurrente
                    'title': f'Turno con {patient.name} {patient.lastname}',
                    'start': current_date.strftime('%Y-%m-%dT%H:%M:%S'),
                    'status': appointment.status
                }
                events.append(event_recurring)

    return render_template('appointments.html', appointments=all_appointments, events=events, patients=patients)

@appointment_bp.route('/appointments/create', methods=['GET', 'POST'])
def create():
    try:
        # Obtener los datos del formulario
        date = request.form.get('date')
        time = request.form.get('time')
        patient_id = request.form.get('patient_id')
        status = request.form.get('status')
        recurrence_type = request.form.get('recurrence_type')
        recurrence_interval = request.form.get('recurrence_interval')
        recurrence_end = request.form.get('recurrence_end', None)

        if not patient_id or not date or not time or not status:
            return jsonify({"error": "Missing required fields"}), 400
        
        # Parsear fecha y hora
        appointment_date = datetime.strptime(date, '%Y-%m-%d').date()
        appointment_time = datetime.strptime(time, '%H:%M').time()

        # Verificar si recurrence_end se pasó como None o vacío y evitar loops
        if recurrence_type != 'Only' and not recurrence_end:
            return jsonify({"error": "Recurrence end date is required for recurring appointments"}), 400
        if recurrence_end:
            recurrence_end = datetime.strptime(recurrence_end, '%Y-%m-%d').date()

        # Crear turnos sin recurrencia
        if recurrence_type == 'Only':
            new_appointment = Appointment(
                patient_id=patient_id,
                date=appointment_date,
                time=appointment_time,
                status=status,
                recurrence_type=recurrence_type,
                recurrence_interval=int(recurrence_interval) if recurrence_interval else None,
                recurrence_end=None
            )
            db.session.add(new_appointment)
            db.session.commit()

            return redirect(url_for('appointment.appointments'))
        
        # Crear turnos con recurrencia
        else:
            current_date = appointment_date
            while current_date <= recurrence_end:
                new_appointment = Appointment(
                    patient_id=patient_id,
                    date=current_date,
                    time=appointment_time,
                    status=status,
                    recurrence_type=recurrence_type,
                    recurrence_interval=recurrence_interval,
                    recurrence_end=recurrence_end
                )
                db.session.add(new_appointment)

                # Incrementar la fecha según el tipo de recurrencia
                if recurrence_type == 'Weekly':
                    current_date += timedelta(weeks=1)
                elif recurrence_type == 'Monthly':
                    current_date += relativedelta(months=1)

            db.session.commit()

            return redirect(url_for('appointment.appointments'))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

