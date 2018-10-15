import unicodedata
import secrets
from django.contrib.auth.hashers import make_password, check_password, is_password_usable

# Create your models here.
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import BaseUserManager, PermissionsMixin
from django.utils.crypto import salted_hmac
from django.utils.translation import gettext_lazy as _



class AbstractBaseUser(models.Model):
    password = models.CharField(_('password'), max_length=128, blank = True)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )


    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None

    class Meta:
        abstract = True

    def get_username(self):
        "Return the identifying username for this User"
        return getattr(self, self.USERNAME_FIELD)

    def __str__(self):
        return self.get_username()

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
     #  if self._password is not None:
     #      password_validation.password_changed(self._password, self)
     #      self._password = None

    def natural_key(self):
        return (self.get_username(),)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return 'email'

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username



class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        if password != None :
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)



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
    token =  models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    def crear(self, usuario):
        s = Sesion()
        s.usuario = usuario
        s.token = secrets.token_hex(16)
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

	def crear(self, masa, borde, nombre, descripcion, img_url):
		try: 
			p = Pizza()
			p.masa = Masa.objects.get(pk=masa)
			p.borde = Borde.objects.get(pk=borde)
			p.nombre = nombre
			p.descripcion = descripcion
			p.img_url = img_url
			p.estado = True
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


