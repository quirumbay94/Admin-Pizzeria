from django.conf.urls import url, include
from rest import views

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^registrar$', views.registrar, name='registrar'),

    ## USUARIOS ##
    url(r'^usuario/ver/(?P<usuario_id>\d+)/$$', views.ver_usuario, name='ver_usuario'),
    url(r'^usuario/editar/(?P<usuario_id>\d+)$$', views.editar_usuario, name='editar_usuario'),

    ## PIZZAS TRADICIONALES ##
    url(r'^pizzas_tradicionales', views.ver_pizzas_tradicionales, name='ver_pizzas_tradicionales'),
]