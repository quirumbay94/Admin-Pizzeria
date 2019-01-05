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
    url(r'^ver_pizza$', views.ver_pizza, name='ver_pizza'),
    url(r'^pizzas_tradicionales$', views.ver_pizzas_tradicionales, name='ver_pizzas_tradicionales'),
    url(r'^pizzas_favoritas$', views.pizzas_favoritas, name='pizzas_favoritas'),
    url(r'^crear_pizza_favorita$', views.crear_pizza_favorita, name='crear_pizza_favorita'),
    url(r'^borrar_pizza_favorita$', views.borrar_pizza_favorita, name='borrar_pizza_favorita'),

    ##TAMANOS
    url(r'^tamanos/$', views.tamanos, name='tamanos'),
    url(r'^tamano_masa/$', views.tamano_masa, name='tamano_masa'),
    url(r'^tamano_borde/$', views.tamano_borde, name='tamano_borde'),
    url(r'^tamano_ingrediente/$', views.tamano_ingrediente, name='tamano_ingrediente'),

    ##COMBINACIONES
    url(r'^crear_combinacion/$', views.crear_combinacion, name='crear_combinacion'),
    url(r'^combos_promocionales/$', views.combos_promocionales, name='combos_promocionales'),
    url(r'^carrito/$', views.getCarrito, name='getCarrito'),
    url(r'^carrito/borrar_elemento/$', views.borrarDetalleCarrito, name='borrarDetalleCarrito'),
    url(r'^carrito/editar_cantidad/$', views.editarCantidadCarrito, name='editarCantidadCarrito'),
    

    ##PROMOCION
    url(r'^promociones/$', views.promociones, name='promociones'),

    ##PORCION
    url(r'^porciones/$', views.porciones, name='porciones'),

    ## ADICIONALES
    url(r'^adicionales/$', views.adicionales, name='adicionales'),

    ##DIRECCIONES DEL CLIENTE
    url(r'^direccion_cliente/ver$', views.direcciones_cliente, name='direcciones_cliente'),
    url(r'^direccion_cliente/crear$', views.crear_direccion_cliente, name='crear_direccion_cliente'),   
    url(r'^direccion_cliente/borrar$', views.borrar_direccion_cliente, name='borrar_direccion_cliente'), 
]