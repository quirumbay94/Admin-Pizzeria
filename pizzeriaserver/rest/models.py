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

##DATOS PERSONALES DE CADA USUARIO
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

## INGREDIENTES DE LA PIZZA O ADICIONALES (BEBIDAS, ETC)
class Componente(models.Model):
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=255)
	tipo = models.CharField(max_length=20)
	costo = models.FloatField()
	img_url = models.ImageField(blank=True)
	estado = models.BooleanField(default=True)

	def __str__(self):
		return self.nombre + " | " + self.tipo

	def crear(self, nombre, descripcion, tipo, costo, img_url, estado):
		try: 
			c = Componente()
			c.nombre = nombre
			c.descripcion = descripcion
			c.tipo = tipo
			c.costo = costo
			c.img_url = img_url
			c.estado = estado
			c.save()
			return c
		except:
			return None

##TIPOS DE MASA DE LA PIZZA
class Masa(models.Model):
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=255)
	estado = models.BooleanField(default=True)

	def __str__(self):
		return self.nombre 

	def crear(self, nombre, descripcion, estado):
		try: 
			m = Masa()
			m.nombre = nombre
			m.descripcion = descripcion
			m.estado = estado
			m.save()
			return m
		except:
			return None

##TIPO DE BORDES DE LA PIZZA
class Borde(models.Model):
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=255)
	estado = models.BooleanField(default=True)

	def __str__(self):
		return self.nombre 

	def crear(self, nombre, descripcion, estado):
		try: 
			b = Borde()
			b.nombre = nombre
			b.descripcion = descripcion
			b.estado = estado
			b.save()
			return b
		except:
			return None

##PIZZA
class Pizza(models.Model):
	masa = models.ForeignKey("Masa", on_delete=models.CASCADE)
	borde = models.ForeignKey("Borde", on_delete=models.CASCADE)
	nombre = models.CharField(max_length=50)
	descripcion = models.CharField(max_length=255)
	img_url = models.ImageField(blank=True)
	estado = models.BooleanField(default=True)

	def __str__(self):
		estadoStr = "Activo"
		if not self.estado:
			estadoStr = "Inactivo"
		return self.nombre + " | " + estadoStr

	def crear(self, masa, borde, nombre, descripcion, img_url, estado):
		try: 
			p = Pizza()
			p.masa = masa
			p.borde = borde
			p.nombre = nombre
			p.descripcion = descripcion
			p.img_url = img_url
			p.estado = estado
			p.save()
			return p
		except:
			return None

##SELECCION DE PIZZAS TRADICIONALES
class Pizza_Tradicional(models.Model):
	pizza = models.ForeignKey("Pizza", on_delete=models.CASCADE)
	costo = models.FloatField()
	estado = models.BooleanField(default=True)

	def __str__(self):
		return self.pizza.nombre + " | $" + str(self.costo)

	def crear(self, pizza, costo, estado):
		try:
			pt = Pizza_Tradicional()
			pt.pizza = pizza
			pt.costo = costo
			pt.estado = estado
			pt.save()
			return pt
		except:
			return None


