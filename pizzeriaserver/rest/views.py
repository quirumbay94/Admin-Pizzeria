from django.contrib.auth import authenticate, logout
from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from .models import *
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
        correo = request.POST.get('CORREO', None)
        contrasena = request.POST.get('CONTRASENA', None)
        nombres = request.POST.get('NOMBRES', None)
        apellidos = request.POST.get('APELLIDOS', None)
        cedula = request.POST.get('CEDULA', None)
        telefono = request.POST.get('TELEFONO', None)
        imagen = request.FILES.get('IMAGEN', None)

        try:
            if correo and contrasena and nombres and apellidos and cedula and telefono:  # EXITO
                usuario = Usuario.objects.create_user(correo, correo, contrasena)
                detalles_personales = Detalles_Personales().crear(usuario, nombres, apellidos, correo, cedula, telefono)
                detalles_personales.imagen = imagen
                detalles_personales.save()
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

## PIZZA ##
def ver_pizza(request):
    token = request.GET.get('TOKEN', None)
    pizza_id = request.GET.get('PIZZA_ID', None)
    if request.method == "GET" and utils.verificarToken(token) and pizza_id:
        try:
            pizza = Pizza.objects.get(pk=pizza_id)
            ingredientes = Pizza_Tamano_Ingrediente.objects.filter(pizza=pizza)
            ingredientes_dic = []
            for i in ingredientes:
                ingredientes_dic.append({
                    "ID" : i.tamano_ingrediente.id,
                    "NOMBRE" : i.tamano_ingrediente.ingrediente.nombre,
                    "DESCRIPCION" : i.tamano_ingrediente.ingrediente.descripcion,
                    "IMAGEN_URL" :  IP + i.tamano_ingrediente.ingrediente.img_url.url,
                    "TAMANO" : i.tamano_ingrediente.tamano.nombre,
                    "PORCION" : i.porcion.nombre,
                    "COSTO" : "%.2f" % float(i.tamano_ingrediente.costo)
                    })
            pizza_dic = {
                "ID" : pizza.id,
                "NOMBRE" : pizza.nombre,
                "TAMANO" : pizza.tamano.nombre,
                "MASA" : {
                    "ID" : pizza.masa.masa.id,
                    "NOMBRE" : pizza.masa.masa.nombre,
                    "TAMANO" : pizza.masa.tamano.nombre,
                    "COSTO" : "%.2f" % float(pizza.masa.costo)
                },
                "BORDE" : {
                    "ID" : pizza.borde.borde.id,
                    "NOMBRE" : pizza.borde.borde.nombre,
                    "TAMANO" : pizza.borde.tamano.nombre,
                    "COSTO" : "%.2f" % float(pizza.borde.costo)
                },
                "INGREDIENTES" : ingredientes_dic
            }
            return JsonResponse({
                'STATUS' : 'OK',
                'CODIGO' : 19,
                'PIZZA' : pizza_dic,
                'DETALLE' : 'Solicitud correcta'
            })
        except Exception as e:
            print(e)
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 14,
                'DETALLE' : 'La pizza no existe'
                })
    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })


## PIZZAS FAVORITAS ##
def pizzas_favoritas(request):
    token = request.GET.get('TOKEN', None)
    if request.method == "GET" and utils.verificarToken(token):
        usuario = utils.getUsuarioConToken(token)
        pizzas_fav = Pizza_Favorita.objects.filter(usuario=usuario)
        paquete = []
        if len(pizzas_fav) > 0:
            for pizza_f in pizzas_fav:
                img_url = None
                if pizza_f.pizza.img_url:
                    img_url = IP + pizza_f.pizza.img_url.url
                paquete.append({
                    "PIZZA_ID" : pizza_f.pizza.id,
                    "NOMBRE" : pizza_f.pizza.nombre,
                    "TAMANO" : pizza_f.pizza.tamano.nombre,
                    "IMAGEN_URL" : img_url
                    })
            return JsonResponse({
                    'STATUS' : 'OK',
                    'CODIGO' : 19,
                    'PIZZAS_FAVORITAS' : paquete,
                    'DETALLE' : 'Solicitud correcta'
                })
        else:
            return JsonResponse({
                    'STATUS' : 'OK',
                    'CODIGO' : 22,
                    'DETALLE' : 'No existen pizzas favoritas para este usuario'
                })
    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })

@csrf_exempt
def crear_pizza_favorita(request):
    body = utils.request_todict(request)
    token = body.get('TOKEN', None)
    if request.method == "POST" and utils.verificarToken(token):
        usuario = utils.getUsuarioConToken(token)
        pizza_id = body.get('PIZZA_ID', None)
        pizza_id_para_retornar = None
        try:
            if pizza_id:
                ##RECUPERANDO ID DE PIZZA
                pizza_obj = Pizza.objects.get(pk=pizza_id).id

                ##CREANDO PIZZA FAVORITA
                pizza_favorita = Pizza_Favorita().crear_con_id(pizza_obj, usuario)
                if not pizza_favorita:
                    return JsonResponse({
                    'STATUS' : 'ERROR',
                    'CODIGO' : 24,
                    'DETALLE' : 'Error guardando pizza favorita'
                    })
            else: 
                pizza = body.get('PIZZA', None)
                nombre = body.get('NOMBRE', None)

                ##CREANDO COMBINACION
                usuario = utils.getUsuarioConToken(token)
                combinacion = Combinacion().crear(nombre, usuario)

                ##OBTENIENDO INFO DE LA PIZZA
                tamano = pizza.get("TAMANO", None)
                masa_t_id = pizza.get("MASA", None)
                borde_t_id = pizza.get("BORDE", None)
                cantidad = 1
                ingredientes = pizza.get("INGREDIENTES", None)

                ##CREANDO PIZZA
                pizza_obj = Pizza().crear_simple(tamano, masa_t_id, borde_t_id, nombre)

                ##CREANDO COMBINACION CON PIZZA
                Combinacion_Pizza().crear(combinacion, pizza_obj, cantidad)

                for diccionario in ingredientes:
                    ##CREANDO PIZZA_TAMANO_INGREDIENTE
                    t_ingrediente = diccionario.get("ID", None)
                    porcion = diccionario.get("PORCION", None)
                    pizza_t_ingrediente = Pizza_Tamano_Ingrediente().crear(pizza_obj, t_ingrediente, porcion)
                
                ##CREANDO PIZZA FAVORITA
                pizza_favorita = Pizza_Favorita().crear(pizza_obj, usuario)
                pizza_id_para_retornar = pizza_favorita.pizza.id
                if not pizza_favorita:
                    return JsonResponse({
                    'STATUS' : 'ERROR',
                    'CODIGO' : 24,
                    'DETALLE' : 'Error guardando pizza favorita'
                    })

            return JsonResponse({
                    'STATUS' : 'OK',
                    'CODIGO' : 19,
                    'DETALLE' : 'Solicitud correcta',
                    'ID' : pizza_id_para_retornar
                    }) 
        except Exception as e:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 15,
                'DETALLE' : 'Error de solicitud'
            })
    else: 
        return JsonResponse({
            'STATUS' : 'ERROR',
            'CODIGO' : 15,
            'DETALLE' : 'Error de solicitud'
            })

@csrf_exempt
def borrar_pizza_favorita(request):
    body = utils.request_todict(request)
    token = body.get('TOKEN', None)
    if request.method == "POST" and utils.verificarToken(token):
        pizza_id = body.get('PIZZA_ID', None)
        try:
            pizza_obj = Pizza.objects.get(pk=pizza_id)
            pizzas_favoritas = Pizza_Favorita.objects.filter(pizza=pizza_obj)
            pizzas_tracionales = Pizza_Tradicional.objects.filter(pizza=pizza_obj)

            if len(pizzas_tracionales) > 0:
                for p in pizzas_favoritas:
                    p.delete()
            else:
                pizza_obj.delete()
            
            return JsonResponse({
                'STATUS' : 'OK',
                'CODIGO' : 19,
                'DETALLE' : 'Solicitud correcta'
            }) 

        except Exception as e:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 15,
                'DETALLE' : 'Error de solicitud'
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
        paquete = []
        if len(pizzas) > 0:
            for pizza in pizzas:
                ##VERIFICANDO SI LA PIZZA ES FAVORITA DEL USUARIO
                usuario = utils.getUsuarioConToken(token)
                pizza_fav = Pizza_Favorita.objects.filter(usuario=usuario).filter(pizza=pizza.pizza)
                es_fav = 0
                if len(pizza_fav) > 0:
                    es_fav = 1
                paquete.append({
                    "ID" : pizza.pizza.id,
                    "NOMBRE" : pizza.pizza.nombre,
                    "IMAGEN_URL" : IP + pizza.pizza.img_url.url,
                    "DESCRIPCION" : pizza.pizza.descripcion,
                    "TAMANO" : pizza.pizza.tamano.nombre.capitalize(),
                    "COSTO" : "%.2f" % float(pizza.costo),
                    "FAVORITA" : es_fav
                })

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
            tamano_model = Tamano.objects.get(pk=tamano)
            tamanos_masas = Tamano_Masa.objects.filter(tamano=tamano_model)
            masas = []
            for t_m in tamanos_masas:
                masas.append({
                    'ID' : t_m.id,
                    'NOMBRE' : t_m.masa.nombre,
                    'DESCRIPCION' : t_m.masa.descripcion,
                    'TAMANO' : t_m.tamano.nombre,
                    'COSTO' : "%.2f" % float(t_m.costo )
            }) 
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
            tamano_model = Tamano.objects.get(pk=tamano)
            tamanos_bordes = Tamano_Borde.objects.filter(tamano=tamano_model)
            bordes = []
            for t_b in tamanos_bordes:
                bordes.append({
                    'ID' : t_b.id,
                    'NOMBRE' : t_b.borde.nombre,
                    'DESCRIPCION' : t_b.borde.descripcion,
                    'TAMANO' : t_b.tamano.nombre,
                    'COSTO' : "%.2f" % float(t_b.costo )
                })
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
            tamano_model = Tamano.objects.get(pk=tamano)
            tamanos_ingredientes = Tamano_Ingrediente.objects.filter(tamano=tamano_model)
            ingredientes = []
            for t_i in tamanos_ingredientes:
                ingredientes.append({
                    'ID' : t_i.id,
                    'NOMBRE' : t_i.ingrediente.nombre,
                    'DESCRIPCION' : t_i.ingrediente.descripcion,
                    'IMAGEN_URL' : IP + t_i.ingrediente.img_url.url,
                    'TAMANO' : t_i.tamano.nombre,
                    'COSTO' : "%.2f" % float(t_i.costo)
                })
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
@csrf_exempt
def crear_combinacion(request):  ## ARREGLAR RESPUESTAS DE ERRORES
    body = utils.request_todict(request)
    token = body.get('TOKEN', None)
    if request.method == "POST" and utils.verificarToken(token):
        try: 
            pizzas = body.get('PIZZAS', None)
            adicionales = body.get('ADICIONALES', None)

            ##CREANDO COMBINACION
            usuario = utils.getUsuarioConToken(token)
            combinacion = Combinacion().crear(None, usuario)

            ##ITERANDO LISTA DE PIZZAS PARA CREARLAS
            for pizza in pizzas:
                id_pizza = pizza.get("ID", None)
                cantidad = pizza.get("CANTIDAD", None)
                if id_pizza and cantidad:
                    ##OBTENIENDO OBJETO DE PIZZA
                    pizza_obj = Pizza.objects.get(pk=id_pizza)

                    ##CREANDO COMBINACION CON PIZZA
                    Combinacion_Pizza().crear(combinacion, pizza_obj, cantidad)
                else:
                    nombre = pizza.get("NOMBRE", "Pizza")
                    tamano = pizza.get("TAMANO", None)
                    masa_t_id = pizza.get("MASA", None)
                    borde_t_id = pizza.get("BORDE", None)
                    cantidad = pizza.get("CANTIDAD", None)
                    ingredientes = pizza.get("INGREDIENTES", None)

                    ##CREANDO PIZZA
                    pizza_obj = Pizza().crear_simple(tamano, masa_t_id, borde_t_id, nombre)


                    ##CREANDO COMBINACION CON PIZZA
                    Combinacion_Pizza().crear(combinacion, pizza_obj, cantidad)

                    for diccionario in ingredientes:
                        ##CREANDO PIZZA_TAMANO_INGREDIENTE
                        t_ingrediente = diccionario.get("ID", None)
                        porcion = diccionario.get("PORCION", None)
                        pizza_t_ingrediente = Pizza_Tamano_Ingrediente().crear(pizza_obj, t_ingrediente, porcion)

            ##ITERANDO LISTA DE ADICIONALES 
            for diccionario in adicionales:
                adicional = diccionario.get("ID", None)
                cantidad = diccionario.get("CANTIDAD", None)

                adicional = Componente.objects.get(pk=adicional)

                ##CREANDO COMBINACION_ADICIONAL
                Combinacion_Adicional().crear(combinacion, adicional, cantidad)

            ##AÑANDIENDO ARTICULOS AL CARRITO
            carrito = utils.getCarritoConToken(token)
            DetalleCarrito().crear(combinacion, carrito)


            return JsonResponse({
                    'STATUS' : 'OK',
                    'CODIGO' : 19,
                    'DETALLE' : 'Solicitud correcta'
                    }) 
        except Exception as e:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 25,
                'DETALLE' : e
            })

    else: 
        return JsonResponse({
            'STATUS' : 'ERROR',
            'CODIGO' : 15,
            'DETALLE' : 'Error de solicitud'
            })

## DETALLE DE CARRITO
def getCarrito(request):
    token = request.GET.get('TOKEN', None)
    if request.method == "GET" and utils.verificarToken(token):
        carrito = utils.getCarritoConToken(token)
        detalles = DetalleCarrito.objects.filter(carrito=carrito)
        pizzas_ARR = []
        adicionales_ARR = []
        for detalle in detalles:
            pizzas = Combinacion_Pizza.objects.filter(combinacion=detalle.combinacion)
            adicionales = Combinacion_Adicional.objects.filter(combinacion=detalle.combinacion)

            ##ITERANDO PIZZAS
            for pizza in pizzas:
                ## ESTIMANDO COSTO DE MASA Y BORDE
                costo = 0
                costo += pizza.pizza.masa.costo
                costo += pizza.pizza.borde.costo

                ingredientes_ARR = []
                ingredientes = Pizza_Tamano_Ingrediente.objects.filter(pizza=pizza.pizza)
                for ingrediente in ingredientes:
                    ## ESTIMANDO COSTO DE INGREDIENTES
                    costo += (ingrediente.tamano_ingrediente.costo * ingrediente.porcion.valor)
                    ingredientes_ARR.append(ingrediente.tamano_ingrediente.ingrediente.nombre.capitalize() + " " + utils.porcionToString(ingrediente.porcion))
                pizzas_ARR.append({
                    "ID" : pizza.id,
                    "NOMBRE" : pizza.pizza.nombre,
                    "TAMANO" : utils.tamanoToFemeninoCapitalize(pizza.pizza.tamano.nombre),
                    "CANTIDAD" : pizza.cantidad,
                    "MASA" : pizza.pizza.masa.masa.nombre.capitalize(),
                    "BORDE" : pizza.pizza.borde.borde.nombre.capitalize(),
                    "INGREDIENTES" : ingredientes_ARR,
                    "COSTO" : "%.2f" % float(costo),
                    "TIPO" : "PIZZA"
                    })
            
            for adicional in adicionales:
                tamano_adicional = Tamano_Ingrediente.objects.filter(ingrediente=adicional.adicional)[0]
                costo = 0
                if tamano_adicional:
                    costo += tamano_adicional.costo
                adicionales_ARR.append({
                    "ID" : adicional.id,
                    "NOMBRE" : adicional.adicional.nombre,
                    "CANTIDAD" : adicional.cantidad,
                    "IMAGEN_URL" : IP + adicional.adicional.img_url.url,
                    "COSTO" : "%.2f" % float(costo),
                    "TIPO" : "ADICIONAL"
                    })

        paquete = {
            "PIZZAS" : pizzas_ARR,
            "ADICIONALES" : adicionales_ARR
        }
        return JsonResponse({
            'STATUS' : 'OK',
            'CODIGO' : 19,
            'CARRITO' : paquete,
            'DETALLE' : 'Solicitud correcta'
        }) 
    
    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        })

@csrf_exempt
def borrarDetalleCarrito(request):
    body = utils.request_todict(request)
    token = body.get('TOKEN', None)
    tipo = body.get('TIPO', None)
    elemento_id = body.get('ID', None)
    if request.method == "POST" and utils.verificarToken(token) and tipo and elemento_id:
        try:
            if tipo == "PIZZA" or tipo == "ADICIONAL":
                if tipo == "PIZZA":
                    pizza = Combinacion_Pizza.objects.get(pk=elemento_id)
                    pizza.delete()
                elif tipo == "ADICIONAL":
                    adicional = Combinacion_Adicional.objects.get(pk=elemento_id)
                    adicional.delete()
                return JsonResponse({
                    'STATUS' : 'OK',
                    'CODIGO' : 19,
                    'DETALLE' : 'Solicitud correcta'
                })
            else: ##TIPO DE OBJETO INCORRECTO
                return JsonResponse({
                    'STATUS' : 'ERROR',
                    'CODIGO' : 15,
                    'DETALLE' : 'Error de solicitud'
                })
        except:
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 27,
                'DETALLE' : 'Error eliminando objeto del carrito'
            })
    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
    })
        ##BUSCANDO PERTENENCIA

@csrf_exempt
def editarCantidadCarrito(request):
    body = utils.request_todict(request)
    token = body.get('TOKEN', None)
    cantidad = body.get('CANTIDAD', None)
    tipo = body.get('TIPO', None)
    elemento_id = body.get('ID', None)
    if request.method == "POST" and utils.verificarToken(token) and cantidad and elemento_id and tipo:
        try:
            if tipo == "PIZZAS":
                pizza_combinacion = Combinacion_Pizza.objects.get(pk=elemento_id)
                pizza_combinacion.cantidad = cantidad
                pizza_combinacion.save()
            elif (tipo == "BEBIDAS") or (tipo == "ADICIONALES"):
                adicional_combinacion = Combinacion_Adicional.objects.get(pk=elemento_id)
                adicional_combinacion.cantidad = cantidad
                adicional_combinacion.save()
            return JsonResponse({
                    'STATUS' : 'OK',
                    'CODIGO' : 19,
                    'DETALLE' : 'Solicitud correcta'
                })
        except Exception as e:
            print(e)
            return JsonResponse({
                'STATUS' : 'ERROR',
                'CODIGO' : 26,
                'DETALLE' : 'Error alterando cantidad de objeto en carrito'
            })  
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
        objectos = Componente.objects.filter(tipo=tipo)
        if len(objectos) > 0:
            paquete = []
            for objeto in objectos:
                tamano_componente = Tamano_Ingrediente.objects.filter(ingrediente=objeto)[0]
                paquete.append({
                    "ID" : objeto.id,
                    "NOMBRE" : objeto.nombre.capitalize(),
                    "COSTO" : "%.2f" % float(tamano_componente.costo),
                    "IMAGEN_URL" : IP + objeto.img_url.url
                    })
            return JsonResponse({
                    'STATUS' : 'OK',
                    'CODIGO' : 19,
                    'ADICIONALES' : paquete,
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

##DIRECCIONES DEL CLIENTE
def direcciones_cliente(request):
    token = request.GET.get('TOKEN', None)
    if request.method == "GET" and utils.verificarToken(token):    
        usuario = utils.getUsuarioConToken(token)
        direcciones = Direccion_Cliente.objects.filter(usuario=usuario)
        if len(direcciones)>0:
            paquete = []
            for direccion in direcciones:
                descripcion = None
                if direccion.descripcion:
                    descripcion = direccion.descripcion
                paquete.append({
                    "ID" : direccion.id,
                    "NOMBRE" : direccion.nombre,
                    "DESCRIPCION" : descripcion,
                    "LATITUD" : direccion.latitud,
                    "LONGITUD" : direccion.longitud
                    })
            return JsonResponse({
                        'STATUS' : 'OK',
                        'CODIGO' : 19,
                        'DIRECCIONES' : paquete,
                        'DETALLE' : 'Solicitud correcta'
                        }) 
        else: 
            JsonResponse({
                'STATUS' : 'OK',
                'CODIGO' : 19,
                'DIRECCIONES' : [],
                'DETALLE' : 'Solicitud correcta'
            }) 

    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        }) 

@csrf_exempt
def crear_direccion_cliente(request):
    body = utils.request_todict(request)
    token = body.get('TOKEN', None)
    if request.method == "POST" and utils.verificarToken(token):  
        usuario = utils.getUsuarioConToken(token)
        nombre = body.get('NOMBRE', None)
        descripcion = body.get('DESCRIPCION', None)
        latitud = body.get('LATITUD', None)
        longitud = body.get('LONGITUD', None)

        direccion = Direccion_Cliente().crear(usuario, nombre, descripcion, latitud, longitud)
        if direccion:
            return JsonResponse({
                        'STATUS' : 'OK',
                        'CODIGO' : 19,
                        'DETALLE' : 'Solicitud correcta'
                        }) 

    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        }) 
@csrf_exempt
def borrar_direccion_cliente(request):
    body = utils.request_todict(request)
    token = body.get('TOKEN', None)
    if request.method == "POST" and utils.verificarToken(token):
        direccion_id = body.get('ID', None)
        direccion = Direccion_Cliente().borrar(direccion_id)
        if direccion:
            return JsonResponse({
                        'STATUS' : 'OK',
                        'CODIGO' : 19,
                        'DETALLE' : 'Solicitud correcta'
                        }) 

    return JsonResponse({
        'STATUS' : 'ERROR',
        'CODIGO' : 15,
        'DETALLE' : 'Error de solicitud'
        }) 





