from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import User
from rest.models import *
from administrador.Funciones import diccionarios

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
		'NOMBRE' : detalles.nombres
	}

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

		if tipo == "INGREDIENTES":
			ingredientes = Componente.objects.filter(tipo="INGREDIENTES").order_by('nombre')
			paquete["INGREDIENTES"] = ingredientes
		elif tipo == "ADICIONALES":
			adicionales = Componente.objects.filter(tipo="ADICIONALES").order_by('nombre')
			paquete["ADICIONALES"] = adicionales
		paquete["TIPO"] = tipo.capitalize()
		return render(request,"Componente/componentes.html", paquete)
	return redirect("login")

def nuevo_componente(request, tipo):
	if verificarSesion(request):
		##DETALLES PARA LA SUBBARRA DE NAVEGACION
		paquete = diccionarios.diccionarioBarraNav(request,{})
		paquete = diccionarios.diccionarioDatosSubBarraComponente(paquete, tipo)

		if request.method == "POST":
			tipo = request.POST.get("TIPO",None)
			nombre = request.POST.get("NOMBRE",None)
			descripcion = request.POST.get("DESCRIPCION",None)
			costo = request.POST.get("COSTO",None)
			imagen = request.FILES.get("IMAGEN",None)
			estado = True

			##CREANDO COMPONENTE
			componente = Componente().crear(nombre, descripcion, tipo, costo, imagen, estado)
			if componente:
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
			costo = request.POST.get("COSTO",None)
			imagen = request.FILES.get("IMAGEN",None)
			estado = request.POST.get("ESTADO",None)
			if estado in ["True", "true"]:
				estado = True
			else:
				estado = False

			##EDITANDO COMPONENTE
			componente = Componente().editar(componente_id, nombre, descripcion, tipo, costo, imagen, estado)
			if componente:
				paquete = diccionarios.diccionarioMensaje(paquete, "Componente editado con exito.")
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
		paquete = diccionarios.diccionarioMasasyBordes(paquete)

		if request.method == "POST":
			nombre = request.POST.get("NOMBRE",None)
			masa = request.POST.get("MASA",None)
			borde = request.POST.get("BORDE",None)
			descripcion = request.POST.get("DESCRIPCION",None)
			costo = request.POST.get("COSTO",None)
			imagen = request.FILES.get("IMAGEN",None)

			pizza = Pizza().crear(masa, borde, nombre, descripcion, imagen)
			if pizza:
				pizza_t = Pizza_Tradicional().crear(pizza,costo)
				if pizza_t:
					paquete = diccionarios.diccionarioMensaje(paquete, "Pizza tradicional creada con exito.")
				else: 
					paquete = diccionarios.diccionarioMensaje(paquete, "Error creando pizza tradicional.")
			else:
				paquete = diccionarios.diccionarioMensaje(paquete, "Error creando pizza.")

		return render(request, "Pizza/nueva_pizza_tradicional.html",paquete)
	return redirect("login")

def editar_pizza_tradicional(request, pizza_t_id):
	if verificarSesion(request):
		##DETALLES PARA LA SUBBARRA DE NAVEGACION
		paquete = diccionarios.diccionarioBarraNav(request,{})
		paquete = diccionarios.diccionarioDatosSubBarraPizza_T(paquete)

		##RECOLECTANDO TIPOS DE MASAS Y BORDES 
		paquete = diccionarios.diccionarioMasasyBordes(paquete)

		if request.method == "POST":
			pizza_id = request.POST.get("PIZZA_ID",None)
			nombre = request.POST.get("NOMBRE",None)
			masa = request.POST.get("MASA",None)
			borde = request.POST.get("BORDE",None)
			descripcion = request.POST.get("DESCRIPCION",None)
			costo = request.POST.get("COSTO",None)
			imagen = request.FILES.get("IMAGEN",None)
			estado = request.POST.get("ESTADO",None)
			if estado in ["True", "true"]:
				estado = True
			else:
				estado = False

			pizza = Pizza().editar(pizza_id, masa, borde, nombre, descripcion, imagen, estado)
			if pizza:
				pizza_t = Pizza_Tradicional().editar(pizza_t_id, pizza, costo, estado)
				if pizza_t:
					paquete = diccionarios.diccionarioMensaje(paquete, "Pizza tradicional creada con exito.")
				else: 
					paquete = diccionarios.diccionarioMensaje(paquete, "Error creando pizza tradicional.")
			else:
				paquete = diccionarios.diccionarioMensaje(paquete, "Error creando pizza.")

		##INFORMACION DE PIZZA TRADICIONAL SELECCIONADA
		paquete = diccionarios.diccionarioDatoPizza_T(paquete, pizza_t_id)

		return render(request, "Pizza/editar_pizza_tradicional.html",paquete)
	return redirect("login")










