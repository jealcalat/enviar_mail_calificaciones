'''
archivo_calificaciones tiene las siguientes columnas:
	nombre	                    correo	            sum_exam sum_tareas	total	extra_final
0	Aquilez Baeza Parada    	  fulano@gmail.com	  57.495	 40	        97.495	0.0

Que son usadas en el ciclo for más abajo
'''

import smtplib
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

archivo_calificaciones = pd.read_csv("<directorio>/calificacion_final.csv")

def enviar_mail(from_to, subject, message):
    ''' 
    from_to: lista de dos strings, la primera con el correo de from,
             la segunda con el correo de to 
    subject: asunto del correo (e.g., "Calificaciones finales")
    message: cuerpo del mensaje; ver ejemplo
    '''
    msg = MIMEMultipart()
    msg["From"] = from_to[0]
    msg["To"] = from_to[1]
    msg["Subject"] = subject
    msg.attach(MIMEText(message, 'plain'))
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # TLS para seguridad
    s.starttls()
    # Autenticar:
    # el primer valor es el usuario de gmail, antes del @
    # el segundo valor es la contraseña de la cuenta. 
    # Por ejemplo: my_email@gmail.com, password: cacaBlanda123
    # s.login("my_email", "cacaBlanda123")
    s.login("usuario", "########") 
    # enviar mail
    s.sendmail(from_to[0], from_to[1], msg.as_string())
    # Terminar sesión
    s.quit()
    print(f'Correo enviado a {from_to[1]}')
    return

# Lo convierte en PRIMER_NOMBRE APELLIDO_PATERNO APELLIDO_MATERNO   
def nombre_orden(nombre):
    nombre = ' '.join(nombre.split())
    new_nombre = [i for i in nombre.split(" ")]
    nombre_new = f'{new_nombre[2]} {new_nombre[0]} {new_nombre[1]}'
    return nombre_new.title()

# Ciclo for que itera sobre cada fila de archivo_calificaciones
for i in len(archivo_calificaciones.index):
    # extraer nombre de alumno
    alumno = archivo_calificaciones['nombre'][i]
    alumno = nombre_orden(alumno)
    tareas = archivo_calificaciones['sum_tareas'][i]
    examenes = archivo_calificaciones['sum_exam'][i]
    extra_re = archivo_calificaciones['extra_final'][i]
    total = archivo_calificaciones['total'][i]
    calificacion = total + extra_re
    # crear mensaje
    SUBJECT = "Calificaciones de DTJ"
    INICIO = f'Hola {alumno}:'
    TEXT = '''\
        Calificaciones desglosadas
        ==================================
        Tareas:                   {tareas}.
        Exámenes:               {examenes}.
        Extra (reseña de libro): {extra_re}
        ==================================
        Total: {TOTAL}
    '''
    FINAL = "\nNo contestes a este correo. Se envió de forma automatizada."
    FROM = "jealcalat@gmail.com"
    TO = "jaime.alcala@iteso.mx"

    # Preparar mensaje
    message = '{}\n\n{}\n{}'.format(INICIO, TEXT, FINAL)
    enviar_mail(from_to, SUBJECT, message)
