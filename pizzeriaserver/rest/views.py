from django.contrib.auth import authenticate, logout
from django.shortcuts import render
from django.http import JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

from .models import Usuario, Detalles_Personales, Pizza_Tradicional, Sesion
import json

IP = "http://navi.pythonanywhere.com"

@csrf_exempt
def login(request):
	if request.method == "POST":
		body = json.loads(request.body.decode('utf-8'))
		correo = body.get('CORREO', None)
		contrasena = body.get('CONTRASENA', None)
		# correo = request.POST.get('CORREO', None)
		# contrasena = request.POST.get('CONTRASENA', None)
		if correo and contrasena:
			usuario = authenticate(username=correo, password=contrasena)
			if usuario is not None:
				sesion = Sesion().crear(usuario)
				return JsonResponse({
					'STATUS' : 'OK',
					'CODIGO' : 1,
					'TOKEN' : sesion.token,
					'DETALLE' : 'ver lista'
					})
			else:
				return JsonResponse({
					'STATUS' : 'ERROR',
					'CODIGO' : 2,
					'DETALLE' : 'VER LISTA'
					})
	return JsonResponse({
		'STATUS' : 'ERROR',
		'CODIGO' : 15,
		'DETALLE' : 'VER LISTA'
		})

@csrf_exempt
def login_RS(request):
	body = json.loads(request.body.decode('utf-8'))
	correo = body.get('CORREO', None)
	# correo = request.POST.get('CORREO', None)
	if correo:
		try:
			usuario = Usuario.objects.get(email=correo)
			sesion = Sesion().crear(usuario)
			return JsonResponse({
				'STATUS' : 'OK',
				'CODIGO' : 1,
				'TOKEN' : sesion.token,
				'DETALLE' : 'ver lista'
				})
		except:
			return JsonResponse({
				'STATUS' : 'ERROR',
				'CODIGO' : 2,
				'DETALLE' : 'VER LISTA'
				})
	return JsonResponse({
		'STATUS' : 'ERROR',
		'CODIGO' : 15,
		'DETALLE' : 'VER LISTA'
		})

@csrf_exempt
def logout(request):
	body = json.loads(request.body.decode('utf-8'))
	token = body.get('TOKEN', None)
	#token = request.POST.get('TOKEN', None)
	if token:
		try:
			if Sesion().logout(token):
				return JsonResponse({
					'STATUS' : 'OK',
					'CODIGO' : 0,
					'DETALLE' : 'VER LISTA'
					})
		except:
			return JsonResponse({
				'STATUS' : 'ERROR',
				'CODIGO' : 11,
				'DETALLE' : 'VER LISTA'
				})
	return JsonResponse({
		'STATUS' : 'ERROR',
		'CODIGO' : 4,
		'DETALLE' : 'VER LISTA'
		})

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

		try:
			usuario = Usuario(email=correo, username=correo).save()
			if usuario and correo and contrasena and nombres and apellidos and cedula and telefono:  # EXITO
				detalles_personales = Detalles_Personales().crear(usuario, nombres, apellidos, correo, cedula, telefono)
				if detalles_personales:
					sesion = Sesion().crear(usuario)
					return JsonResponse({
						'STATUS' : 'OK',
						'CODIGO' : 10,
						'TOKEN' : sesion.token,
						'DETALLE' : 'ver lista'
						})
			else:
				return JsonResponse({
						'STATUS' : 'ERROR',
						'CODIGO' : 15,
						'DETALLE' : 'ver lista'
						})
		except(IntegrityError):
			return JsonResponse({
				'STATUS' : 'ERROR',
				'CODIGO' : 5,
				'DETALLE' : 'ver lista'
				})
	return JsonResponse({
			'STATUS' : 'ERROR',
			'CODIGO' : 15,
			'DETALLE' : 'ver lista'
			})

## USUARIOS ##
def ver_usuario(request, usuario_id):
	if request.method == "GET":
		user = Usuario.objects.get(pk=usuario_id)
		usuario = Detalles_Personales.objects.get(usuario=user)
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
		user = Usuario.objects.get(pk=usuario_id)
		usuario = Detalles_Personales.objects.get(usuario=user)

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

## PIZZAS TRADICIONALES ##
def ver_pizzas_tradicionales(request):
	if request.method == "GET":
		pizzas = Pizza_Tradicional.objects.all()
		paquete = {}
		for pizza in pizzas:
			pizza_tradicional = {
				"NOMBRE" : pizza.pizza.nombre,
				"IMAGEN_URL" : IP + pizza.pizza.img_url.url,
				"DESCRIPCION" : pizza.pizza.descripcion,
				"COSTO" : "%.2f" % float(pizza.costo)
			}
			paquete[pizza.id] = pizza_tradicional

		return JsonResponse(paquete)








