# Hera 

### Hera se trata de una aplicación web hecha en Flask con ayuda de mysql y la librería de Arduino [SparkFun_MAX3010x](https://github.com/sparkfun/SparkFun_MAX3010x_Sensor_Library), la cual mide la frecuencia cardíaca de una persona. Así mismo permite visualizar todos sus registros.

## Funcionamiento
En Hera una persona puede registrase o loguearse y posteriormente será redirigido a la página de inicio. Está constara con un menú navegable en la cuál tendrá a disposición páginas como "Medición". "Historial" y "Tutorial". En la página de medición contará con un bontón que al darle click hará la petición a la aplicación y está lo redirigerá a una página en la cual se le mostrara su medición. De no ser así le alertara del error. Además en la página de historial podrá ver cada uno de sus registros. Sin embargo, si la persona no conoce sobre como usar la aplicación en la página de "Tutorial" podrá ver cuáles son los pasos para realizar una medición.

Por otra parte, Hera utiliza la librería pyserial de python para leer los datos del puerto serial de la computadora para mandarlo a la aplicación y luego ser guardados en la base de datos. Para esto se ha hecho uso de la librería de Arduino SparkFun_MAX3010x y se ha modificado uno de sus ejemplos __"Example5_HeartRate.ino"__ y unicamente se ha modifica para adaptarlo al proyecto, el codigo y su esquema lo encontraras en la parte de uso.

## Uso 

``` bash
git clone https://github.com/ManuelC09/Hera.git
```
Te aparecerán estas carpetas:
``` bash
Arduino
Hera
```
En la carpeta de Arduino encontraras el codigo del arduino y una foto del esquema de conexiones.

En la carpeta de Hera encontraras estas carpetas y archivos:
``` bash
Hera
config.py
requeriments.txt
run.py
```
Ejecuta en la consola
``` bash
pip install requeriments.txt
```
Luego abre el archivo __config.py__ y agregale la configuración de tu base de datos
``` python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://#user:password:@host:/name' 
```
Una vez hecho esto abre la carpeta de Hera
``` bash
cd Hera
```
Verás estas carpetas y archivos
``` bash
admin
archivos
medicion
static
templates
users
__init__.py
helpers.py
views.py
```

Abre el archivo de __init.py__ y realiza estás configuraciones
``` python
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = #'Tu correo'
app.config["MAIL_PASSWORD"] = #'Tu contraseña'
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail = Mail(app)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = #'Tu Secret Key'

Session(app) 
```
Luego de eso abre el archivo __helpers.py__ y modifica esto:

``` python
serialArduino = serial.Serial('COM3', 9600)
```
Asegurate de saber en que puerto está conectado el Arduino, si esta conectado en el puerto __COM3__ dejalo de esa manera. Si no es así modificalo.

Luego cambia esto:
``` python
if len(argv) == 4:
        msg = Message(argv[0], sender= 'tu correo',
                      recipients=[argv[1]])

if len(argv) == 4:
        msg = Message(argv[0], sender= 'tu correo',
                      recipients=[argv[1]])
```
Donde aparece __sender = 'tu correo'__ cambialo por tu correo. 

Una vez, hecho realizado todos estos cambios ejecuta  en la terminal o consola;

``` bash
python run.py
```
Te aparcerá esto:
``` bash
* Serving Flask app 'Hera'
* Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5000
Press CTRL+C to quit
* Restarting with stat
* Debugger is active!
```
Abre http://127.0.0.1:5000 en el navegador y listo. 

## Administrador
Hera tiene un apartado de administrador que estará a cargo de las personas que deseen administrar el sitio. En este apartado el administradir podrá ver datos de todos los usuarios registrados, y los registros de medición que se han hecho. También, tendrá a disposición la opci+on de descargar los datos en un archivo Excel.

Para acceder a la ruta de admin primeramente debes registrar un usuario. Para registrar un nuevo usuario pudes seguir el siguiente ejemplo:

``` bash
cd Hera/Hera/admin
```

Luego de abrir esa ruta, si haces un ls podrás ver estos archivos:
``` bash
ls

```
``` bash
__init__.py
models.py
views.py

```

Ahora abre el archivo __views.py__ y modifica este apartado
``` python
from werkzeug.security import check_password_hash, generate_password_hash

admin = Admin('usuario', generate_password_hash('contraseña'))
db.session.add(admin)
db.session.commit()
```

Este código lo podras ver en la funcion "admin_login()"
``` python
@admin.route('/admin', methods=['GET', 'POST'])
@admin.route('/adminlogin', methods=['GET', 'POST'])
def admin_login():
```
En este  archivo __views.py__ podrás ver cuales son todas las rutas.

## Nota
Asegurate de subir el código de arduino y realiza bien las conexiones. Una vez, ya hayas subido el código no habras el monitor serial ya que puede existir un conflicto con la librería de Python __pyserial__.

Si no posees el sensor MAX3010x y posees otro, puedes cambiar el código del Arduino y adaptarlo de tal manera de que en el Monitor Serial solo muestre el valor del los bpm. 

Recuerda el en el código de Python solo se leen los datos del puerto.

## Agradecimientos
- [SparkFun_MAX3010x_Sensor_Library](https://github.com/sparkfun/SparkFun_MAX3010x_Sensor_Library)
