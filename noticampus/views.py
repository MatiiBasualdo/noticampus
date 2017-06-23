from django.shortcuts import render, render_to_response
from django.utils import timezone
from .models import Noticia
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext

# Create your views here.

def inicio(request):
	noticias = Noticia.objects.all().order_by('created_date')
	return render(request, 'inicio.html', {'noticias': noticias})

def nuevo_usuario(request):
	if request.method == 'POST':
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid:
			formulario.save()
			return HttpResponseRedirect('/')
	else:
		formulario = UserCreationForm()
	return render(request, 'nuevo_usuario.html', {'formulario': formulario})

def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/inicio')
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/inicio')
				else:
					return render(request, 'noactivo.html', context=None)
			else:
				return render(request, 'nousuario.html', context=None)
	else:
		formulario = AuthenticationForm()
	return render(request, 'ingresar.html', {'formulario':formulario})

@login_required(login_url='/ingresar')
def privado(request):
	usuario = request.user
	return render(request, 'inicio.html', {'usuario': usuario})

@login_required(login_url='/ingresar')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/')