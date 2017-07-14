from django.shortcuts import render, render_to_response, redirect
from django.utils import timezone
from .models import Noticia
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.template import RequestContext
from .forms import NoticiaForm
from django.contrib.auth.models import Group, User
from django.shortcuts import render, get_object_or_404
from django.views.defaults import page_not_found

# Create your views here.
@login_required(login_url='/ingresar')
def inicio(request):
    noticias = Noticia.objects.all().order_by('created_date')
    grupo = Group.objects.get(name="Profesores").user_set.all()
    return render(request, 'inicio.html', {'noticias': noticias, 'grupo':grupo})

def noticia_completa(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    return render(request, 'noticia_completa.html', {'noticia': noticia})


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

def nueva_noticia(request):
    if request.method == "POST":
        form = NoticiaForm(request.POST)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.author = request.user
            noticia.published_date = timezone.now()
            noticia.save()
            return HttpResponseRedirect('/inicio')
    else:
        form = NoticiaForm()
        return render(request, 'noticia_edit.html', {'form': form})

def noticia_edit(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    if request.method == "POST":
        form = NoticiaForm(request.POST, instance=noticia)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.author = request.user
            noticia.save()
            return HttpResponseRedirect('/')
    else:
        form = NoticiaForm(instance=noticia)
    if request.user == noticia.author:
        return render(request, 'noticia_edit.html', {'form': form})
    else:
        return render(request, 'noticia_completa.html', {'noticia': noticia})

def noticia_delete(request, pk):
    noticia = get_object_or_404(Noticia, pk=pk)
    noticia.delete()
    return HttpResponseRedirect('/inicio')

def noticia_usuario(request, pk):
    usr = get_object_or_404(User, pk=pk)
    noticias = Noticia.objects.filter(author=usr)
    return render(request, 'noticias_usuario.html', {'noticias': noticias, 'usuario':usr})

