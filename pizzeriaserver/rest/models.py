import secrets

from django.db import models
from rest import user_model
from rest.user_model import AbstractBaseUser, PermissionsMixin, UsuarioManager
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractBaseUser , PermissionsMixin):

    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __unicode__(self):
        return self.email

    def crearSinContrasena(self, correo):
        usuario = Usuario()
        usuario.email = correo
        usuario.username = correo
        usuario.save()
        return usuario

class Sesion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    token =  models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)

    def crear(self, usuario):
        s = Sesion()
        s.usuario = usuario
        s.token = secrets.token_hex(32)
        s.save()
        return s
    def logout(self, token):
        try:
            s = Sesion.objects.get(token=token)
            s.delete()
            return  True
        except:
            return False
    def get(self, usuario):
        try:
            s = Sesion.objects.get(usuario=usuario)
            return s
        except:
            return None


##DATOS PERSONALES DE CADA USUARIO
class Detalles_Personales(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)
    correo = models.CharField(max_length=30)
    cedula = models.CharField(max_length=20, blank=True)
    telefono = models.CharField(max_length=15, blank=True)

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
        except Exception as e:
            print("")
            print("ERROR")
            print(e)
            print("")
            return None

    def crear_simple(self, usuario, nombres, apellidos, correo):
        try:
            detalles = Detalles_Personales()
            detalles.usuario = usuario
            detalles.nombres = nombres
            detalles.apellidos = apellidos
            detalles.correo = correo
            detalles.save()    
            return detalles
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

    def editar(self, componente_id, nombre, descripcion, tipo, costo, img_url, estado):
        try:
            c = Componente.objects.get(pk=componente_id)
            c.nombre = nombre
            c.descripcion = descripcion
            c.tipo = tipo
            c.costo = costo
            c.estado = estado
            if img_url:
                c.img_url = img_url
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
    tamano =  models.CharField(max_length=30)
    masa = models.ForeignKey("Tamano_Masa", on_delete=models.CASCADE)
    borde = models.ForeignKey("Tamano_Borde", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, blank=True)
    img_url = models.ImageField(blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        estadoStr = "Activo"
        if not self.estado:
            estadoStr = "Inactivo"
        return self.nombre + " | " + estadoStr

    def crear(self, tamano, masa, borde, nombre, descripcion, img_url):
        try: 
            p = Pizza()
            p.tamano = tamano
            p.masa = Tamano_Masa.objects.get(pk=masa)
            p.borde = Tamano_Borde.objects.get(pk=borde)
            p.nombre = nombre
            p.descripcion = descripcion
            p.img_url = img_url
            p.estado = True
            p.save()
            return p
        except:
            return None
    def editar(self, pizza_id, masa, borde, nombre, descripcion, img_url, estado):
        try: 
            p = Pizza.objects.get(pk=pizza_id)
            p.masa = Masa.objects.get(pk=masa)
            p.borde = Borde.objects.get(pk=borde)
            p.nombre = nombre
            p.descripcion = descripcion
            p.estado = estado
            if img_url:
                p.img_url = img_url
            p.save()
            return p
        except:
            return None

class Pizza_Tamano_Ingrediente(models.Model):
    pizza = models.ForeignKey("Pizza", on_delete=models.CASCADE)
    tamano_ingrediente = models.ForeignKey("Tamano_Ingrediente", on_delete=models.CASCADE)

    def __str__(self):
        return self.pizza.nombre + " | " + self.tamano_ingrediente.ingrediente.nombre

    def crear(self, pizza, tamano_ingrediente):
        pizza_t_ingrediente = Pizza_Tamano_Ingrediente()
        pizza_t_ingrediente.pizza = pizza
        pizza_t_ingrediente.tamano_ingrediente = tamano_ingrediente
        pizza_t_ingrediente.save()
        return pizza_t_ingrediente

##SELECCION DE PIZZAS TRADICIONALES
class Pizza_Tradicional(models.Model):
    pizza = models.ForeignKey("Pizza", on_delete=models.CASCADE)
    costo = models.FloatField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.pizza.nombre + " | $" + str(self.costo)

    def crear(self, pizza, costo):
        try:
            pt = Pizza_Tradicional()
            pt.pizza = pizza
            pt.costo = costo
            pt.estado = True
            pt.save()
            return pt
        except:
            return None

    def editar(self, pizza_t_id, pizza, costo, estado):
        try:
            pt = Pizza_Tradicional.objects.get(pk=pizza_t_id)
            pt.pizza = pizza
            pt.costo = costo
            pt.estado = estado
            pt.save()
            return pt
        except:
            return None

##TAMAÑOS PARA MASAS Y BORDES
class Tamano(models.Model):
    nombre = models.CharField(_("Tamaño"),max_length=15)

    def __str__(self):
        return self.nombre

class Tamano_Masa(models.Model):
    tamano =  models.ForeignKey("Tamano", on_delete=models.CASCADE)   
    masa = models.ForeignKey("Masa", on_delete=models.CASCADE)
    costo = models.FloatField()

    def __str__(self):
        return self.masa.nombre + " | " + self.tamano.nombre + ": $" + str(self.costo)

class Tamano_Borde(models.Model):
    tamano =  models.ForeignKey("Tamano", on_delete=models.CASCADE)   
    borde = models.ForeignKey("Borde", on_delete=models.CASCADE)
    costo = models.FloatField()

    def __str__(self):
        return self.borde.nombre + " | " + self.tamano.nombre + ": $" + str(self.costo)

class Tamano_Ingrediente(models.Model):
    tamano =  models.ForeignKey("Tamano", on_delete=models.CASCADE)   
    ingrediente = models.ForeignKey("Componente", on_delete=models.CASCADE)
    costo = models.FloatField()

    def __str__(self):
        return self.ingrediente.nombre + " | " + self.tamano.nombre + ": $" + str(self.costo)

## COMBINACIONES
class Combinacion(models.Model):
    nombre = models.CharField(max_length=50, blank=True)
    usuario = models.ForeignKey("Usuario", on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        nombre_ = "Combinacion"
        if self.nombre:
            nombre_ = self.nombre
        return nombre_ + " | CREADO POR: " + self.usuario.username

    def crear(self, nombre, usuario):
        nombre_ = "Combinacion"
        if nombre:
            nombre_ = nombre

        combinacion = Combinacion()
        combinacion.nombre = nombre_
        combinacion.usuario = usuario
        combinacion.save()
        return combinacion

class Combos_Promocionales(models.Model):
    combinacion = models.ForeignKey("Combinacion", on_delete=models.CASCADE, default=None)
    nombre = models.CharField(max_length=30)
    costo = models.FloatField()
    img_url = models.ImageField()
    descripcion = models.TextField(max_length=255, blank=True)
    fecha_inicio = models.DateField(blank=True)
    fecha_fin = models.DateField(blank=True)

    def __str__(self):
        return self.nombre + " $" + str(self.costo)

class Combinacion_Pizza(models.Model):
    combinacion = models.ForeignKey("Combinacion", on_delete=models.CASCADE, default=None)
    pizza = models.ForeignKey("Pizza", on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.pizza.nombre + " | COMBINACION: " + self.combinacion.nombre + " | CANT: " + str(self.cantidad)

class Combinacion_Adicional(models.Model):
    combinacion = models.ForeignKey("Combinacion", on_delete=models.CASCADE, default=None)
    adicional =  models.ForeignKey("Componente", on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return self.adicional.nombre + " | COMBINACION: " + self.combinacion.nombre + " | CANT: " + str(self.cantidad)


##PROMOCION
class Promocion(models.Model):
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=255)
    costo = models.FloatField(default=0.00, blank=True)
    img_url = models.ImageField()
    fecha_inicio = models.DateField(blank=True)
    fecha_fin = models.DateField(blank=True)

    def __str__(self):
        return self.nombre + " | INICIO: " + str(self.fecha_inicio) + " | FIN: " + str(self.fecha_fin)



