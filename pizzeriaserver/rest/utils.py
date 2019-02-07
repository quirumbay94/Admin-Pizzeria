import json
from pyfcm import FCMNotification
from pizzeriaserver.settings import FIREBASE_TOKEN
from rest.models import *

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

##CRITERIO DE ESTADO DE PEDIDO
def getCantidadPizzasPedido(pedido):
    cantidad = 0
    detalles = Detalle_Pedido.objects.filter(pedido=pedido)
    for detalle in detalles:
        combinaciones_pizza = Combinacion_Pizza.objects.filter(combinacion=detalle.combinacion)
        for c in combinaciones_pizza:
            cantidad += c.cantidad
    return cantidad

##CALCULAR TOTAL DEL PEDIDO
def calcularTotal(carrito):
    detalle_carrito = DetalleCarrito.objects.filter(carrito=carrito)
    total = 0.0
    for d_c in detalle_carrito:
        combinacion = d_c.combinacion
        combinaciones_pizza = Combinacion_Pizza.objects.filter(combinacion=combinacion)
        combinaciones_adicional = Combinacion_Adicional.objects.filter(combinacion=combinacion)
        combos = Combos_Promocionales.objects.filter(combinacion=combinacion)

        ##ITERANDO PIZZAS
        for c_p in combinaciones_pizza:
            pizza = c_p.pizza
            cantidad = c_p.cantidad
            pizza_trad = Pizza_Tradicional.objects.filter(pizza=pizza)
            if len(pizza_trad) > 0: ##SI ES QUE LA PIZZA ES PIZZA TRADICIONAL
                total += (pizza_trad[0].costo * cantidad)
            else: ##SI ES QUE LA PIZZA ES ARMADA POR EL CLIENTE
                pizza_t_i = Pizza_Tamano_Ingrediente.objects.filter(pizza=pizza)
                for p_t_i in pizza_t_i: ##CACULANDO COSTO DE INGREDIENTE SEGUN LA PORCION
                    total += (p_t_i.tamano_ingrediente.costo * p_t_i.porcion.valor)
                ##CACULANDO COSTO DE BORDE Y MASA
                total += pizza.masa.costo 
                total += pizza.borde.costo
        ##ITERANDO ADICIONALES
        for c_a in combinaciones_adicional:
            t_a = Tamano_Ingrediente.objects.filter(ingrediente=c_a.adicional)[0]
            total += (t_a.costo * c_a.cantidad)
        ##ITERANDO COMBOS
        for c in combos:
            total += c.costoprint("******TOTAL ACU: " + str(total))
    return total

##ACTUALIZAR CANTIDADES DE CARRITO
def actualizarCantidades(elementos):
    response = True
    for elemento in elementos:
        combinacion_id = elemento.get("ID",None)
        cantidad = elemento.get("CANTIDAD", None)
        tipo = elemento.get("TIPO", None)
        if tipo == "PIZZA":
            c_p = Combinacion_Pizza().editar(combinacion_id, cantidad)
            if not c_p:
                response = False
                break
        elif tipo == "ADICIONAL":
            c_a = Combinacion_Adicional().editar(combinacion_id,cantidad)
            if not c_a:
                response = False
                break
    return response

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
    print("RESULTADO")
    print(result)




