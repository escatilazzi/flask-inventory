from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models import db, SocialSecurity

social_bp = Blueprint('socialsecurity', __name__)

@social_bp.route('/social_security', methods =['GET', 'POST'])
def manage_social():
    if request.method == 'POST':
        if 'create' in request.form:
            # Crear nueva obra social
            name = request.form['name']
            new_social = SocialSecurity(name=name)
            db.session.add(new_social)
            db.session.commit()
            return redirect(url_for('socialsecurity.get_all'))

        elif 'update' in request.form:
            # Actualizar obra social
            social_id = request.form['social_id']
            social = SocialSecurity.query.get(social_id)
            if social:
                social.name = request.form['name']
                db.session.commit()
            return redirect(url_for('socialsecurity.get_all'))

        elif 'delete' in request.form:
            # Eliminar obra social
            social_id = request.form['social_id']
            social = SocialSecurity.query.get(social_id)
            if social:
                db.session.delete(social)
                db.session.commit()
            return redirect(url_for('socialsecurity.get_all'))

    # Para solicitudes GET, mostrar la tabla de todas las obras sociales
    return redirect(url_for('socialsecurity.get_all'))


# Ruta para obtener todas las obras sociales y mostrarlas en la plantilla
@social_bp.route('/social_security/all', methods=['GET'])
def get_all():
    socials = SocialSecurity.query.all()  #
    return render_template('social_security.html', socials=socials)

