from django.conf.urls import url, include
from administrador import views

urlpatterns = [
	url(r'^$', views.redireccionar, name='redireccionar'),

    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout_, name='logout_'),

    url(r'^menu$', views.menu, name='menu'),
    url(r'^menu/usuario$', views.usuario, name='usuario'),
    url(r'^menu/usuario/(?P<usuario_id>\d+)/$$', views.ver_usuario, name='ver_usuario'),
]