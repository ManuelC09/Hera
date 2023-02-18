from flask import render_template, Blueprint, session
from Hera import app
from Hera.users.models import User
from Hera.medicion.models import UserDato

from Hera import db

base = Blueprint('base', __name__)


# Manejo general de todos los errores 404 en la apllicación
@app.errorhandler(404)
def page_not_found(e):

    """
    https://flask.palletsprojects.com/en/1.0.x/patterns/errorpages/
    
    """

    return render_template('error404.html'), 404




@base.route('/')
def index():

    """
    Obtenemos los datos del usuario, en caso de que encuentre algun dato los mostrara en la página 
    de inicio, y si no solo retorna la plantilla inicial
        
    """

    try:
        user = UserDato.query.filter_by(id_usuario = session['id_usuario']
        ).order_by(UserDato.id.desc()).limit(3)

        nombre = User.query.filter_by(id = session['id_usuario']).first()
        nombre = nombre.nombre.split(' ')
        nombre = ''.join(nombre[0])

        return render_template('index.html', nombre = nombre, user = user)

    except:
        return render_template('index.html', user = None)