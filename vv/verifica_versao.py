#!/usr/bin/python3

import os
import logging
import urllib.request
import threading
import subprocess
import time

"""
PARAM 0 = IP ou HOST
PARAM 1 = OPERATION f or d
PARAM 2 = DIRECTORY
PARAM 3 = MASK
"""
URL = 'http://{0}/cgi-bin/verifica_versao.exe?f={1}/{2}'

GEOS = (
    'ac', 'ba', 'co', 'mg', 'no', 'pr', 'rj', 'sp', 'su',
    'tt', 'tc', 'qa', 't1', 't2', 't3', 't4', 'tc', 'te', 'tr'
)

SERVERS = [
    'acsxpa', 'acsxp0', 'acsxp1', 'acsxp2',
    'acsxp3', 'acsxp7', 'acsxp8', 'acsxp9',
]

SERVER_GEO = {
    'acsxpa':['tt', 'tc', 'qa'],
    'acsxp0':['t1', 't2', 't3', 't4', 'tc', 'te', 'tr'],
    'acsxp1':[],
    'acsxp2':['ac', 'co', 'sp'],
    'acsxp3':['mg'],
    'acsxp7':['ba'],
    'acsxp8':['no', 'rj'],
    'acsxp9':['pr', 'su'],
}

GEO_IP = {
    'ac':'172.22.4.244',
    'ba':'172.22.5.35',
    'co':'172.22.4.243',
    'mg':'172.22.4.239',
    'no':'172.22.4.248',
    'pr':'172.22.4.249',
    'rj':'172.22.4.246',
    'sp':'172.22.4.242',
    'su':'172.22.4.237',
    'tt':'172.22.4.252',
    'tc':'172.22.4.251',
    'qa':'172.22.4.253',
    't1':'172.19.117.111',
    't2':'172.19.117.112',
    't3':'172.19.117.113',
    't4':'127.0.0.1',
    'tc':'172.19.117.110',
    'te':'172.19.117.114',
    'tr':'172.19.117.115',
}

SERVER_IP = {
    'lpar': {
        'acsxpa':'172.22.4.221',
        'acsxp0':'172.19.117.109',
        'acsxp2':'172.22.4.236',
        'acsxp3':'172.22.4.238',
        'acsxp7':'172.22.4.241',
        'acsxp8':'172.22.4.245',
        'acsxp9':'172.22.4.247',
        'acsxnfex01':'172.22.8.96',
        'acsxnfex02':'172.22.4.151',
    },
    'virtual':{
        'acprxac':'172.22.4.244',
        'acprxba':'172.22.5.35',
        'acprxco':'172.22.4.243',
        'acprxmg':'172.22.4.239',
        'acprxno':'172.22.4.248',
        'acprxpr':'172.22.4.249',
        'acprxrj':'172.22.4.246',
        'acprxsp':'172.22.4.242',
        'acprxsu':'172.22.4.237',
        'acprxtt':'172.22.4.252',
        'acprxtc':'172.22.4.251',
        'acprxqa':'172.22.4.253',
        'acprxt1':'172.19.117.111',
        'acprxt2':'172.19.117.112',
        'acprxt3':'172.19.117.113',
        'acprxt4':'127.0.0.1',
        'acprxtc':'172.19.117.110',
        'acprxte':'172.19.117.114',
        'acprxtr':'172.19.117.115',
    }
}

def verifica_versao_url(geo, d, f):
    if(geo in GEO_IP.keys()):
        return URL.format(GEO_IP[geo], d, f)
    else:
        return None

def valid_v(k, d, default = ''):
    if(k in d):
        return d[k]
    return default

class VersionVerifyFileException(Exception):
    """Raise VerifyFileException Exception"""

class VersionVerifyException(Exception):
    """Raise VersionVerify Exception"""

class VersionVerifyFile:
    """
    VerifyFile classe que representa um arquivo pesquisado no servidor para comparação
    """
    def __init__(self, *args, **kwargs):
        if(len(args) == 5):
            self.servidor = args[0]
            self.version = args[1]
            self.md5sum = args[2]
            self.raw_info = args[3]
            self.name = args[4]
        else:
            raise Exception("Quantidade inválida de parâmetros")

    def FileInfo(self):
        mask = 'Tipo: {0}, Usuário: {1}, Grupo: {2}, Permissão: {3}, mtime: {4} {5}, ctime: {6} {7}'
        return mask.format(*(self.raw_info.split('.')))

    def __str__(self):
        return "{0};{1};{2};{3};{4}".format(
            self.servidor,
            self.version,
            self.md5sum,
            self.raw_info,
            self.name
        )


class VersionVerify:
    """
    Classe para executar query de validação de distribuição dos Promax
    """

    def __init__(self):
        self.files = []
        self.response = {}
        self.file_array = []
        logger.debug('Criando objeto VersionVerify()')


    def loadfilesfromgeo(self, geo, dir = '.', mask = '*.exe'):
        """
        loadfilesfromserver(geo, dir, mask)
        Carrega arquivos do HOST diretório com máscara especificada para verificação.
        """

        url = ''
        if(geo in GEO_IP.keys()):
            url = verifica_versao_url(geo, dir, mask)
            logger.debug('URL: {0}'.format(url))
        else:
            raise VersionVerifyException('Host inválido!')

        if(geo not in self.response.keys() or not self.response[geo]):
            try:
                r = urllib.request.urlopen(url)
                self.response[geo] = {}
                for line in r.readlines():
                    line = line.decode().expandtabs().split()
                    o = VersionVerifyFile(geo, *line)
                    self.response[geo][o.name] = o
                r.close()
            except:
                self.response[geo] = b''

    def filesfromgeo(self, geo):
        """
        filesfromgeo(geo) = retorna lista de arquivos de uma geo
        """
        r = []
        for k in self.response[geo]:
            v = self.response[geo][k]
            r.append([v.servidor,v.name,v.version,v.md5sum,v.raw_info])
        return r

    def comparegeofiles(self, *args):
        """
        comparegeofiles(*args), args = lista de geos a serem comparadas, compara o MD5SUM dos arquivos
        com mesmo nome, retorna uma lista com os nomes de arquivos únicos e o status TRUE = tudo 
        igual e False = uma das GEOS com arquivos diferentes.
        """
        f = []
        r = {}
        for geo in args:
            f = f + list(self.response[geo].keys())

        f = list(set(f))

        for filename in f:
            equal = True
            md5sum = ''
            for geo in args:
                if(filename in self.response[geo].keys()):
                    if(len(md5sum) == 0):
                        md5sum = self.response[geo][filename].md5sum
                    if(self.response[geo][filename].md5sum != md5sum):
                        equal = False
                        break
                else:
                    equal = False
                    break
            r[filename] = equal

        return r

    def existgeofiles(self, *args):
        """
        existgeofiles(*args), args = lista de geos a serem comparadas, verifica se os arquivos nas 
        GEOS da lista existem uma na outra
        """
        f = []
        r = {}
        for geo in args:
            f = f + list(self.response[geo].keys())

        f = list(set(f))

        for filename in f:
            r[filename] = {}
            for geo in args:
                r[filename][geo] = (filename in self.response[geo].keys())

        return r


    def matrixgeofiles(self, *args):
        """
        MatrixGeoFiles(*args), args = lista de geos a serem retornadas. Retorna matriz de MD5SUM
        """
        r = {}
        f = []
        for geo in args:
            f = f + list(self.response[geo].keys())
        files = list(set(f))
        for f in files:
            if(f not in r.keys()):
                r[f] = {}
            for geo in self.response.keys():
                file = valid_v(f, self.response[geo])
                if(file):
                    r[f][geo] = self.response[geo][f].md5sum
                else:
                    r[f][geo] = ''
        return r


class LoadFilesFromGeo(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)

        self.vv = kwargs['vv']
        self.geo = kwargs['geo']
        self.pool = kwargs['pool']
        self.dir = kwargs['dir']
        self.mask = kwargs['mask']

    def run(self):
        self.vv.loadfilesfromgeo(self.geo, self.dir, self.mask)
        self.pool.release()

class LoadGeos(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)

        self.jobs = []
        self.vv = VersionVerify()
        self.geos = kwargs['geos']
        self.pool = kwargs['pool']

        if('dir' in kwargs.keys()):
            self.dir = kwargs['dir']
        else:
            self.dir = '.'
        if('mask' in kwargs.keys()):
            self.mask = kwargs['mask']
        else:
            self.mask = '*.exe'
          
    def run(self):
        for geo in self.geos:
            self.pool.acquire()
            kwargs = {
                'vv': self.vv, 
                'pool': self.pool, 
                'geo': geo, 
                'dir': self.dir, 
                'mask': self.mask
            }
            job = LoadFilesFromGeo(**kwargs)
            job.setDaemon(True)
            job.start()
            self.jobs.append(job)

        for job in self.jobs:
            job.join()

class GeoLoader():
    def __init__(self, *args, **kwargs):
        if('geos' in kwargs.keys()):
            self.thread_count = len(kwargs['geos'])
        else:
            raise VersionVerifyException('Erro não foram passadas as GEO\'s')

        self.pool = threading.BoundedSemaphore(value = self.thread_count)
        self.loader = LoadGeos(pool=self.pool, **kwargs)

    def load(self):
        self.loader.start()
        self.loader.join()



#LOG CONFIG
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
#create file handler
handler = logging.FileHandler('{0}.log'.format(__name__))
handler.setLevel(logging.ERROR)
# create formatter
formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)