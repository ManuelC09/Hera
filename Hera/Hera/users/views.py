from flask import render_template, Blueprint, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from Hera import db
from Hera.helpers import Email

from Hera.users.models import User
users = Blueprint('users', __name__)


@users.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        edad = request.form.get('edad')
        usuario = request.form.get('usuario')
        correo = request.form.get('email')
        clave = request.form.get('clave')
        confirmacion = request.form.get('confirmacion')

        # Verificaciones 
        if not nombre:
            return render_template("users/register.html", alert = "Ingrese su nombre") 
        
        if not edad:
            return render_template("users/register.html", alert = "Ingrese su edad") 
        
        if not usuario:
            return render_template("users/register.html", alert = "Ingrese un usuario")
        
        if not correo:
            return render_template("users/register.html", alert = "Ingrese un correo")
        
        if not clave:
            return render_template("users/register.html", alert = "Ingrese una contraseña")
        
        if not confirmacion:
            return render_template("users/register.html", alert = "Repita la contraseña")

        if clave != confirmacion:
            return render_template("users/register.html", alert = "Las claves no coinciden")

        # Creamos el objeto de usuario y lo guardamos en la base de datos
        try:
            usuario_nuevo = User(nombre, int(edad), usuario, correo, generate_password_hash(clave))
            db.session.add(usuario_nuevo)
            db.session.commit()
            db.session.close()

            #Enviamos un correo
            Email('Se ha registrado exitosamente en Hera!', correo, 'email/registro.html', nombre)

            session['id_usuario'] = usuario_nuevo
            return render_template('index.html')
        except:
            return render_template("users/register.html", alert = "Usuario y/o correo ya existen")
    else:
        return render_template('users/register.html')

@users.route('/logout')
def logout():
    session['id_usuario'] = None
    return redirect(url_for('base.index'))

@users.route('/login', methods=['GET','POST'])
def login():
    session.clear()
    if request.method == 'POST':
        usuario = User.query.filter_by(usuario = request.form.get('usuario')).first()

        # Verificariones
        if not request.form.get('usuario'):
            return render_template("users/login.html", alert = "Ingrese un usuario")
           
        if not request.form.get('contraseña'):
            return render_template("users/login.html", alert = "Ingrese una contraseña")
        
        if not usuario:
            return render_template("users/login.html", alert = "El usuario no existe")

    
        if not usuario or not check_password_hash(usuario.contraseña, request.form.get('contraseña')):
            return render_template('users/login.html', alert = "Contraseña invalida")
        
        session['id_usuario'] = usuario.id
        
        return render_template('index.html', success="Ha iniciado sesion")
        
    
    else:
        return render_template('users/login.html')