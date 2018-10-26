from django.contrib.auth import authenticate, logout
from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from .models import Usuario, Detalles_Personales, Pizza_Tradicional, Sesion
from rest import utils
import json

IP = "http://navi.pythonanywhere.com"

@csrf_exempt
def login(request):
    if request.method == "POST":
        body = utils.request_todict(request)
        correo = body.get('CORREO', None)
        contrasena = body.get('CONTRASENA', None)

        if correo and contrasena:
            usuario = authenticate(username=correo, password=contrasena)
            if usuario is not None:
                sesion = Sesion().crear(usuario)
                return JsonResponse({
                    'STATUS' : 'OK',
                    'CODIGO' : 1,
                    'TOKEN' : sesion.token,
                    'DETALLE' : 'Inicio de sesión exitoso'
                    })
            elif Usuario.objects.filter(email=correo).count() <= 0:
                return JsonResponse({
                    'STATUS' : 'ERROR',
                    'CODIGO' : 2,
                    'DETALLE' : 'No existe ninguna cuenta asociada a este correo'
                    })
            else: 
                return JsonResponse({
                    'STATUS' : 'ERROR',
                    'CODIGO' : 3,
                    'DETALLE' : 'La contraseña es incorrecta'
                    })
    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })

@csrf_exempt
def login_RS(request):
    body = utils.request_todict(request)
    correo = body.get('CORREO', None)
    nombres = body.get('NOMBRES', None)
    apellidos = body.get('APELLIDOS', None)

    if correo and nombres and apellidos:
        if Usuario.objects.filter(email=correo).count() == 0: ##USUARIO SIN REGISTRAR, SE CREA UNA CUENTA
            usuario = Usuario().crearSinContrasena(correo)
            detalles = Detalles_Personales().crear_simple(usuario, nombres, apellidos, correo)

        ##BUSCANDO EL USUARIO PARA CREARLE UNA SESION
        try: 
            usuario = Usuario.objects.get(email=correo)
            sesion = Sesion().crear(usuario)

            return JsonResponse({
                'STATUS' : 'OK',
                'CODIGO' : 1,
                'TOKEN' : sesion.token,
                'DETALLE' : 'Inicio de sesión exitoso'
                })
        except:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 2,
                'DETALLE' : 'No existe ninguna cuenta asociada a este correo'
                })
    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })

@csrf_exempt
def logout(request):
    body = utils.request_todict(request)
    token = body.get('TOKEN', None)
    if request.method == "POST" and utils.verificarToken(token):
        try:
            if Sesion().logout(token):
                return JsonResponse({
                    'STATUS' : 'OK',
                    'CODIGO' : 0,
                    'DETALLE' : 'Sesión cerrada con éxito '
                    })
        except:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 11,
                'DETALLE' : 'No existe una sesion'
                })
    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })

@csrf_exempt
def registrar(request):
    if request.method == "POST":
        body = utils.request_todict(request)
        correo = body.get('CORREO', None)
        contrasena = body.get('CONTRASENA', None)
        nombres = body.get('NOMBRES', None)
        apellidos = body.get('APELLIDOS', None)
        cedula = body.get('CEDULA', None)
        telefono = body.get('TELEFONO', None)

        try:
            if correo and contrasena and nombres and apellidos and cedula and telefono:  # EXITO
                usuario = Usuario.objects.create_user(correo, correo, contrasena)
                detalles_personales = Detalles_Personales().crear(usuario, nombres, apellidos, correo, cedula, telefono)
                if detalles_personales:
                    sesion = Sesion().crear(usuario)
                    return JsonResponse({
                        'STATUS' : 'OK',
                        'CODIGO' : 10,
                        'TOKEN' : sesion.token,
                        'DETALLE' : 'La cuenta ha sido creada con éxito '
                        })
                else: 
                    return JsonResponse({
                        'STATUS' : 'ERROR',
                        'CODIGO' : 16,
                        'DETALLE' : 'Error creando detalles de usuario'
                        })

            else:
                return JsonResponse({
                        'STATUS' : 'ERROR',
                        'CODIGO' : 4,
                        'DETALLE' : 'El json no cumple la estructura'
                        })
        except(IntegrityError):
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 5,
                'DETALLE' : 'El correo ya se encuentra en uso'
                })
    return JsonResponse({
            'STATUS' : 'ERROR',
            'CODIGO' : 15,
            'DETALLE' : 'Error de solicitud'
            })

## USUARIOS ##
def ver_usuario(request, usuario_id):
    token = request.GET.get('TOKEN', None)
    if request.method == "GET" and utils.verificarToken(token):
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            usuario = Detalles_Personales.objects.get(usuario=usuario)
            return JsonResponse({
                'STATUS' : 'OK',
                'CODIGO' : 7,
                'NOMBRES' : usuario.nombres,
                'APELLIDOS' : usuario.apellidos,
                'CORREO' : usuario.correo,
                'TELEFONO' : usuario.telefono,
                'CEDULA' : usuario.cedula,
                'DETALLE' : 'Usuario valido'
            })

        except:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 8,
                'DETALLE' : 'El usuario no existe'
            })
    return JsonResponse({
            'STATUS' : 'ERROR',
            'CODIGO' : 15,
            'DETALLE' : 'Error de solicitud'
            })

@csrf_exempt
def editar_usuario(request, usuario_id):
    body = utils.request_todict(request)
    token = body.get('TOKEN', None)
    nombres = body.get("NOMBRES",None)
    apellidos = body.get("APELLIDOS",None)
    correo = body.get("CORREO",None)
    telefono = body.get("TELEFONO",None)
    cedula = body.get("CEDULA",None)

    if not token or not nombres or not apellidos or not correo or not telefono or not cedula:
        return JsonResponse({
            'STATUS' : 'ERROR',
            'CODIGO' : 4,
            'DETALLE' : 'El json no cumple la estructura'
        })
    elif request.method == "POST" and utils.verificarToken(token):
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            detalles = Detalles_Personales.objects.get(usuario=usuario)

            ##VERIFICANDO SI EL USUARIO QUIERE CAMBIAR DE CORREO Y EL CORREO ESTA DISPONIBLE
            if usuario.username != correo:
                if Usuario.objects.filter(username=correo).count() >= 1:
                    return JsonResponse({
                        'STATUS' : 'ERROR',
                        'CODIGO' : 5,
                        'DETALLE' : 'El correo ya se encuentra en uso'
                    })
             
            ##TODO ESTA BIEN PARA ALTERAR EL CORREO DEL USUARIO
            usuario.username = correo
            usuario.email = correo
            usuario.save()
                
            ##EDITANDO DATOS DEL USUARIO
            detalles.nombres = nombres
            detalles.apellidos = apellidos
            detalles.correo = correo
            detalles.telefono = telefono
            detalles.cedula = cedula
            detalles.save()
            
            return JsonResponse({
                'STATUS' : 'OK',
                'CODIGO': 9,
                'DETALLE' : 'Los datos fueron actualizados exitosamente'
                })
        except Exception as e:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 8,
                'DETALLE' : 'El usuario no existe'
            })
    return JsonResponse({
            'STATUS' : 'ERROR',
            'CODIGO' : 15,
            'DETALLE' : 'Error de solicitud'
            })

## PIZZAS TRADICIONALES ##
def ver_pizzas_tradicionales(request):
    token = request.GET.get('TOKEN', None)
    if request.method == "GET" and utils.verificarToken(token):
        pizzas = Pizza_Tradicional.objects.all()
        paquete = {}
        if len(pizzas) > 0:
            for pizza in pizzas:
                pizza_tradicional = {
                    "NOMBRE" : pizza.pizza.nombre,
                    "IMAGEN_URL" : IP + pizza.pizza.img_url.url,
                    "DESCRIPCION" : pizza.pizza.descripcion,
                    "COSTO" : "%.2f" % float(pizza.costo)
                }
                paquete[pizza.id] = pizza_tradicional

            return JsonResponse({
                    'STATUS' : 'OK',
                    'CODIGO' : 7,
                    'PIZZAS' : paquete,
                    'DETALLE' : 'Usuario valido'
                })
        else:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 17,
                'DETALLE' : 'No hay pizzas tradicionales por el momento'
                })

    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })






