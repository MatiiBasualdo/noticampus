from django.conf.urls import include, url
from . import views

urlpatterns = [
	url(r'^$', views.ingresar),
	url(r'^usuario/nuevo$', views.nuevo_usuario),
	url(r'^inicio/$', views.inicio),
	url(r'^privado/$',views.privado),
	url(r'^cerrar/$', views.cerrar),

]
