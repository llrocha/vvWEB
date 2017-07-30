from django.shortcuts import render

# Create your views here.
from django.http import HttpRequest, HttpResponse
from datetime import datetime
from vv import settings

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

def comparar(request):
    """Renders the comparar page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'vvPromax/comparar.html',
        {
            'menu':'comparar',
            'appname':'vvPromax',
            'title':'Home Page',
            'year':datetime.now().year,
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
            'title':'Home Page',
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
            'title':'Home Page',
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
            'title':'Home Page',
            'year':datetime.now().year,
            'request':request.readlines()
        }
    )