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
    help = """Comando para traer las origenes desde lineas de las empresas MiBondiYa.cba.gov.ar. Es un caos """

    def add_arguments(self, parser):
        parser.add_argument('--empresa_id_externo', type=str, default='NO', help='Id externo de la empresa si se desea una sola')
        parser.add_argument('--linea_id_externo', type=str, default='NO', help='Id externo de la la linea si se desea una sola')
        
    # @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Comenzando importacion ---'))
        
        linea_id_externo = options['linea_id_externo']
        empresa_id_externo = options['empresa_id_externo']
        if linea_id_externo == 'NO':
            lineas = Linea.objects.all()
        else:
            empresa = Empresa.objects.get(id_externo=empresa_id_externo)
            linea = Linea.objects.get(id_externo=linea_id_externo, empresa=empresa)
            lineas = [linea]
            self.stdout.write(self.style.SUCCESS('Linea encontrada {} {}'.format(empresa.nombre, linea.nombre)))
        
        for linea in lineas:
            empresa = linea.empresa
            params = {"pCodigoEmpresa": empresa.id_externo, 'pCodigoLinea': linea.id_externo}
            headers = {'Content-Type': 'application/json; charset=UTF-8'}
            
            url = 'http://mibondiya.cba.gov.ar/MiBondi.asmx/GetOrigen'
                    
            
            self.stdout.write(self.style.WARNING('Buscando {} {} {} {} {} {}'.format(url, params, linea.nombre, empresa.nombre, empresa.prop1, empresa.prop2)))
            origenes = requests.post(url, headers=headers, json=params)

            data = origenes.json()
            self.stdout.write(self.style.SUCCESS('Lineas: {}'.format(data)))
            
            
            ''' ejemplo 
                {"d":[{"__type":"MiBondiEntidades.OrigenBE","codigo":"1","nombre":"CORDOBA CAPITAL"},
                        {"__type":"MiBondiEntidades.OrigenBE","codigo":"193","nombre":"MENDIOLAZA"},
                        {"__type":"MiBondiEntidades.OrigenBE","codigo":"132","nombre":"TERMINAL DE UNQUILLO"},
                        {"__type":"MiBondiEntidades.OrigenBE","codigo":"194","nombre":"UNQUILLO"}]}
            '''
            
            for d in data['d']:
                if d['__type'] == 'MiBondiEntidades.OrigenBE':
                    origen, created = Origen.objects.get_or_create(id_externo=d['codigo'], empresa=empresa, linea=linea)
                    if not created and origen.nombre != d['nombre']:
                        self.stdout.write(self.style.ERROR('Cambio el nombre {} - {}'.format(origen.nombre, d['nombre'])))    
                        sys.exit(1)
                    origen.nombre = d['nombre']
                    origen.save()
                else:
                    self.stdout.write(self.style.ERROR('Tipo desconocido {}'.format(d)))
                    sys.exit(1)
                
        self.stdout.write(self.style.SUCCESS('FIN'))
