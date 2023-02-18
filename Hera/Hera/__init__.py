from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


app = Flask(__name__)

# Configuración de la APP
app.config.from_object('config.DevelopmentConfig')

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configuracion de email, en este caso de gmail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = #'Tu correo'
app.config["MAIL_PASSWORD"] = #'Tu contraseña'
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail = Mail(app)

# Sesiones
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = #'Tu Secret Key'
Session(app)

# Configuración de la base de datos
db = SQLAlchemy(app)


# Registrar los decoradores
from Hera.views import base
from Hera.users.views import users
from Hera.medicion.views import medicion
from Hera.admin.views import admin

app.register_blueprint(base)
app.register_blueprint(users)
app.register_blueprint(medicion)
app.register_blueprint(admin)

# Ejecutar todas las consultas 
with app.app_context():
    db.create_all()
