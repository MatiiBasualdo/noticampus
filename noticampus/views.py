from django.shortcuts import render
from django.utils import timezone
from .models import Noticia


# Create your views here.

def inicio(request):
	noticias = Noticia.objects.all().order_by('created_date')
	return render(request, 'inicio.html', {'noticias': noticias})




