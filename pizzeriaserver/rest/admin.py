from django.contrib import admin
from  .models import Usuario, Sesion, Detalles_Personales, Componente, Masa, Borde, Pizza, Pizza_Tradicional, Tamano

# Register your models here.
admin.site.register(Detalles_Personales)
admin.site.register(Sesion)
admin.site.register(Usuario)
admin.site.register(Componente)
admin.site.register(Masa)
admin.site.register(Borde)
admin.site.register(Pizza)
admin.site.register(Pizza_Tradicional)
admin.site.register(Tamano)
