from django.conf.urls import url, include
from rest import views

urlpatterns = [
    url(r'^login$', views.login, name='login'),
    url(r'^registrar$', views.registrar, name='registrar'),
]