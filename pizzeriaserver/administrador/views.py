from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from rest.models import Detalles_Personales, Componente
from django.contrib.auth.models import User

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
				paquete["MENSAJE"] = "Correo o contraseña invalida"
		else:
			paquete["MENSAJE"] = "Correo o contraseña imcompleta"
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
		paquete = {}
		paquete["NOMBRE"] = request.session["DETALLES_PERSONALES"]['NOMBRE'] ##NOMBRE DEL USUARIO PARA LA BARRA DE NAV
		return render(request,"Menu/menu.html", paquete)
	return redirect("login")

## USUARIOS ##
def usuario(request):
	if verificarSesion(request):
		if request.method == "POST": ##MANEJAR LA ACCION DE HABILITAR O DESABILITAR EL USUARIO
			usuario_id = request.POST.get("USUARIO",None)
			accion = request.POST.get("ACCION",None)
			if usuario_id and accion:
				usuario = User.objects.get(pk=usuario_id) ##BUSCANDO EL USUARIO
				if accion in ["true","True"]:
					usuario.is_active = True
				else: 
					usuario.is_active = False
				usuario.save()

		usuarios = Detalles_Personales.objects.all()
		paquete = {'USUARIOS' : usuarios}
		paquete["NOMBRE"] = request.session["DETALLES_PERSONALES"]['NOMBRE'] ##NOMBRE DEL USUARIO PARA LA BARRA DE NAV

		return render(request,"Usuario/usuario.html", paquete)
	return redirect("login")

def ver_usuario(request, usuario_id):
	if verificarSesion(request):
		##DETALLES PARA LA SUBBARRA DE NAVEGACION
		usuario = Detalles_Personales.objects.get(pk=usuario_id)
		paquete = {'USUARIO' : usuario, 'URL' : 'usuario', 'TITULO' : 'USUARIOS'}
		paquete["NOMBRE"] = request.session["DETALLES_PERSONALES"]['NOMBRE'] ##NOMBRE DEL USUARIO PARA LA BARRA DE NAV
		return render(request, "Usuario/ver_usuario.html", paquete)
	return redirect("login")

## COMPONENTES ##
def componentes(request, tipo):
	if verificarSesion(request):
		paquete = {"NOMBRE" : request.session["DETALLES_PERSONALES"]['NOMBRE']} ##NOMBRE DEL USUARIO PARA LA BARRA DE NAV
		
		##RECOLECTAR TODOS LOS COMPONENTES ACTIVOS
		if tipo == "INGREDIENTES":
			ingredientes = Componente.objects.filter(tipo="INGREDIENTE", estado=True).order_by('nombre')
			paquete["INGREDIENTES"] = ingredientes
		elif tipo == "ADICIONALES":
			adicionales = Componente.objects.filter(tipo="ADICIONAL", estado=True).order_by('nombre')
			paquete["ADICIONALES"] = adicionales
		paquete["TIPO"] = tipo.capitalize()
		return render(request,"Componente/componentes.html", paquete)
	return redirect("login")

def nuevo_componente(request, tipo):
	if verificarSesion(request):
		##DETALLES PARA LA SUBBARRA DE NAVEGACION
		paquete = {'USUARIO' : usuario, 'URL' : 'componentes/' + tipo.upper(), 'TITULO' : tipo.upper()}
		paquete["NOMBRE"] = request.session["DETALLES_PERSONALES"]['NOMBRE'] ##NOMBRE DEL USUARIO PARA LA BARRA DE NAV
		paquete["TIPO"] = tipo.upper()

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
				paquete["MENSAJE"] = "Componente creado con exito."
			else: 
				paquete["MENSAJE"] = "Error creando componente."
		
		return render(request, "Componente/nuevo_componente.html", paquete)
	return redirect("login")

def ver_componente(request, tipo, componente_id):
	if verificarSesion(request):
		##DETALLES PARA LA SUBBARRA DE NAVEGACION
		paquete = {'USUARIO' : usuario, 'URL' : 'componentes/'  + tipo.upper(), 'TITULO' : tipo.upper()}
		paquete["NOMBRE"] = request.session["DETALLES_PERSONALES"]['NOMBRE'] ##NOMBRE DEL USUARIO PARA LA BARRA DE NAV

		##BUSCANDO COMPONENTE
		componente = Componente.objects.get(pk=componente_id)
		paquete["COMPONENTE"] = componente

		return render(request, "Componente/ver_componente.html", paquete)
	return redirect("login")






