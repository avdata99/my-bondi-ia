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
    help = """Comando para traer las lineas, origenes y ramales desde las empresas MiBondiYa.cba.gov.ar. Es un caos """

    def add_arguments(self, parser):
        parser.add_argument('--empresa_id_externo', type=str, default='NO', help='Id externo de la empresa si se desea una sola')

    
        
    # @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Comenzando importacion ---'))
        
        id_externo = options['empresa_id_externo']
        if id_externo == 'NO':
            empresas = Empresa.objects.all()
        else:
            empresa = Empresa.objects.get(id_externo=id_externo)
            empresas = [empresa]
            self.stdout.write(self.style.SUCCESS('Empresa encontrada {} {} {}'.format(empresa.nombre, empresa.prop1, empresa.prop2)))
        
        for empresa in empresas:
            params = {"pCodigoEmpresa": empresa.id_externo}
            headers = {'Content-Type': 'application/json; charset=UTF-8'}
            
            if empresa.prop1 == 'yv':
                if empresa.prop2 == '1':
                    url = 'http://mibondiya.cba.gov.ar/MiBondi.asmx/GetLineas'
                else:
                    url = 'http://mibondiya.cba.gov.ar/MiBondi.asmx/GetOrigen'
                    params['pCodigoLinea'] = 0
            else: 
                url = 'http://mibondiya.cba.gov.ar/MiBondi.asmx/GetRamal'
            
            self.stdout.write(self.style.WARNING('Buscando {} {} {} {} {}'.format(url, params, empresa.nombre, empresa.prop1, empresa.prop2)))
            lineas = requests.post(url, headers=headers, json=params)

            data = lineas.json()
            self.stdout.write(self.style.SUCCESS('Lineas: {}'.format(data)))
            
            
            ''' ejemplo de lineas u origenes 
                {'__type': 'MiBondiEntidades.OrigenBE', 'codigo': '43', 'nombre': 'CRUCE ALMAFUERTE'} 
                {'__type': 'MiBondiEntidades.LineaBE', 'codigo': '0', 'nombre': 'TODAS', 'empresa': '12901'}
                {"__type":"MiBondiEntidades.RamalBE","codigo":"1","nombre":"TANTI","empresa":null,"id":"1","descripcion":"TANTI"}
            '''

            for d in data['d']:
                if d['__type'] == 'MiBondiEntidades.LineaBE':
                    linea, created = Linea.objects.get_or_create(id_externo=d['codigo'], empresa=empresa)
                    linea.nombre = d['nombre']
                    linea.save()
                elif d['__type'] == 'MiBondiEntidades.OrigenBE':
                    origen, created = Origen.objects.get_or_create(id_externo=d['codigo'], empresa=empresa)
                    if not created and origen.nombre != d['nombre']:
                        self.stdout.write(self.style.ERROR('Cambio el nombre {} - {}'.format(origen.nombre, d['nombre'])))    
                        sys.exit(1)
                    origen.nombre = d['nombre']
                    origen.save()
                elif d['__type'] == 'MiBondiEntidades.RamalBE':
                    ramal, created = Ramal.objects.get_or_create(id_externo=d['codigo'], empresa=empresa)
                    ramal.nombre = d['nombre']
                    ramal.id_externo2 = d['id']
                    ramal.descripcion = d['descripcion']
                    ramal.save()
                
                else:
                    self.stdout.write(self.style.ERROR('Tipo desconocido {}'.format(d)))
                    sys.exit(1)
                
        self.stdout.write(self.style.SUCCESS('FIN'))
