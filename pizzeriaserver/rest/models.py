import secrets
import random
import datetime
from datetime import timedelta, timezone 
from django.db import models
from rest import user_model
from rest.user_model import AbstractBaseUser, PermissionsMixin, UsuarioManager
from pizzeriaserver.settings import DEFASE_ZONA_HORARIA
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractBaseUser , PermissionsMixin):

    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    local = models.ForeignKey("Local", on_delete=models.CASCADE, null=True)

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
            s.save()
            return  True
        except:
            return False
    def get(self, usuario):
        try:
            s = Sesion.objects.get(usuario=usuario)
            return s
        except:
            return None
    def __str__ (self):
        return self.usuario.username


##DATOS PERSONALES DE CADA USUARIO
class Detalles_Personales(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombres = models.CharField(max_length=40)
    apellidos = models.CharField(max_length=40)
    correo = models.CharField(max_length=30)
    cedula = models.CharField(max_length=20, blank=True)
    telefono = models.CharField(max_length=15, blank=True)
    imagen = models.ImageField(blank=True)

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
    img_url = models.ImageField(blank=True)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + " | " + self.tipo

    def crear(self, nombre, descripcion, tipo, img_url, estado):
        try: 
            c = Componente()
            c.nombre = nombre
            c.descripcion = descripcion
            c.tipo = tipo
            c.img_url = img_url
            c.estado = estado
            c.save()
            return c
        except:
            return None

    def editar(self, componente_id, nombre, descripcion, tipo, img_url, estado):
        try:
            c = Componente.objects.get(pk=componente_id)
            c.nombre = nombre
            c.descripcion = descripcion
            c.tipo = tipo
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

## PORCION
class Porcion(models.Model):
    nombre = models.CharField(max_length=30)
    valor = models.IntegerField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre + " | VALOR: " + str(self.valor)

##PIZZA
class Pizza(models.Model):
    tamano =  models.ForeignKey("Tamano", on_delete=models.CASCADE, default=None) 
    masa = models.ForeignKey("Tamano_Masa", on_delete=models.CASCADE)
    borde = models.ForeignKey("Tamano_Borde", on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, blank=True)
    img_url = models.ImageField(blank=True)
    estado = models.BooleanField(default=True)
    de_admin = models.BooleanField(default=False)

    def __str__(self):
        estadoStr = "Activo"
        if not self.estado:
            estadoStr = "Inactivo"
        return self.nombre + " | " + estadoStr

    def crear(self, tamano_id, masa_t_id, borde_t_id, nombre, descripcion, img_url):
        try: 
            p = Pizza()
            p.tamano = Tamano.objects.get(pk=tamano_id)
            p.masa = Tamano_Masa.objects.get(pk=masa_t_id)
            p.borde = Tamano_Borde.objects.get(pk=borde_t_id)
            p.nombre = nombre
            p.descripcion = descripcion
            p.img_url = img_url
            p.estado = True
            p.save()
            return p
        except:
            return None

    def crear_simple(self, tamano_id, masa_t_id, borde_t_id, nombre):
        try: 
            p = Pizza()
            p.tamano = Tamano.objects.get(pk=tamano_id)
            p.masa = Tamano_Masa.objects.get(pk=masa_t_id)
            p.borde = Tamano_Borde.objects.get(pk=borde_t_id)
            p.nombre = nombre
            p.estado = True
            p.save()
            return p
        except:
            return None
            
    def editar(self, pizza_id, tamano_id, masa_t_id, borde_t_id, nombre, descripcion, img_url, estado):
        try: 
            p = Pizza.objects.get(pk=pizza_id)
            p.tamano = Tamano.objects.get(pk=tamano_id)
            p.masa = Tamano_Masa.objects.get(pk=masa_t_id)
            p.borde = Tamano_Borde.objects.get(pk=borde_t_id)
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
    porcion = models.ForeignKey("Porcion", on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.pizza.nombre + " | " + self.tamano_ingrediente.ingrediente.nombre

    def crear(self, pizza, tamano_ingrediente_id, porcion_id):
        pizza_t_ingrediente = Pizza_Tamano_Ingrediente()
        pizza_t_ingrediente.pizza = pizza
        pizza_t_ingrediente.tamano_ingrediente = Tamano_Ingrediente.objects.get(pk=tamano_ingrediente_id)
        pizza_t_ingrediente.porcion = Porcion.objects.get(pk=porcion_id)
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

class Pizza_Favorita(models.Model):
    pizza = models.ForeignKey("Pizza", on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.pizza.nombre

    def crear(self, pizza, usuario):
        try:
            pizza_fav = Pizza_Favorita()
            pizza_fav.pizza = pizza
            pizza_fav.usuario = usuario
            pizza_fav.save()
            return pizza_fav
        except:
            return None

    def crear_con_id(self, pizza_id, usuario):
        try:
            pizza_fav = Pizza_Favorita()
            pizza_fav.pizza = Pizza.objects.get(pk=pizza_id)
            pizza_fav.usuario = usuario
            pizza_fav.save()
            return pizza_fav
        except Exception as e:
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

    def crear(self, tamano_id, ingrediente, costo):
        try:
            t_i = Tamano_Ingrediente()
            t_i.tamano = Tamano.objects.get(pk=tamano_id)
            t_i.ingrediente = ingrediente
            t_i.costo = costo
            t_i.save()
            return t_i
        except:
            return None
    def crear_default(self, ingrediente, costo):
        try:
            tamano_mediano = Tamano.objects.filter(nombre="MEDIANO")[0]
            t_i = Tamano_Ingrediente()
            t_i.tamano = tamano_mediano
            t_i.ingrediente = ingrediente
            t_i.costo = costo
            t_i.save()
            return t_i
        except:
            return None

    def borrar_masivo(self, ingrediente_id):
        try:
            ingrediente = Componente.objects.get(pk=ingrediente_id)
            Tamano_Ingrediente.objects.filter(ingrediente=ingrediente).delete()
            return True
        except:
            return False

## COMBINACIONES
class Combinacion(models.Model):
    nombre = models.CharField(max_length=50, blank=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        nombre_ = "Combinacion"
        if self.nombre:
            nombre_ = self.nombre
        return nombre_ + " | CREADO POR: " + self.usuario.username

    def crear(self, nombre, usuario):
        try:
            nombre_ = "Combinacion"
            if nombre:
                nombre_ = nombre

            combinacion = Combinacion()
            combinacion.nombre = nombre_
            combinacion.usuario = usuario
            combinacion.save()
            return combinacion
        except:
            return None

    def editar(self, combinacion_id, nombre, usuario):
        nombre_ = "Combinacion"
        if nombre:
            nombre_ = nombre
        try:
            combinacion = Combinacion.objects.get(pk=combinacion_id)
            combinacion.nombre = nombre_
            combinacion.usuario = usuario
            combinacion.save()
            return combinacion
        except:
            return None

class Combos_Promocionales(models.Model):
    combinacion = models.ForeignKey("Combinacion", on_delete=models.CASCADE, default=None)
    nombre = models.CharField(max_length=30)
    costo = models.FloatField()
    img_url = models.ImageField()
    descripcion = models.TextField(max_length=255, blank=True)
    fecha_inicio = models.DateField(auto_now_add=True)
    fecha_fin = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre + " $" + str(self.costo)

    def crear(self, combinacion, nombre, costo, img_url, descripcion):
        try:
            c = Combos_Promocionales()
            c.combinacion = combinacion
            c.nombre = nombre
            c.costo = costo
            c.img_url = img_url
            c.descripcion = descripcion
            c.save()
            return c
        except:
            return None

class Combinacion_Combo(models.Model):
    combinacion = models.ForeignKey("Combinacion", on_delete=models.CASCADE, default=None)
    combo = models.ForeignKey("Combos_Promocionales", on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return "ID: " + str(self.id) + " NOMBRE: " + self.combo.nombre
    def crear(self, combinacion, combo, cantidad):
        try:
            c = Combinacion_Combo()
            c.combinacion = combinacion
            c.combo = combo
            c.cantidad = cantidad
            c.save()
            return c
        except:
            return None
    def editar(self, combinacion_id, cantidad):
        try:
            c = Combinacion_Combo.objects.get(pk=combinacion_id)
            c.cantidad = cantidad
            c.save()
            return c
        except:
            return None

class Combinacion_Pizza(models.Model):
    combinacion = models.ForeignKey("Combinacion", on_delete=models.CASCADE, default=None)
    pizza = models.ForeignKey("Pizza", on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return "ID: " + str(self.id) + "  NOMBRE: " + self.pizza.nombre + " | COMBINACION: " + self.combinacion.nombre + " | CANT: " + str(self.cantidad)

    def crear(self, combinacion, pizza, cantidad):
        try:
            c = Combinacion_Pizza()
            c.combinacion = combinacion
            c.pizza = pizza
            c.cantidad = cantidad
            c.save()
            return c
        except:
            return None
    def editar(self, combinacion_id, cantidad):
        try:
            c = Combinacion_Pizza.objects.get(pk=combinacion_id)
            c.cantidad = cantidad
            c.save()
            return c
        except:
            return None

class Combinacion_Adicional(models.Model):
    combinacion = models.ForeignKey("Combinacion", on_delete=models.CASCADE, default=None)
    adicional =  models.ForeignKey("Componente", on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return "ID: " + str(self.id) + "  NOMBRE: " + self.adicional.nombre + " | COMBINACION: " + self.combinacion.nombre + " | CANT: " + str(self.cantidad)

    def crear(self, combinacion, adicional, cantidad):
        try: 
            c_a = Combinacion_Adicional()
            c_a.combinacion = combinacion
            c_a.adicional = adicional
            c_a.cantidad = cantidad
            c_a.save()
            return c_a
        except:
            return None

    def editar(self, combinacion_id, cantidad):
        try:
            c = Combinacion_Adicional.objects.get(pk=combinacion_id)
            c.cantidad = cantidad
            c.save()
            return c
        except:
            return None

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

##DIRECCIONES DEL CLIENTE
class Direccion_Cliente(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50, default="Dirección")
    descripcion = models.CharField(max_length=255, blank=True)
    latitud = models.CharField(max_length=15)
    longitud = models.CharField(max_length=15)

    def __str__(self):
        return self.usuario.username + " | " + self.nombre

    def crear(self, usuario, nombre, descripcion, latitud, longitud):
        try:
            direccion = Direccion_Cliente()
            direccion.usuario = usuario
            direccion.nombre = nombre
            direccion.latitud = latitud
            direccion.longitud = longitud
            if descripcion:
                direccion.descripcion = descripcion
            direccion.save()
            return direccion
        except:
            return None
    def borrar(self,direccion_id):
        try:
            direccion = Direccion_Cliente.objects.get(pk=direccion_id)
            direccion.delete()
            return True
        except:
            return False
    def editar(self, direccion_id, usuario, nombre, descripcion, latitud, longitud):
        try:
            direccion = Direccion_Cliente.objects.get(pk=direccion_id)
            direccion.usuario = usuario
            direccion.nombre = nombre
            direccion.descripcion = descripcion
            direccion.latitud = latitud
            direccion.longitud = longitud
            direccion.save()
            return direccion
        except:
            return None

class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.BooleanField()

    def __str__(self):
        return self.usuario.username + " | " + str(self.estado)

    def crear(self, usuario_id):
        try: 
            usuario = Usuario.objects.get(pk=usuario_id)
            carrito = Carrito()
            carrito.usuario = usuario
            carrito.estado = True
            carrito.save()
            return carrito
        except:
            return None

class DetalleCarrito(models.Model):
    combinacion = models.ForeignKey("Combinacion", on_delete=models.CASCADE, default=None)
    carrito = models.ForeignKey("Carrito", on_delete=models.CASCADE, default=None)

    def __str__(self):
        return "ID: " + str(self.id) + " CARRITO DE: " + self.carrito.usuario.username

    def crear(self, combinacion, carrito):
        try:
            detalle = DetalleCarrito()
            detalle.combinacion = combinacion
            detalle.carrito = carrito
            detalle.save()
            return detalle
        except:
            return None

class Poligono(models.Model):
    local = models.OneToOneField("Local", on_delete=models.CASCADE, unique=True, default=None)
    color = models.CharField(max_length=10, default='#4286f4')

    ##CASO ESPECIFICO DONDE SE CREA O SE ACTUALIZA EN EL MISMO METODO
    def crear(self, local, coordenadas):
        poligono = Poligono.objects.filter(local=local)
        ##CREAR POLIGONO
        if len(poligono) == 0:
            try:
                p = Poligono()
                p.local = local

                ##CREANDO COLOR ALEATORIO 
                r = lambda: random.randint(0,255)
                p.color = '#%02X%02X%02X' % (r(),r(),r())

                p.save()
                ##CREANDO COORDENADAS
                for coordenada in coordenadas:
                    c = Coordenada().crear(coordenada.split("|")[0], coordenada.split("|")[1])
                    Coordenada_Poligono().crear(p, c)
                return p
            except:
                return None
        ##ACTUALIZAR POLIGONO
        else:
            try: 
                poligono = poligono[0]
                coordenadas_poligono = Coordenada_Poligono.objects.filter(poligono=poligono)
                ##BORRANDO PREVIAS INSTANCIAS
                for c in coordenadas_poligono:
                    c.coordenada.delete()
                 ##CREANDO COORDENADAS
                for coordenada in coordenadas:
                    c = Coordenada().crear(coordenada.split("|")[0], coordenada.split("|")[1])
                    Coordenada_Poligono().crear(poligono, c)
                return poligono
            except:
                return None


    def getCoordenadas(self, local_id):
        try:
            local = Local.objects.get(pk=local_id)
            poligono = Poligono.objects.get(local=local)
            coordenadas_poligono = Coordenada_Poligono.objects.filter(poligono=poligono)
            paquete = []
            for c in coordenadas_poligono:
                paquete.append(c.coordenada)
            return paquete
        except: 
            return []
    def getCoordenadasJSON(self, local_id):
        try:
            local = Local.objects.get(pk=local_id)
            poligono = Poligono.objects.get(local=local)
            coordenadas_poligono = Coordenada_Poligono.objects.filter(poligono=poligono)
            paquete = []
            for c in coordenadas_poligono:
                paquete.append({"LAT" : c.coordenada.latitud, "LNG" : c.coordenada.longitud})
            return paquete
        except: 
            return []

    def __str__(self):
        return self.local.sector + " | " + self.local.ciudad.upper()


class Coordenada_Poligono(models.Model):
    poligono = models.ForeignKey("Poligono", on_delete=models.CASCADE, default=None)
    coordenada = models.ForeignKey("Coordenada", on_delete=models.CASCADE, default=None)

    def crear(self, poligono, coordenada):
        try:
            c = Coordenada_Poligono()
            c.poligono = poligono
            c.coordenada = coordenada
            c.save()
            return c
        except: 
            return None

class Coordenada(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()

    def crear(self, latitud, longitud):
        try:
            c = Coordenada()
            c.latitud = latitud
            c.longitud = longitud
            c.save()
            return c
        except:
            return None


class Local(models.Model):
    sector = models.CharField(max_length=128)
    ciudad = models.CharField(max_length=64, default="Guayaquil")
    coordenada = models.ForeignKey("Coordenada", on_delete=models.CASCADE, default=None)
    apertura = models.TimeField(default=None)
    cierre = models.TimeField(default=None)
    img_url = models.ImageField()
    estado = models.BooleanField()

    def crear(self, sector, ciudad, coordenada, apertura, cierre, imagen):
        try:
            l = Local()
            l.sector = sector
            l.ciudad = ciudad
            l.coordenada = coordenada
            l.apertura = apertura
            l.cierre = cierre
            l.img_url = imagen
            l.estado = True
            l.save()
            return l
        except:
            return None

    def editar(self, local_id, sector, ciudad, coordenada, apertura, cierre, imagen, estado):
        try:
            l = Local.objects.get(pk=local_id)
            l.sector = sector
            l.ciudad = ciudad
            l.apertura = apertura
            l.cierre = cierre
            if coordenada:
                l.coordenada.latitud = coordenada.split("|")[0] ##LATITUD OBTENIDA DE LA COORDENADA
                l.coordenada.longitud = coordenada.split("|")[1] ##LONGITUD OBTENIDA DE LA COORDENADA
                l.coordenada.save()
            if imagen:
                l.img_url = imagen
            l.estado = estado
            l.save()
            return l
        except:
            return None

    def __str__(self):
        return self.sector + " | " + self.ciudad.upper()


class Reclamo_Sugerencia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    contenido = models.CharField(max_length=500)
    fecha = models.DateTimeField()
    estado = models.BooleanField()

    def crear(self, usuario, contenido, fecha):
        try:
            reclamo = Reclamo_Sugerencia()
            reclamo.usuario = usuario
            reclamo.contenido = contenido
            reclamo.fecha = fecha
            reclamo.estado = True
            reclamo.save()
            return reclamo
        except:
            return None

class Pedido(models.Model):
    carrito = models.ForeignKey("Carrito", on_delete=models.CASCADE) 
    local = models.ForeignKey("Local", on_delete=models.CASCADE, null=True)
    coordenada_entrega = models.ForeignKey("Coordenada", on_delete=models.CASCADE, null=True)
    total = models.FloatField()
    forma_pago = models.IntegerField()
    codigo = models.CharField(max_length=32, unique=True)
    fecha = models.DateTimeField()
    entregado = models.IntegerField(default=0)
    recibido = models.IntegerField(default=0)

    def crear(self, carrito, total, coordenada_entrega, forma_pago, codigo, poligono, local):
        try:
            pedido = Pedido()
            pedido.carrito = carrito
            pedido.total = total
            pedido.forma_pago = forma_pago
            pedido.codigo = codigo
            pedido.fecha = datetime.datetime.now(timezone.utc) - timedelta(hours=DEFASE_ZONA_HORARIA)
            pedido.entregado = 0
            pedido.recibido = 0

            #ENCONTRAR EL LOCAL SEGUN EL POLIGONO
            if poligono:
                poligono_obj = Poligono.objects.get(pk=poligono)
                pedido.local = poligono_obj.local

            if local:
                pedido.local = Local.objects.get(pk=local)

            if coordenada_entrega:
                pedido.coordenada_entrega = coordenada_entrega

            pedido.save()
            return pedido
        except:
            return None

    def __str__(self):
        return self.carrito.usuario.username + " | " + str(self.total)


class Detalle_Pedido(models.Model):
    pedido = models.ForeignKey("Pedido", on_delete=models.CASCADE) 
    combinacion = models.ForeignKey("Combinacion", on_delete=models.CASCADE) 

    def crear(self, pedido, combinacion):
        try:
            d = Detalle_Pedido()
            d.pedido = pedido
            d.combinacion = combinacion
            d.save()
            return d
        except:
            return None

    def __str__(self):
        return self.pedido.carrito.usuario.username















