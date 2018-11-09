from django.contrib.auth import authenticate, logout
from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from .models import Usuario, Detalles_Personales, Pizza, Pizza_Tradicional, Sesion, Tamano, Tamano_Masa, Tamano_Borde, Tamano_Ingrediente
from .models import Combos_Promocionales, Combinacion, Combinacion_Pizza, Combinacion_Adicional, Promocion, Componente, Pizza_Tamano_Ingrediente, Porcion
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
def ver_usuario(request):
    token = request.GET.get('TOKEN', None)
    usuario_id = utils.getUsuarioIdConToken(token)
    if request.method == "GET" and usuario_id:
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
def editar_usuario(request):
    body = utils.request_todict(request)
    token = body.get('TOKEN', None)
    nombres = body.get("NOMBRES",None)
    apellidos = body.get("APELLIDOS",None)
    correo = body.get("CORREO",None)
    telefono = body.get("TELEFONO",None)
    cedula = body.get("CEDULA",None)

    usuario_id = utils.getUsuarioIdConToken(token)

    if not token or not nombres or not apellidos or not correo or not telefono or not cedula:
        return JsonResponse({
            'STATUS' : 'ERROR',
            'CODIGO' : 4,
            'DETALLE' : 'El json no cumple la estructura'
        })
    elif request.method == "POST" and usuario_id:
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
                    "COSTO" : "%.2f" % float(pizza.costo),
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

##TAMAÑOS
def tamanos(request):
    token = request.GET.get('TOKEN', None)
    if request.method == "GET" and utils.verificarToken(token):
        tamanos = Tamano.objects.all()
        paquete = []
        for tamano in tamanos:
            nombre = tamano.nombre
            if nombre == "PEQUENO":
                nombre = "PEQUEÑA"
            elif nombre == "MEDIANO":
                nombre = "MEDIANA"
            nombre = nombre.capitalize()
            paquete.append({
                "ID" : tamano.id,
                "NOMBRE" : nombre,
                "NOMBRE_BASE" : tamano.nombre
                })
        return JsonResponse({
                'STATUS' : 'OK',
                'CODIGO' : 19,
                'TAMANOS' : paquete,
                'DETALLE' : 'Solicitud correcta'
                }) 
    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })

def tamano_masa(request):
    token = request.GET.get('TOKEN', None)
    tamano = request.GET.get('TAMANO', None)
    if request.method == "GET" and utils.verificarToken(token) and tamano:
        try:
            tamano_model = Tamano.objects.get(nombre=tamano)
            tamanos_masas = Tamano_Masa.objects.filter(tamano=tamano_model)
            masas = {}
            for t_m in tamanos_masas:
                masas[t_m.id] = {
                    'NOMBRE' : t_m.masa.nombre,
                    'DESCRIPCION' : t_m.masa.descripcion,
                    'TAMANO' : t_m.tamano.nombre,
                    'COSTO' : "%.2f" % float(t_m.costo )
                }
            return JsonResponse({
                'STATUS' : 'OK',
                'CODIGO' : 19,
                'MASAS' : masas,
                'DETALLE' : 'Solicitud correcta'
                }) 
        except Exception as e:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 18,
                'DETALLE' : 'Tamaño incorrecto'
                }) 

    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })

def tamano_borde(request):
    token = request.GET.get('TOKEN', None)
    tamano = request.GET.get('TAMANO', None)
    if request.method == "GET" and utils.verificarToken(token) and tamano:
        try:
            tamano_model = Tamano.objects.get(nombre=tamano)
            tamanos_bordes = Tamano_Borde.objects.filter(tamano=tamano_model)
            bordes = {}
            for t_b in tamanos_bordes:
                bordes[t_b.id] = {
                    'NOMBRE' : t_b.borde.nombre,
                    'DESCRIPCION' : t_b.borde.descripcion,
                    'TAMANO' : t_b.tamano.nombre,
                    'COSTO' : "%.2f" % float(t_b.costo )
                }
            return JsonResponse({
                'STATUS' : 'OK',
                'CODIGO' : 19,
                'BORDES' : bordes,
                'DETALLE' : 'Solicitud correcta'
                }) 
        except Exception as e:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 18,
                'DETALLE' : 'Tamaño incorrecto'
                }) 

    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })

def tamano_ingrediente(request):
    token = request.GET.get('TOKEN', None)
    tamano = request.GET.get('TAMANO', None)
    if request.method == "GET" and utils.verificarToken(token) and tamano:
        try:
            tamano_model = Tamano.objects.get(nombre=tamano)
            tamanos_ingredientes = Tamano_Ingrediente.objects.filter(tamano=tamano_model)
            ingredientes = {}
            for t_i in tamanos_ingredientes:
                ingredientes[t_i.id] = {
                    'NOMBRE' : t_i.ingrediente.nombre,
                    'DESCRIPCION' : t_i.ingrediente.descripcion,
                    'IMAGEN_URL' : IP + t_i.ingrediente.img_url.url,
                    'TAMANO' : t_i.tamano.nombre,
                    'COSTO' : "%.2f" % float(t_i.costo)
                }
            return JsonResponse({
                'STATUS' : 'OK',
                'CODIGO' : 19,
                'INGREDIENTES' : ingredientes,
                'DETALLE' : 'Solicitud correcta'
                }) 
        except Exception as e:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 18,
                'DETALLE' : 'Tamaño incorrecto'
                }) 

    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })

## COMBINACION ##
def crear_combinacion(request):  ## ARREGLAR RESPUESTAS DE ERRORES

    ## FALTA CREAR TABLA DE PIZZA_INGREDIENTE Y CREAR METODOS PARA CREAR OBJETOS

    body = utils.request_todict(request)
    token = body.get('TOKEN', None)
    if request.method == "POST" and utils.verificarToken(token):
        pizzas = body.get('PIZZAS', None)
        adicionales = body.get('ADICIONALES', None)

        for pizza in pizzas:
            tamano = pizza.get("TAMANO", None)
            masa_t_id = pizza.get("MASA", None)


            crear(self, tamano, masa, borde, nombre, descripcion, img_url)

        else: 
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 15,
                'DETALLE' : 'Error de solicitud'
                })



##COMBOS PROMOCIONALES
def combos_promocionales(request):
    token = request.GET.get('TOKEN', None)
    if request.method == "GET" and utils.verificarToken(token):
        combos = Combos_Promocionales.objects.all()
        paquete = {}
        for combo in combos:
            combinaciones_pizzas = Combinacion_Pizza.objects.filter(combinacion=combo.combinacion)
            combinaciones_adicionales = Combinacion_Adicional.objects.filter(combinacion=combo.combinacion)
            combo_dict = {}
            comb_pizza_dict = {}
            comb_adic_dict = {}

            for c in combinaciones_pizzas:
                comb_pizza_dict[c.id] = {
                    'NOMBRE' : c.pizza.nombre,
                    'DESCRIPCION' : c.pizza.descripcion,
                    'IMAGEN_URL' : IP + c.pizza.img_url.url,
                    'CANTIDAD' : c.cantidad
                }
            for c in combinaciones_adicionales: 
                comb_adic_dict[c.id] = {
                    'NOMBRE' : c.adicional.nombre,
                    'DESCRIPCION' : c.adicional.descripcion,
                    'IMAGEN_URL' : IP + c.adicional.img_url.url,
                    'CANTIDAD' : c.cantidad
                }
            if len(combinaciones_pizzas) > 0:
                combo_dict['PIZZAS'] = comb_pizza_dict
            if len(combinaciones_adicionales) > 0:
                combo_dict['ADICIONALES'] = comb_adic_dict

            combo_dict['NOMBRE'] = combo.nombre
            combo_dict['DESCRIPCION'] = combo.descripcion
            combo_dict['COSTO'] = "%.2f" % float(combo.costo)
            combo_dict['IMAGEN_URL'] = IP + combo.img_url.url
            
            paquete[combo.id] = combo_dict
           

        return JsonResponse({
                'STATUS' : 'OK',
                'CODIGO' : 19,
                'COMBOS' : paquete,
                'DETALLE' : 'Solicitud correcta'
                })         
    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })

# def ver_combo_promocional(request):
#     token = request.GET.get('TOKEN', None)
#     combo_id = request.GET.get('COMBO_ID', None)
#     if request.method == "GET" and utils.verificarToken(token) and combo_id:
#         try:
#             paquete = {}
#             combo = Combos_Promocionales.objects.get(pk=combo_id)
#             combinaciones_pizzas = Combinacion_Pizza.objects.filter(combo=combo)
#             combinaciones_adicionales = Combinacion_Adicional.objects.filter(combo=combo)
#         except:
#             return JsonResponse({
#                 'STATUS' : 'ERROR',
#                 'CODIGO' : 20,
#                 'DETALLE' : 'El combo promocional no existe'
#                 })

#     return JsonResponse({
#         'STATUS' : 'ERROR',
#         'CODIGO' : 15,
#         'DETALLE' : 'Error de solicitud'
#         })


## PROMOCION
def promociones(request):
    token = request.GET.get('TOKEN', None)
    if request.method == "GET" and utils.verificarToken(token):
        promociones = Promocion.objects.all()
        paquete = {}
        for p in promociones:
            paquete[p.id] = {
                'NOMBRE' : p.nombre,
                'DESCRIPCION' : p.descripcion,
                'IMAGEN_URL' : IP + p.img_url.url,
                'COSTO' : "%.2f" % float(p.costo)
            }
        return JsonResponse({
                'STATUS' : 'OK',
                'CODIGO' : 19,
                'COMBOS' : paquete,
                'DETALLE' : 'Solicitud correcta'
                }) 

    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })

## PORCION
def porciones(request):
    token = request.GET.get('TOKEN', None)
    if request.method == "GET" and utils.verificarToken(token):
        porciones = Porcion.objects.all()
        paquete = []
        for porcion in porciones:
            paquete.append({
                "ID" : porcion.id,
                "NOMBRE" : porcion.nombre.capitalize(),
                "VALOR" : porcion.valor
                })
        return JsonResponse({
                'STATUS' : 'OK',
                'CODIGO' : 19,
                'PORCIONES' : paquete,
                'DETALLE' : 'Solicitud correcta'
                }) 
    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })

##  ADICIONALES
def adicionales(request):
    token = request.GET.get('TOKEN', None)
    tipo = request.GET.get('TIPO', None)
    if request.method == "GET" and utils.verificarToken(token) and tipo:
        adicionales = Componente.objects.filter(tipo=tipo)
        if len(adicionales) > 0:
            paquete = []
            for adicional in adicionales:
                paquete.append({
                    "ID" : adicional.id,
                    "NOMBRE" : adicional.nombre.capitalize(),
                    "COSTO" : "%.2f" % float(adicional.costo),
                    "IMAGEN_URL" : IP + adicional.img_url.url
                    })
            return JsonResponse({
                    'STATUS' : 'OK',
                    'CODIGO' : 19,
                    'PORCIONES' : paquete,
                    'DETALLE' : 'Solicitud correcta'
                    }) 
        else:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 21,
                'DETALLE' : 'Tipo de adicional incorrecto'
                })
    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })    












