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
]