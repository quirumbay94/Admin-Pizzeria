from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from rest.models import Usuario, Detalles_Personales
import json


#TRES TIPOS DE RESPUESTA EN EL LOGIN
#	EXITO = EXITO DE LOGIN
#	ERROR_CREDENCIALES = EMAIL O CONTRASENA INCORRECTOS
# 	ERROR_SOLICITUD = SOLICITUD INCORRECTA
@csrf_exempt
def login(request):
	if request.method == "POST":
		body = json.loads(request.body.decode('utf-8'))
		correo = body['CORREO']
		contrasena = body['CONTRASENA']
		if correo and contrasena:
			usuario = authenticate(username=correo, password=contrasena)
			if usuario is not None:
				return JsonResponse({'RESPUESTA': 'EXITO'})
			else: 
				return JsonResponse({'RESPUESTA': 'ERROR_CREDENCIALES'})

	return JsonResponse({'RESPUESTA': 'ERROR_SOLICITUD'})

#TRES TIPOS DE RESPUESTA EN EL REGISTRO
#	EXITO = EXITO DE REGISTRO
#	CREDENCIALES_REPETIDAS = EMAIL YA OCUPADO
# 	SOLICITUD_INCOMPLETA = FALTAN CAMPOS PARA EL REGISTRO
# 	ERROR_SOLICITUD = SOLICITUD INCORRECTA
@csrf_exempt
def registrar(request):
	if request.method == "POST":
		body = json.loads(request.body.decode('utf-8'))
		correo = body['CORREO']
		contrasena = body['CONTRASENA']
		nombres = body['NOMBRES']
		apellidos = body['APELLIDOS']
		cedula = body['CEDULA']
		telefono = body['TELEFONO']

		usuario = Usuario().crear(correo, contrasena)
		if usuario == IntegrityError: #VERIFICACION SI ESTA REPETIDO
			return JsonResponse({'RESPUESTA': 'CREDENCIALES_REPETIDAS'})
		elif usuario and correo and contrasena and nombres and apellidos and cedula and telefono: #EXITO
			detalles_personales = Detalles_Personales().crear(usuario, nombres, apellidos, correo, cedula, telefono)
			if detalles_personales:
				return JsonResponse({'RESPUESTA': 'EXITO'})
		else:
			return JsonResponse({'RESPUESTA': 'SOLICITUD_INCOMPLETA'})
	return JsonResponse({'RESPUESTA': 'ERROR_SOLICITUD'})

def ver_usuario(request, usuario_id):
	if request.method == "GET":
		usuario = Detalles_Personales.objects.get(pk=usuario_id)
		paquete = {
			'NOMBRES' : usuario.nombres,
			'APELLIDOS' : usuario.apellidos,
			'CORREO' : usuario.correo,
			'TELEFONO' : usuario.telefono,
			'CEDULA' : usuario.cedula
		}
		return JsonResponse({'RESPUESTA': paquete})
	return JsonResponse({'RESPUESTA': 'ERROR'})

@csrf_exempt
def editar_usuario(request, usuario_id):
	if request.method == "POST":
		usuario = Detalles_Personales.objects.get(pk=usuario_id)

		## RECUPERANDO DATOS DEL REQUEST
		nombres = request.POST.get("NOMBRES",None)
		apellidos = request.POST.get("APELLIDOS",None)
		correo = request.POST.get("CORREO",None)
		telefono = request.POST.get("TELEFONO",None)
		cedula = request.POST.get("CEDULA",None)

		if nombres and apellidos and correo and telefono and cedula:
			usuario.nombres = nombres
			usuario.apellidos = apellidos
			usuario.correo = correo
			usuario.telefono = telefono
			usuario.cedula = cedula
			usuario.save()
			return JsonResponse({'RESPUESTA': 'EXITO'})
	return JsonResponse({'RESPUESTA': 'ERROR'})









