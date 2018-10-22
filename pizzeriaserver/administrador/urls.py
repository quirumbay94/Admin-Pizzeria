from django.conf.urls import url, include
from administrador import views

urlpatterns = [
	url(r'^$', views.redireccionar, name='redireccionar'),

	## AUTH
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout_, name='logout_'),

    ## MENU PRINCIPAL
    url(r'^menu$', views.menu, name='menu'),

    ## USUARIOS
    url(r'^menu/usuario$', views.usuario, name='usuario'),
    url(r'^menu/usuario/(?P<usuario_id>\d+)/$', views.ver_usuario, name='ver_usuario'),

    ## COMPONENTES
    url(r'^menu/componentes/(?P<tipo>[\w\-]+)/$', views.componentes, name='componentes'),
    url(r'^menu/componentes/nuevo_componente/(?P<tipo>[\w\-]+)/$', views.nuevo_componente, name='nuevo_componente'),
    url(r'^menu/componentes/(?P<tipo>[\w\-]+)/(?P<componente_id>\d+)/$', views.ver_componente, name='ver_componente'),
    url(r'^menu/componentes/editar/(?P<tipo>[\w\-]+)/(?P<componente_id>\d+)/$', views.editar_componente, name='editar_componente'),

    ## PIZZAS TRADICIONALES
    url(r'^menu/pizzas_tradicionales$', views.pizzas_tradicionales, name='pizzas_tradicionales'),
    url(r'^menu/pizzas_tradicionales/ver/(?P<pizza_t_id>\d+)/$', views.ver_pizza_tradicional, name='ver_pizza_tradicional'),
    url(r'^menu/pizzas_tradicionales/nueva_pizza_tradicional$', views.nueva_pizza_tradicional, name='nueva_pizza_tradicional'),
    url(r'^menu/pizzas_tradicionales/editar/(?P<pizza_t_id>\d+)/$', views.editar_pizza_tradicional, name='editar_pizza_tradicional'),
]