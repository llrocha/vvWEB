from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest, HttpResponse
from datetime import datetime
from vv import settings

def valid_v(k, d):
    if(k in d):
        if(len(d[k])):
            return 'RECEBIDO!'
    return ''

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vvPromax/index.html',
        {
            'menu':'',
            'appname':'vvPromax',
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def listar(request):
    """Renders the verificar page."""
    assert isinstance(request, HttpRequest)
    
    f = valid_v('f', request.GET)
    d = valid_v('d', request.GET)

    return render(
        request,
        'vvPromax/listar.html',
        {
            'menu':'listar',
            'appname':'vvPromax',
            'title':'Listar arquivos',
            'year':datetime.now().year,
            'd': d,
            'f': f,
        }
    )

def verificar(request):
    """Renders the verificar page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vvPromax/verificar.html',
        {
            'menu':'verificar',
            'appname':'vvPromax',
            'title':'Verificar existência',
            'year':datetime.now().year,
        }
    )

def comparar(request):
    """Renders the comparar page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vvPromax/comparar.html',
        {
            'menu':'comparar',
            'appname':'vvPromax',
            'title':'Comparar pastas/arquivos',
            'year':datetime.now().year,
        }
    )

def contato(request):
    """Renders the contato page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vvPromax/contato.html',
        {
            'menu':'contato',
            'appname':'vvPromax',
            'title':'Contato',
            'year':datetime.now().year,
        }
    )

def sobre(request):
    """Renders the sobre page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vvPromax/sobre.html',
        {
            'menu':'sobre',
            'appname':'vvPromax',
            'title':'Sobre',
            'year':datetime.now().year,
            'request':request,
        }
    )