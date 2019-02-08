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
    url(r'^menu/usuario/(?P<usuario_id>\d+)$', views.ver_usuario, name='ver_usuario'),

    ## COMPONENTES
    url(r'^menu/componentes/(?P<tipo>[\w\-]+)$', views.componentes, name='componentes'),
    url(r'^menu/componentes/nuevo_componente/(?P<tipo>[\w\-]+)$', views.nuevo_componente, name='nuevo_componente'),
    url(r'^menu/componentes/(?P<tipo>[\w\-]+)/(?P<componente_id>\d+)$', views.ver_componente, name='ver_componente'),
    url(r'^menu/componentes/editar/(?P<tipo>[\w\-]+)/(?P<componente_id>\d+)$', views.editar_componente, name='editar_componente'),

    ## PIZZAS TRADICIONALES
    url(r'^menu/pizzas_tradicionales$', views.pizzas_tradicionales, name='pizzas_tradicionales'),
    url(r'^menu/pizzas_tradicionales/ver/(?P<pizza_t_id>\d+)$', views.ver_pizza_tradicional, name='ver_pizza_tradicional'),
    url(r'^menu/pizzas_tradicionales/nueva_pizza_tradicional$', views.nueva_pizza_tradicional, name='nueva_pizza_tradicional'),
    url(r'^menu/pizzas_tradicionales/editar/(?P<pizza_t_id>\d+)$', views.editar_pizza_tradicional, name='editar_pizza_tradicional'),

    ## COMBOS PROMOCIONALES
    url(r'^menu/combos_promocionales$', views.combos_promocionales, name='combos_promocionales'),
    url(r'^menu/combos_promocionales/crear$', views.nuevo_combo_promocional, name='nuevo_combo_promocional'),
    url(r'^menu/combos_promocionales/ver/(?P<combo_id>\d+)$', views.ver_combo_promocional, name='ver_combo_promocional'),
    url(r'^menu/combos_promocionales/editar/(?P<combo_id>\d+)$', views.editar_combo_promocional, name='editar_combo_promocional'),

    ##COBERTURA
    url(r'^menu/cobertura$', views.cobertura, name='cobertura'), 
    url(r'^menu/cobertura/local$', views.cobertura_local, name='cobertura_local'), 
    url(r'^menu/cobertura/get_poligonos$', views.get_poligonos, name='get_poligonos'),
    url(r'^menu/cobertura/get_poligono_local$', views.get_poligono_local, name='get_poligono_local'), 
    
    ##LOCALES
    url(r'^menu/local$', views.local, name='local'),
    url(r'^menu/local/crear$', views.crear_local, name='crear_local'),
    url(r'^menu/local/ver/(?P<local_id>\d+)$', views.ver_local, name='ver_local'),
    url(r'^menu/local/editar/(?P<local_id>\d+)$', views.editar_local, name='editar_local'),

    ##RECLAMOS Y SUGERENCIAS
    url(r'^menu/reclamos_sugerencias$', views.reclamos_sugerencias, name='reclamos_sugerencias'),

    ##PEDIDOS
    url(r'^menu/pedidos$', views.pedidos, name='pedidos'),
    url(r'^menu/pedidos/(?P<pedido_id>\d+)$$', views.ver_pedido, name='ver_pedido'),
]






























