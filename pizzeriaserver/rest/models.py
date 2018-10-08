# -*- coding: utf-8 -*-
from django.db import models
from django.db import IntegrityError
from django.contrib.auth.models import User as UsuarioDjango

# Create your models here.
class Usuario(models.Model):
	def crear(self, correo, contrasena):
		try: 
			usuario = UsuarioDjango.objects.create_user(correo, correo, contrasena)
			usuario.save()
			return usuario
		except IntegrityError:
			return IntegrityError
		else: 
			return None

class Detalles_Personales(models.Model):
	usuario = models.ForeignKey(UsuarioDjango, on_delete=models.CASCADE)
	nombres = models.CharField(max_length=40)
	apellidos = models.CharField(max_length=40)
	correo = models.CharField(max_length=30)
	cedula = models.CharField(max_length=20)
	telefono = models.CharField(max_length=15)

	def __str__ (self):
		return self.nombres + " " + self.apellidos + " | " + self.correo
 
	def crear (self, usuario, nombres, apellidos, correo, cedula, telefono):
		try:
			p = Detalles_Personales()
			p.usuario = usuario
			p.nombres = nombres
			p.apellidos = apellidos
			p.correo = correo
			p.cedula = cedula
			p.telefono = telefono
			p.save()
			return p
		except:
			return None