import sys
import os
import pandas as pd
from functools import wraps
from flask import session, request, render_template, redirect, url_for
from flask_mail import Message
import time
import serial

# Configuracion necesaria para que se pueda encontrar HERA

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Hera import mail


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
        https://flask-es.readthedocs.io/patterns/viewdecorators/?highlight=login_required#login-required-decorator

        """
        if session.get('id_usuario') is None:
            return redirect(url_for('users.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def excel(datos, nombre):

    # Convertimos el diccionario a un dataframe de pandas
    df = pd.DataFrame(datos)

    # Nombre de la carpeta en la cual se descargaran los archivos
    carpeta = 'Hera/archivos'

    # Verificamos si ya existe la carpeta
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

    # Definimos la ruta en donde se guardara nuestro archivo
    ruta = carpeta + '/' + nombre + '.xlsx'

    # Convertimos el dataframe en un archivo excel y lo retornamos
    return df.to_excel(ruta, index=False)


# Parametros que recibe -> (Título, Correo, Plantilla HTML, nombre) y otros datos para conveniencia
def Email(*argv):

    # Verificamos si existe un quinto elemento
    if len(argv) == 4:
        msg = Message(argv[0], sender= 'tu correo',
                      recipients=[argv[1]])
        print(argv[2])
        msg.html = render_template(argv[2], nombre=argv[3])
        mail.send(msg)

    if len(argv) == 5:
        msg = Message(argv[0], sender= 'tu correo',
                      recipients=[argv[1]])
        
        msg.html = render_template(argv[2], nombre=argv[3], bpm=argv[4])
        mail.send(msg)


"""
Función que realiza la respectiva medición de los bpm del usuario
la fucion funciona de tal manera que lee el puerto serial de la computadora 
en este caso el 'COM3'. Sin embargo, este puerto puede cambiar así que asegurate 
de saber y modificar el puerto asignado. luego de leer el puerto los datos se asignan a una 
lista en la cual tomaremos los valores que sean unicamente correspondientes y retornamos el 
promedio de los datos leídos

"""


def Arduino(estado):
    # En este caso, para no estar realizando mediciones a cada rato se le asigna un estado

    if estado == 1:
        tiempo = time.time()
        try:
            # NOTA: Si tu arduino esta conectado a un puerto diferente modifica esta parte
            # serialArduino = serial.Serial('Tu Puerto', 9600)
            serialArduino = serial.Serial('COM3', 9600)

            datos = []
            sum = 0
            while ((time.time() - tiempo) < 15):
                bpmArd = serialArduino.readline().decode('ascii').replace('\r\n', '')
                time.sleep(.4)

                # Capturamos unicamente un bpm util, puesto que el sensor también captura datos no ideales
                if bpmArd > 60 and bpmArd < 110:
                    datos.append(int(bpmArd))
                    sum += int(bpmArd)
                
                else:
                    continue

            bpm = int(sum/len(datos))
            print(bpm)

            return bpm

        except:
            return None

    else:
        return None
