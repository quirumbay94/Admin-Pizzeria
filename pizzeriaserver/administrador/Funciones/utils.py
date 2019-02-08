from rest.models import *
from pyfcm import FCMNotification
from pizzeriaserver.settings import FIREBASE_TOKEN

def limpiarRegistros_Ingredientes(pizza_obj):
    ingredientes = Pizza_Tamano_Ingrediente.objects.filter(pizza=pizza_obj)
    for ingrediente in ingredientes:
        try:
            ingrediente.delete()
        except:
            return False
    return True

def crearPosiciones(posiciones):
    exito = True

    ##BORRANDO TODAS LAS INSTANCIAS ANTERIORES
    Coordenada.objects.all().delete()

    ##CREANDO NUEVAS INSTANCIAS
    for posicion in posiciones:
        p = posicion.split("|")
        lat = p[0]
        lng = p[1]
        coordenada = Coordenada().crear(lat,lng)
        if not coordenada: 
            exito = False
            break
    return exito

def crearPosicion(posicion):
    p = posicion.split("|")
    lat = p[0]
    lng = p[1]
    coordenada = Coordenada().crear(lat,lng)
    return coordenada

def obtenerPedido(pedido_id):
    pedido = Pedido.objects.get(pk=pedido_id)
    detalles = Detalle_Pedido.objects.filter(pedido=pedido)
    pizzas = []
    adicionales = []
    combos_p = []
    for detalle in detalles:
        combinaciones_pizza = Combinacion_Pizza.objects.filter(combinacion=detalle.combinacion)
        combinaciones_adicional = Combinacion_Adicional.objects.filter(combinacion=detalle.combinacion)
        combos = Combinacion_Combo.objects.filter(combinacion=detalle.combinacion)

        ##ITERANDO PIZZAS
        for c_p in combinaciones_pizza:
            pizza_t_i = Pizza_Tamano_Ingrediente.objects.filter(pizza=c_p.pizza)
            ingredientes = []
            for p_t_i in pizza_t_i:
                ingredientes.append({
                    "NOMBRE" : p_t_i.tamano_ingrediente.ingrediente.nombre,
                    "PORCION" : p_t_i.porcion.nombre
                })
            pizzas.append({
                "NOMBRE" : c_p.pizza.nombre,
                "TAMANO" : c_p.pizza.tamano.nombre.capitalize(),
                "CANTIDAD" : c_p.cantidad,
                "INGREDIENTES" : ingredientes
            })
        ##ITERANDO ADICIONALES
        for c_a in combinaciones_adicional:
            adicionales.append({
                "NOMBRE" : c_a.adicional.nombre,
                "CANTIDAD" : c_a.cantidad
            })
        ##ITERANDO COMBOS
        for c in combos:
            combos_p.append({
                "NOMBRE" : c.combo.nombre,
                "DESCRIPCION" : c.combo.descripcion,
                "CANTIDAD" : c.cantidad
            })
    paquete = {
        "PIZZAS" : pizzas,
        "ADICIONALES" : adicionales,
        "COMBOS" : combos_p,
        "TOTAL" : pedido.total,
        "ENTREGADO" : pedido.entregado
    }
    return paquete

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

    result = push_service.notify_single_device(registration_id=token, sound=True, message_title=titulo, message_body=mensaje)


