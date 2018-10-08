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
		## ANTES =>  correo = body['CORREO']      SI NO SIRVE RESTAURAR A ESTE ESTADO
		correo = body.get('CORREO',None)
		contrasena = body.get('CONTRASENA',None)
		nombres = body.get('NOMBRES',None)
		apellidos = body.get('APELLIDOS',None)
		cedula = body.get('CEDULA',None)
		telefono = body.get('TELEFONO',None)

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


## USUARIOS

## FUNCION PARA OBTENER LOS DETALLES PERSONALES DE UN USUARIO ESPECIFICO
def ver_usuario(request, usuario_id): 
	if request.method == "GET":
		try: 
			##  body = json.loads(request.body.decode('utf-8'))
			usuario = Detalles_Personales.objects.get(pk=int(usuario_id))
			paquete = {
				'NOMBRES' : usuario.nombres,
				'APELLIDOS' : usuario.apellidos,
				'CORREO' : usuario.correo,
				'CEDULA' : usuario.cedula,
				'TELEFONO' : usuario.telefono
			}
			return JsonResponse({'RESPUESTA' : paquete})
		except: 
			return JsonResponse({'RESPUESTA' : 'ERROR'})
	return JsonResponse({'RESPUESTA' : 'ERROR'})

## FUNCION PARA EDITAR LOS DATOS PERSONALES DE UN USUARIO EN ESPECIFICO
@csrf_exempt
def editar_usuario(request, usuario_id):
	if request.method == "POST":
		## body = json.loads(request.body.decode('utf-8')) IVAN NO SE PORQUE ESO A MI NO ME SIRVE PERO ESPERO QUE PUEDAS DARLE SOLUCION :(
		correo = request.POST.get('CORREO',None)
		nombres = request.POST.get('NOMBRES',None)
		apellidos = request.POST.get('APELLIDOS',None)
		cedula = request.POST.get('CEDULA',None)
		telefono = request.POST.get('TELEFONO',None)

		if correo and nombres and apellidos and cedula and telefono:
			usuario = Detalles_Personales.objects.get(pk=usuario_id)
			usuario.nombres = nombres
			usuario.apellidos = apellidos
			usuario.correo = correo
			usuario.telefono = telefono
			usuario.cedula = cedula
			usuario.save()
			return JsonResponse({'RESPUESTA' : 'EXITO'})
	return JsonResponse({'RESPUESTA' : 'ERROR'})







