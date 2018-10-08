from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from rest.models import Detalles_Personales
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
	usuario = Detalles_Personales.objects.get(pk=usuario_id)
	paquete = {'USUARIO' : usuario, 'URL' : 'usuario', 'TITULO' : 'USUARIOS'}
	paquete["NOMBRE"] = request.session["DETALLES_PERSONALES"]['NOMBRE'] ##NOMBRE DEL USUARIO PARA LA BARRA DE NAV
	return render(request, "Usuario/ver_usuario.html", paquete)






