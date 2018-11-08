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

    ## PIZZAS TRADICIONALES ##
    url(r'^pizzas_tradicionales', views.ver_pizzas_tradicionales, name='ver_pizzas_tradicionales'),

    ##TAMANOS
     url(r'^tamanos', views.tamanos, name='tamanos'),
    url(r'^tamano_masa', views.tamano_masa, name='tamano_masa'),
    url(r'^tamano_borde', views.tamano_borde, name='tamano_borde'),
    url(r'^tamano_ingrediente', views.tamano_ingrediente, name='tamano_ingrediente'),

    ##COMBOS
    url(r'^combos_promocionales', views.combos_promocionales, name='combos_promocionales'),
    
    ##PROMOCION
    url(r'^promociones', views.promociones, name='promociones'),
]