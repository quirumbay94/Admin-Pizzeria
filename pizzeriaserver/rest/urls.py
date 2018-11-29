from django.conf.urls import url, include
from rest import views

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^login_RS$', views.login_RS, name='login_RS'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^registrar$', views.registrar, name='registrar'),

    ## USUARIOS ##
    url(r'^usuario/ver$', views.ver_usuario, name='ver_usuario'),
    url(r'^usuario/editar$', views.editar_usuario, name='editar_usuario'),

    ## PIZZAS ##
    url(r'^pizzas_tradicionales$', views.ver_pizzas_tradicionales, name='ver_pizzas_tradicionales'),
    url(r'^pizzas_favoritas$', views.pizzas_favoritas, name='pizzas_favoritas'),
    url(r'^crear_pizza_favorita$', views.crear_pizza_favorita, name='crear_pizza_favorita'),

    ##TAMANOS
    url(r'^tamanos/$', views.tamanos, name='tamanos'),
    url(r'^tamano_masa/$', views.tamano_masa, name='tamano_masa'),
    url(r'^tamano_borde/$', views.tamano_borde, name='tamano_borde'),
    url(r'^tamano_ingrediente/$', views.tamano_ingrediente, name='tamano_ingrediente'),

    ##COMBINACIONES
    url(r'^crear_combinacion/$', views.crear_combinacion, name='crear_combinacion'),
    url(r'^combos_promocionales/$', views.combos_promocionales, name='combos_promocionales'),
    
    ##PROMOCION
    url(r'^promociones/$', views.promociones, name='promociones'),

    ##PORCION
    url(r'^porciones/$', views.porciones, name='porciones'),

    ## ADICIONALES
    url(r'^adicionales/$', views.adicionales, name='adicionales'),
]