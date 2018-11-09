from django.contrib import admin
from .models import Usuario, Sesion, Detalles_Personales, Componente, Masa, Borde, Pizza, Pizza_Tradicional, Tamano, Tamano_Masa, Tamano_Borde, Tamano_Ingrediente
from .models import Combinacion, Combos_Promocionales, Combinacion_Pizza, Combinacion_Adicional, Promocion, Porcion
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
admin.site.register(Tamano_Masa)
admin.site.register(Tamano_Borde)
admin.site.register(Tamano_Ingrediente)
admin.site.register(Combinacion)
admin.site.register(Combos_Promocionales)
admin.site.register(Combinacion_Pizza)
admin.site.register(Combinacion_Adicional)
admin.site.register(Promocion)
admin.site.register(Porcion)
