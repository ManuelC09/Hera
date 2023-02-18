from flask import render_template, Blueprint, request, session, redirect, url_for, send_file
from werkzeug.security import check_password_hash

from Hera import db
from Hera.helpers import excel

from Hera.admin.models import Admin
from Hera.users.models import User
from Hera.medicion.models import UserDato

admin = Blueprint('admin', __name__)


@admin.route('/homeadmin')
def home_admin():
    return render_template('admin/homeAdmin.html')


@admin.route('/adminlogout')
def admin_logout():
    session['id_admin'] = None

    return redirect(url_for('base.index'))


@admin.route('/admin', methods=['GET', 'POST'])
@admin.route('/adminlogin', methods=['GET', 'POST'])
def admin_login():
    """
    Asegurate de crear un usuario admin, esto lo puedes hacer de la siguiente manera:
    Si lo vas a registrar asegurate de immportar generate_password_hash

    * from werkzeug.security import check_password_hash, generate_password_hash

    NOTA: Si no incluyes generate_password_hash el programa no servira

    admin = Admin('usuario', generate_password_hash('contraseña'))
    db.session.add(admin)
    db.session.commit()

    """
    session.clear()
    if request.method == 'POST':

        admin = Admin.query.filter_by(
            usuario=request.form.get('usuario')).first()

        # Verificaciones
        if not request.form.get('usuario'):
            return render_template("admin/loginAdmin.html", alert="Ingrese un usuario")

        if not request.form.get('contraseña'):
            return render_template("admin/loginAdmin.html", alert="Ingrese una contraseña")

        if not admin:
            return render_template("admin/loginAdmin.html", alert="El usuario no existe")

        if not admin or not check_password_hash(admin.contraseña, request.form.get('contraseña')):
            return render_template("admin/loginAdmin.html", alert="Contraseña invalida")

        session['id_admin'] = admin.id

        return render_template('admin/homeAdmin.html', success="Ha iniciado sesion como administrador")

    else:
        return render_template('admin/loginAdmin.html')


@admin.route('/admin/users', methods=['GET', 'POST'])
def users_all():

    if request.method == 'POST':
        return redirect(url_for('admin.buscar', format='userinfo', name=request.form.get('nombre')))

    else:
        users = User.query.all()

        return render_template('admin/users_all.html', users=users)


@admin.route('/admin/users/data', methods=['GET', 'POST'])
def users_data():
   
    if request.method == 'POST':

        return redirect(url_for('admin.buscar', format='userdata', name=request.form.get('nombre')))

    else:

        users = db.session.query(User, UserDato).join(
            UserDato, User.id == UserDato.id_usuario).order_by(User.nombre.asc()).all()

        return render_template('admin/data_users.html', users=users)


@admin.route('/buscar/<format>/<name>')
def buscar(format, name):

    if format == 'userinfo':

        user = User.query.filter_by(nombre=name).first()

        if not user:
            return redirect(url_for('admin.users_all'))

        return render_template('admin/user.html', user=user)

    if format == 'userdata':
        user = db.session.query(User, UserDato).join(UserDato,
                User.id == UserDato.id_usuario).filter(User.nombre == name).all()

        name = User.query.filter_by(nombre=name).first()

        if not user or not name:
            return redirect(url_for('admin.users_data'))

        return render_template('admin/userdata.html', user=user, name=name.nombre)


@admin.route('/admin/users/edit/<int:id>')
def edit(id):
    user = User.query.get_or_404(id)
    return render_template('admin/edit.html', user=user)


@admin.route('/admin/users/update/<int:id>', methods=['POST'])
def update(id):
    # Obtenemos los datos del usuario
    user = User.query.get_or_404(id)

    # Actualizamos los datos con los nuevos ingresados por el usuario
    user.nombre = request.form.get('nombre')
    user.edad = request.form.get('edad')
    user.usuario = request.form.get('usuario')
    user.correo = request.form.get('correo')

    # Insertamos en la base el nuevo registro
    db.session.add(user)
    db.session.commit()
    db.session.close()

    return redirect(url_for('admin.users_all'))


@admin.route('/admin/users/update/<int:id>')
def delete(id):

    # Obtenemos los datos del usuario
    user = User.query.get_or_404(id)

    # Eliminamos al usuario de la base de datos
    db.session.delete(user)
    db.session.commit()
    db.session.close()
    return redirect(url_for('admin.users_all'))


@admin.route('/download/<format>')
def download_file(format):

    if format == 'usersall':
        name = 'Users_All'
        users_all = User.query.with_entities(
            User.nombre, User.edad, User.usuario, User.correo).all()

        try:
            excel(users_all, name)

            return send_file(f'archivos/{name}.xlsx', as_attachment=True)

        except:
            return redirect(url_for('admin.users_all'))

    if format == 'usersdata':
        name = 'Users_Data'
        users_data = db.session.query(User, UserDato).join(UserDato,
        User.id == UserDato.id_usuario).with_entities(User.nombre, User.edad, UserDato.bpm, UserDato.fecha).all()

        try:
            excel(users_data, name)

            return send_file(f'archivos/{name}.xlsx', as_attachment=True)

        except:
            return redirect(url_for('admin.users_data'))


@admin.route('/download/user/<name>')
def download_datauser(name):

    users_data = db.session.query(User, UserDato).join(UserDato,
                User.id == UserDato.id_usuario).filter(User.nombre == name).with_entities(
                User.nombre,User.edad, UserDato.bpm, UserDato.fecha).all()
    try:
        name = name.split(' ')
        name = "".join(name)
        excel(users_data, f'Data-{name}')

        return send_file(f'archivos/Data-{name}.xlsx', as_attachment=True)

    except:
        return redirect(url_for('admin.users_data'))
