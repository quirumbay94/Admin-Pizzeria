from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from rest.models import *
from administrador.Funciones import diccionarios, utils

## ERROR ##
def error(request):
    return render(request,"General/error.html")

## REDIRECCION ##
def redireccionar(request):
    if verificarSesion(request):
        return redirect("menu")
    return redirect("login")

## AUTH ##
def verificarSesion(request):
    sesion = request.session.get("SESION",None)
    if sesion:
        return True
    return False

def crearSesion(request,detalles):
    request.session["SESION"] = True
    request.session["DETALLES_PERSONALES"] = {
        'NOMBRE' : detalles.nombres,
        'USUARIO_ID' : detalles.usuario.id
    }

def getUserBySesion(request):
    detalles = request.session.get("DETALLES_PERSONALES", None)
    if detalles:
        usuario_id = detalles.get("USUARIO_ID", None)
        try:
            usuario = Usuario.objects.get(pk=usuario_id)
            return usuario
        except: 
            None
    return None

def login(request):
    if request.method == "POST":
        correo = request.POST.get("correo",None)
        contrasena = request.POST.get("contrasena",None)
        paquete = {}
        if correo and contrasena:
            usuario = authenticate(username=correo, password=contrasena)
            if usuario is not None:
                detalles = Detalles_Personales.objects.get(usuario=usuario)
                crearSesion(request,detalles) ##CREANDO SESION DEL USUARIO
                return redirect("menu")
            else:
                paquete = diccionarios.diccionarioMensaje(paquete, "Correo o contraseña incorrecta")
        else:
            paquete = diccionarios.diccionarioMensaje(paquete, "Correo o contraseña invalida")
        return render(request, "Login/login.html", paquete)
    return render(request, "Login/login.html")

def logout_(request):
    if request.method == "POST":
        logout(request)
        request.session = None
        return redirect("login")
    return redirect("error")

## INDEX ##
def menu(request):
    if verificarSesion(request):
        paquete = diccionarios.diccionarioBarraNav(request,{})
        return render(request,"Menu/menu.html", paquete)
    return redirect("login")

## USUARIOS ##
def usuario(request):
    if verificarSesion(request):
        ##MANEJAR LA ACCION DE HABILITAR O DESABILITAR EL USUARIO
        if request.method == "POST": 
            usuario_id = request.POST.get("USUARIO",None)
            accion = request.POST.get("ACCION",None)
            if usuario_id and accion:
                usuario = Usuario.objects.get(pk=usuario_id) ##BUSCANDO EL USUARIO
                if accion in ["true","True"]:
                    usuario.is_active = True
                else: 
                    usuario.is_active = False
                usuario.save()

        ##DICCIONARIOS CON DATOS PARA EL FRONTEND
        paquete = diccionarios.diccionarioBarraNav(request,{})
        paquete = diccionarios.diccionarioUsuarios(paquete)

        return render(request,"Usuario/usuario.html", paquete)
    return redirect("login")

def ver_usuario(request, usuario_id):
    if verificarSesion(request):
        ##DETALLES PARA LA SUBBARRA DE NAVEGACION
        paquete = diccionarios.diccionarioBarraNav(request,{})
        paquete = diccionarios.diccionarioDatosSubBarraUsuario(paquete,usuario_id)
        return render(request, "Usuario/ver_usuario.html", paquete)
    return redirect("login")

## COMPONENTES ##
def componentes(request, tipo):
    if verificarSesion(request):
        paquete = diccionarios.diccionarioBarraNav(request,{})
        
        if tipo == "INGREDIENTE":
            ingredientes = Componente.objects.filter(tipo="INGREDIENTE").order_by('nombre')
            paquete["INGREDIENTE"] = ingredientes
        elif tipo == "ADICIONAL":
            adicionales = Componente.objects.filter(tipo="ADICIONAL").order_by('nombre')
            paquete["ADICIONAL"] = adicionales
        elif tipo == "BEBIDA":
            bebidas = Componente.objects.filter(tipo="BEBIDA").order_by('nombre')
            paquete["BEBIDA"] = bebidas
        paquete["TIPO"] = tipo.capitalize()
        return render(request,"Componente/componentes.html", paquete)
    return redirect("login")

def nuevo_componente(request, tipo):
    if verificarSesion(request):
        ##DETALLES PARA LA SUBBARRA DE NAVEGACION
        paquete = diccionarios.diccionarioBarraNav(request,{})
        paquete = diccionarios.diccionarioDatosSubBarraComponente(paquete, tipo)
        paquete = diccionarios.diccionarioTamanos(paquete)

        if request.method == "POST":
            tipo = request.POST.get("TIPO",None)
            nombre = request.POST.get("NOMBRE",None)
            descripcion = request.POST.get("DESCRIPCION",None)
            imagen = request.FILES.get("IMAGEN",None)
            estado = True

            ##CREANDO COMPONENTE
            componente = Componente().crear(nombre, descripcion, tipo, imagen, estado)

            if tipo == "INGREDIENTE":
                tamanos = paquete["TAMANOS"]
                costos = []
                for tamano in tamanos:
                    costo = request.POST.get("COSTO_" + tamano.nombre, None)
                    costos.append({"TAMANO_ID" : tamano.id, "COSTO" : costo})
                
                verificador_TI_creado = True
                for costo in costos:
                    t_i = Tamano_Ingrediente().crear(costo["TAMANO_ID"], componente, costo["COSTO"])
                    if not t_i:
                        verificador_TI_creado = False
                        break
                if componente and verificador_TI_creado:
                    paquete = diccionarios.diccionarioMensaje(paquete, "Componente creado con exito.")
                else: 
                    paquete = diccionarios.diccionarioMensaje(paquete, "Error creando componente.")
            else:
                costo = request.POST.get("COSTO",None) 
                t_i = Tamano_Ingrediente().crear_default(componente, costo)
                if componente and t_i:
                    paquete = diccionarios.diccionarioMensaje(paquete, "Componente creado con exito.")
                else: 
                    paquete = diccionarios.diccionarioMensaje(paquete, "Error creando componente.")
        
        return render(request, "Componente/nuevo_componente.html", paquete)
    return redirect("login")

def ver_componente(request, tipo, componente_id):
    if verificarSesion(request):
        ##DETALLES PARA LA SUBBARRA DE NAVEGACION
        paquete = diccionarios.diccionarioBarraNav(request,{})
        paquete = diccionarios.diccionarioDatosSubBarraComponente(paquete, tipo)

        ##INFORMACION DEL COMPONENTE SELECCIONADO
        paquete = diccionarios.diccionarioDatosComponente(paquete, componente_id)

        return render(request, "Componente/ver_componente.html", paquete)
    return redirect("login")

def editar_componente(request, tipo, componente_id):
    ##DETALLES PARA LA BARRA DE NAV
    paquete = diccionarios.diccionarioBarraNav(request,{})

    if verificarSesion(request):
        if request.method == "POST":
            tipo = request.POST.get("TIPO",None)
            nombre = request.POST.get("NOMBRE",None)
            descripcion = request.POST.get("DESCRIPCION",None)
            imagen = request.FILES.get("IMAGEN",None)
            estado = request.POST.get("ESTADO",None)
            if estado in ["True", "true"]:
                estado = True
            else:
                estado = False

            ##EDITANDO COMPONENTE
            componente = Componente().editar(componente_id, nombre, descripcion, tipo, imagen, estado)
            if tipo == "INGREDIENTE":
                tamanos = Tamano.objects.all()
                costos = []
                if Tamano_Ingrediente().borrar_masivo(componente_id):
                    for tamano in tamanos:
                        costo = request.POST.get("COSTO_" + tamano.nombre, None)
                        costos.append({"TAMANO_ID" : tamano.id, "COSTO" : costo})
                    
                    verificador_TI_creado = True
                    for costo in costos:
                        t_i = Tamano_Ingrediente().crear(costo["TAMANO_ID"], componente, costo["COSTO"])
                        if not t_i:
                            verificador_TI_creado = False
                            break
                    if componente and verificador_TI_creado:
                        paquete = diccionarios.diccionarioMensaje(paquete, "Componente editado con exito.")
                    else: 
                        paquete = diccionarios.diccionarioMensaje(paquete, "Error editando componente.")
                else: 
                    paquete = diccionarios.diccionarioMensaje(paquete, "Error editando componente.")    
            else:
                costo = request.POST.get("COSTO",None) 
                if Tamano_Ingrediente().borrar_masivo(componente_id):
                    t_i = Tamano_Ingrediente().crear_default(componente, costo)
                    if componente and t_i:
                        paquete = diccionarios.diccionarioMensaje(paquete, "Componente editado con exito.")
                    else: 
                        paquete = diccionarios.diccionarioMensaje(paquete, "Error editando componente.")
                else: 
                    paquete = diccionarios.diccionarioMensaje(paquete, "Error editando componente.")


        ##DETALLES PARA LA SUBBARRA DE NAVEGACION
        paquete = diccionarios.diccionarioDatosSubBarraComponente(paquete, tipo)

        ##INFORMACION DEL COMPONENTE SELECCIONADO
        paquete = diccionarios.diccionarioDatosComponente(paquete, componente_id)

        return render(request, "Componente/editar_componente.html", paquete)
    return redirect("login")

## PIZZAS TRADICIONALES
def pizzas_tradicionales(request):
    if verificarSesion(request):
        paquete = diccionarios.diccionarioBarraNav(request,{})
        paquete = diccionarios.diccionarioPizzasTradicionales(paquete)
        return render(request, "Pizza/pizzas_tradicionales.html",paquete)
    return redirect("login")

def ver_pizza_tradicional(request, pizza_t_id):
    if verificarSesion(request):
        ##DETALLES PARA LA SUBBARRA DE NAVEGACION
        paquete = diccionarios.diccionarioBarraNav(request,{})
        paquete = diccionarios.diccionarioDatosSubBarraPizza_T(paquete)

        ##INFORMACION DE PIZZA TRADICIONAL SELECCIONADA
        paquete = diccionarios.diccionarioDatoPizza_T(paquete, pizza_t_id)

        return render(request, "Pizza/ver_pizza_tradicional.html",paquete)
    return redirect("login")

def nueva_pizza_tradicional(request):
    if verificarSesion(request):
        ##DETALLES PARA LA SUBBARRA DE NAVEGACION
        paquete = diccionarios.diccionarioBarraNav(request,{})
        paquete = diccionarios.diccionarioDatosSubBarraPizza_T(paquete)

        ##RECOLECTANDO TIPOS DE MASAS Y BORDES 
        paquete = diccionarios.diccionarioMasasBordesIngredientes(paquete)

        if request.method == "POST":
            usuario = getUserBySesion(request)
            if not usuario:
                paquete = diccionarios.diccionarioMensaje(paquete, "Error obteniendo credenciales de usuario, inicie sesion nuevamente.")
                return render(request, "Pizza/nueva_pizza_tradicional.html",paquete)

            ##OBTENIENDO INFO DE LA PIZZA
            nombre = request.POST.get("NOMBRE",None)
            descripcion = request.POST.get("DESCRIPCION",None)
            costo = request.POST.get("COSTO",None)
            img_url = request.FILES.get("IMAGEN",None)
            tamano_id = request.POST.get("TAMANO",None)
            masa_t_id = request.POST.get("MASA",None)
            borde_t_id = request.POST.get("BORDE",None)
            ingredientes = request.POST.getlist("INGREDIENTES[]", None)
            porciones = request.POST.getlist("PORCIONES[]", None)
            cantidad = 1


            ##CREANDO COMBINACION
            combinacion = Combinacion().crear(nombre, usuario)
            if not combinacion:
                paquete = diccionarios.diccionarioMensaje(paquete, "Error creando pizza.")
                return render(request, "Pizza/nueva_pizza_tradicional.html",paquete)

            ##CREANDO PIZZA
            pizza_obj = Pizza().crear(tamano_id, masa_t_id, borde_t_id, nombre, descripcion, img_url)
            ##DECLARANDO QUE LA PIZZA FUE CREADA POR ADMIN
            pizza_obj.de_admin = True
            pizza_obj.save()
            if not pizza_obj:
                paquete = diccionarios.diccionarioMensaje(paquete, "Error creando pizza.")
                return render(request, "Pizza/nueva_pizza_tradicional.html",paquete)

            ##CREANDO COMBINACION CON PIZZA
            Combinacion_Pizza().crear(combinacion, pizza_obj, cantidad)
            if not Combinacion_Pizza:
                paquete = diccionarios.diccionarioMensaje(paquete, "Error creando pizza.")
                return render(request, "Pizza/nueva_pizza_tradicional.html",paquete)

            ##CREANDO REGISTROS DE INGREDIENTES
            try:
                for i in range(0,len(ingredientes)):
                    ##CREANDO PIZZA_TAMANO_INGREDIENTE
                    t_ingrediente = ingredientes[i]
                    porcion = porciones[i]
                    pizza_t_ingrediente = Pizza_Tamano_Ingrediente().crear(pizza_obj, t_ingrediente, porcion)
                    if not pizza_t_ingrediente:
                        paquete = diccionarios.diccionarioMensaje(paquete, "Error creando pizza.")
                        return render(request, "Pizza/nueva_pizza_tradicional.html",paquete)
            except: 
                paquete = diccionarios.diccionarioMensaje(paquete, "Error creando pizza.")
                return render(request, "Pizza/nueva_pizza_tradicional.html",paquete)

            ##CREANDO PIZZA FAVORITA
            pizza_tradicional = Pizza_Tradicional().crear(pizza_obj, costo)
            if not pizza_tradicional:
                paquete = diccionarios.diccionarioMensaje(paquete, "Error creando pizza tradicional.")
                return render(request, "Pizza/nueva_pizza_tradicional.html",paquete)

            paquete = diccionarios.diccionarioMensaje(paquete, "Pizza tradicional creada con exito.")
            
        return render(request, "Pizza/nueva_pizza_tradicional.html",paquete)
    return redirect("login")

def editar_pizza_tradicional(request, pizza_t_id):
    if verificarSesion(request):
        ##DETALLES PARA LA SUBBARRA DE NAVEGACION
        paquete = diccionarios.diccionarioBarraNav(request,{})
        paquete = diccionarios.diccionarioDatosSubBarraPizza_T(paquete)

        ##RECOLECTANDO TIPOS DE MASAS Y BORDES 
        paquete = diccionarios.diccionarioMasasBordesIngredientes(paquete)

        if request.method == "POST":
            nombre = request.POST.get("NOMBRE",None)
            descripcion = request.POST.get("DESCRIPCION",None)
            costo = request.POST.get("COSTO",None)
            img_url = request.FILES.get("IMAGEN",None)
            estado = request.POST.get("ESTADO",None)
            tamano_id = request.POST.get("TAMANO",None)
            masa_t_id = request.POST.get("MASA",None)
            borde_t_id = request.POST.get("BORDE",None)
            ingredientes = request.POST.getlist("INGREDIENTES[]", None)
            porciones = request.POST.getlist("PORCIONES[]", None)
            cantidad = 1


            ##EDITANDO PIZZA
            pizza_obj = Pizza_Tradicional.objects.get(pk=pizza_t_id) ##OBTENIENDO ID DE PIZZA DESDE LA PIZZA TRADICIONAL
            pizza_obj = Pizza().editar(pizza_obj.pizza.id, tamano_id, masa_t_id, borde_t_id, nombre, descripcion, img_url, estado)

            ##VERIFICANDO SI SE CREO PIZZA
            if not pizza_obj:
                paquete = diccionarios.diccionarioMensaje(paquete, "Error actualizando pizza.")
                return render(request, "Pizza/editar_pizza_tradicional.html",paquete)   

            ##ELIMINADO TODOS LOS REGISTROS DE INGREDIENTES
            estado = utils.limpiarRegistros_Ingredientes(pizza_obj)
            if not estado:
                paquete = diccionarios.diccionarioMensaje(paquete, "Error actualizando ingredientes.")
                return render(request, "Pizza/editar_pizza_tradicional.html",paquete) 
            
            ##CREAR NUEVAMENTE LOS REGISTROS DE INGREDIENTES
            try:
                for i in range(0,len(ingredientes)):
                    ##CREANDO PIZZA_TAMANO_INGREDIENTE
                    t_ingrediente = ingredientes[i]
                    porcion = porciones[i]
                    pizza_t_ingrediente = Pizza_Tamano_Ingrediente().crear(pizza_obj, t_ingrediente, porcion)
                    if not pizza_t_ingrediente:
                        paquete = diccionarios.diccionarioMensaje(paquete, "Error actualizando ingredientes de pizza.")
                        return render(request, "Pizza/editar_pizza_tradicional.html",paquete)
            except: 
                paquete = diccionarios.diccionarioMensaje(paquete, "Error creando pizza.")
                return render(request, "Pizza/editar_pizza_tradicional.html",paquete)

            ##ACTUALIZANDO PIZZA TRADICIONAL
            pizza_tradicional = Pizza_Tradicional().editar(pizza_t_id, pizza_obj, costo, estado)
            if not pizza_tradicional:
                paquete = diccionarios.diccionarioMensaje(paquete, "Error actualizando pizza tradicional.")
                return render(request, "Pizza/editar_pizza_tradicional.html",paquete)

            paquete = diccionarios.diccionarioMensaje(paquete, "Pizza tradicional actualizada con exito.")

        ##INFORMACION DE PIZZA TRADICIONAL SELECCIONADA
        paquete = diccionarios.diccionarioDatoPizza_T(paquete, pizza_t_id)

        return render(request, "Pizza/editar_pizza_tradicional.html",paquete)
    return redirect("login")

## COMBOS PROMOCIONALES
def combos_promocionales(request):
    if verificarSesion(request):
        paquete = diccionarios.diccionarioBarraNav(request,{})
        paquete = diccionarios.diccionarioCombosPromocionales(paquete)
        return render(request, "CombosPromocionales/combos_promocionales.html",paquete)
    return redirect("login")

def nuevo_combo_promocional(request):
    if verificarSesion(request):
        ##DETALLES PARA LA SUBBARRA DE NAVEGACION
        paquete = diccionarios.diccionarioBarraNav(request,{})
        paquete = diccionarios.diccionarioOpcionesParaComboPromocional(paquete)

        return render(request, "CombosPromocionales/nuevo_combo_promocional.html",paquete)
    return redirect("login")







