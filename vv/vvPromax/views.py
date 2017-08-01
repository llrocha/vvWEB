from django.shortcuts import render

# Create your views here.
import urllib
from django.http import HttpRequest, HttpResponse
from datetime import datetime
from vv import settings
from verifica_versao import GEO_IP, VersionVerify

def valid_v(k, d, default = ''):
    if(k in d):
        if(len(d[k])):
            return urllib.parse.unquote(d[k])
    return default

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
    
    l = valid_v('Listar', request.GET, '')
    f = valid_v('f', request.GET, '*.gnt')
    d = valid_v('d', request.GET, '.')
    g = valid_v('geo', request.GET, '')

    if(l and g):
        vv = VersionVerify()
        vv.loadfilesfromgeo(g, d, f)
        context = {
            'menu': 'listar',
            'appname': 'vvPromax',
            'title': 'Listar arquivos',
            'year': datetime.now().year,
            'd': d,
            'f': f,
            'listar': True,
            'files': vv.filesfromgeo(g),
            'geo': g
        }
    else:
        context = {
            'menu':'listar',
            'appname':'vvPromax',
            'title':'Listar arquivos',
            'year':datetime.now().year,
            'd': d,
            'f': f,
            'geos': GEO_IP.keys()
        }

    return render(
        request,
        'vvPromax/listar.html',
        context
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