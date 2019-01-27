import json
from pyfcm import FCMNotification
from pizzeriaserver.settings import FIREBASE_TOKEN
from rest.models import Sesion, Carrito, Detalles_Personales

## TRANSFORMANDO REQUEST EN DICCIONARIO
def request_todict(request):
    try: 
        body = request.body.decode('utf-8')
        body = json.loads(body)
        return body
    except:
        return {}

##VERIFICACION DE TOKEN
def verificarToken(token):
    try:
        Sesion.objects.get(token=token)
        return True
    except:
        return False

##OBTENER ID DE USUARIO A TRAVES DEL TOKEN
def getUsuarioIdConToken(token):
    try:
        sesion = Sesion.objects.get(token=token)
        return sesion.usuario.id
    except:
        return False

def getUsuarioConToken(token):
    try:
        sesion = Sesion.objects.get(token=token)
        return sesion.usuario
    except:
        return False

def getCarritoConToken(token):
    try:
        sesion = Sesion.objects.get(token=token)
        usuario = sesion.usuario
        carrito = Carrito.objects.filter(usuario=usuario)[0]
        return carrito
    except:
        return None

def porcionToString(porcion):
    return "X" + str(porcion.valor)

def tamanoToFemeninoCapitalize(tamano):
    if tamano == "PEQUEÑO":
        return "Pequeña"
    elif tamano == "MEDIANO":
        return "Mediana"
    return tamano.capitalize()

def cedulaRepetida(cedula, usuario):
    cedulas = Detalles_Personales.objects.filter(cedula=cedula)
    if len(cedulas) == 0:
        return False
    elif len(cedulas) == 1:
        if usuario == cedulas[0].usuario:
            return False
        else:
            return True
    else:
        return True

##PUSH NOTIFICATION
def enviarPushNot(token, titulo, mensaje):
    push_service = FCMNotification(api_key=FIREBASE_TOKEN)
    
    # try:
    #     sesion = Sesion.objects.get(token=token)
    #     usuario = sesion.usuario
    #     sesiones = Sesion.objects.filter(usuario=usuario)
    #     for sesion in sesiones:
    #         result = push_service.notify_single_device(registration_id=sesion.firebase_id, message_title=titulo,
    #                                            message_body=mensaje)
    #     return True
    # except:
    #     return False
    # Token del dispositivo

    result = push_service.notify_single_device(registration_id=token, message_title=titulo,
                                               message_body=mensaje)
    print("RESULTADO")
    print(result)




