#!/usr/bin/python
from django.core.management.base import BaseCommand

from django.db import transaction
import sys
import datetime
import os
from datetime import date
from empresas.models import Empresa
from lineas.models import Linea, Origen, Ramal
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = """Comando para traer las origenes directo desde las empresas que no tienen lineas en MiBondiYa.cba.gov.ar. Es un caos """

    def add_arguments(self, parser):
        parser.add_argument('--empresa_id_externo', type=str, default='NO', help='Id externo de la empresa si se desea una sola')
        
    # @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Comenzando importacion ---'))
        
        empresa_id_externo = options['empresa_id_externo']
        if empresa_id_externo == 'NO':
            empresas = Empresa.objects.filter(prop1='yv').exclude(prop2='1')
        else:
            empresa = Empresa.objects.get(id_externo=empresa_id_externo)
            empresas = [empresa]
            self.stdout.write(self.style.SUCCESS('Empresa encontrada {}'.format(empresa.nombre)))
        
        for empresa in empresas:
            params = {"pCodigoEmpresa": empresa.id_externo, 'pCodigoLinea': 0}
            headers = {'Content-Type': 'application/json; charset=UTF-8'}
            
            url = 'http://mibondiya.cba.gov.ar/MiBondi.asmx/GetOrigen'
                    
            
            self.stdout.write(self.style.WARNING('Buscando {} {} {} {} {}'.format(url, params, empresa.nombre, empresa.prop1, empresa.prop2)))
            origenes = requests.post(url, headers=headers, json=params)

            data = origenes.json()
            self.stdout.write(self.style.SUCCESS('Lineas: {}'.format(data)))
            
            
            ''' ejemplo 
                {"d":[
                    {"__type":"MiBondiEntidades.OrigenBE","codigo":"42","nombre":"ALMAFUERTE"}
                    {"__type":"MiBondiEntidades.OrigenBE","codigo":"27","nombre":"ALTO FIERRO"}
                    {"__type":"MiBondiEntidades.OrigenBE","codigo":"167","nombre":"ARROYO CABRAL"}
            '''
            
            for d in data['d']:
                if d['__type'] == 'MiBondiEntidades.OrigenBE':
                    origen, created = Origen.objects.get_or_create(id_externo=d['codigo'], empresa=empresa, linea=None)
                    if not created and origen.nombre != d['nombre']:
                        self.stdout.write(self.style.ERROR('Cambio el nombre {} - {}'.format(origen.nombre, d['nombre'])))    
                        sys.exit(1)
                    origen.nombre = d['nombre']
                    origen.save()
                else:
                    self.stdout.write(self.style.ERROR('Tipo desconocido {}'.format(d)))
                    sys.exit(1)
                
        self.stdout.write(self.style.SUCCESS('FIN'))
