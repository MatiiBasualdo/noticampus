from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.ingresar),
	url(r'^usuario/nuevo$', views.nuevo_usuario),
	url(r'^inicio/$', views.inicio),
	url(r'^privado/$',views.privado),
	url(r'^cerrar/$', views.cerrar),
	url(r'^nueva/$', views.nueva_noticia),
	url(r'^noticia/(?P<pk>[0-9]+)/edit/$', views.noticia_edit, name='noticia_edit'),
	url(r'^noticia/(?P<pk>[0-9]+)/delete/$', views.noticia_delete, name="noticia_delete"),
]
