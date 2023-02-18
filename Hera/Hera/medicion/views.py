from flask import render_template, Blueprint, request, session, redirect, url_for
from Hera.medicion.models import UserDato
from Hera.users.models import User
from Hera import db
from Hera.helpers import login_required, Email, Arduino
import datetime


medicion = Blueprint('medicion', __name__)

@medicion.route('/medicion', methods = ['GET', 'POST'])
@login_required
def medicion_base():

    if request.method == 'POST':
        return redirect(url_for('medicion.user_medicion'))
    
    else:
        return render_template('medicion/medicion.html')

@medicion.route('/medicion/user')
@login_required
def user_medicion():
      
    #Obtenemos el valor del bpm para mostrarlo al usuario
    bpm = Arduino(1)
    
    try:    
        #Insertar en la base de datos
        datos = UserDato(session['id_usuario'], bpm, datetime.datetime.now())
        db.session.add(datos)
        db.session.commit()
        db.session.close()
        # Obtenemos los datos del usuario para ser enviados al correo
        user = User.query.filter_by(id = session['id_usuario']).first()
        
        #Enviamos un correo
        Email('Haz obtenido una nueva medición!', user.correo, 'email/medicion.html', user.nombre, bpm)
    
    except:
        return render_template('medicion/medicion.html', alert = "Ha ocurrido un error, vuelva a intentarlo. Si el error persiste conecte de nuevo el dispositivo")
    
    return render_template('medicion/user_medicion.html', success = "Ha obtenido una nueva medición", bpm = bpm)


@medicion.route('/historial')
@login_required
def user_historial():

    historial = db.session.query(User, UserDato).join(UserDato, User.id == UserDato.id_usuario).filter(UserDato.id_usuario == session['id_usuario']).all()
    return render_template('medicion/historial.html', datos = historial)
    
@medicion.route('/tutorial')
def tutorial():

    return render_template('medicion/tutorial.html')