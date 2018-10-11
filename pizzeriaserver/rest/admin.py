from django.contrib import admin
from rest.models import Detalles_Personales, Componente, Masa, Borde, Pizza, Pizza_Tradicional

# Register your models here.
admin.site.register(Detalles_Personales)
admin.site.register(Componente)
admin.site.register(Masa)
admin.site.register(Borde)
admin.site.register(Pizza)
admin.site.register(Pizza_Tradicional)
