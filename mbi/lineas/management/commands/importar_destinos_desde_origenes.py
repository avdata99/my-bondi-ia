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
    help = """Comando para traer destinos desde las origenes QUE TIENEN LINEA de MiBondiYa.cba.gov.ar. Es un caos """

    def add_arguments(self, parser):
        parser.add_argument('--empresa_id_externo', type=str, default='NO', help='Id externo de la empresa si se desea una sola')
        parser.add_argument('--linea_id_externo', type=str, default='NO', help='Id externo de la linea si se desea una sola')
        parser.add_argument('--origen_id_externo', type=str, default='NO', help='Id externo del origen si se desea una sola')
        
    # @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Comenzando importacion ---'))
        
        linea_id_externo = options['linea_id_externo']
        empresa_id_externo = options['empresa_id_externo']
        origen_id_externo = options['origen_id_externo']

        if origen_id_externo == 'NO':
            origenes = Origen.objects.filter(linea__isnull=False)
        else:
            empresa = Empresa.objects.get(id_externo=empresa_id_externo)
            linea = Linea.objects.get(id_externo=linea_id_externo, empresa=empresa)
            origen = Origen.objects.get(id_externo=origen_id_externo, empresa=empresa)
            origenes = [origen]
            self.stdout.write(self.style.SUCCESS('Encontrados {} {} {}'.format(empresa.nombre, linea.nombre, origen.nombre)))
        
        for origen in origenes:
            empresa = origen.empresa
            linea = origen.linea
            params = {"pCodigoEmpresa": empresa.id_externo,
                        'pCodigoLinea': linea.id_externo,
                        'pCodigoOrigen': origen.id_externo}
            headers = {'Content-Type': 'application/json; charset=UTF-8'}
            
            url = 'http://mibondiya.cba.gov.ar/MiBondi.asmx/GetDestino'
                    
            
            self.stdout.write(self.style.WARNING('Buscando {} {} {} {} {} {}'.format(url, params, linea.nombre, empresa.nombre, empresa.prop1, empresa.prop2)))
            destinos = requests.post(url, headers=headers, json=params)

            data = destinos.json()
            self.stdout.write(self.style.SUCCESS('Lineas: {}'.format(data)))
            
            ''' ejemplo 
                {"d":[
                {"__type":"MiBondiEntidades.DestinoBE","codigo":"1","nombre":"CORDOBA CAPITAL"}
                {"__type":"MiBondiEntidades.DestinoBE","codigo":"132","nombre":"TERMINAL DE UNQUILLO"}
                {"__type":"MiBondiEntidades.DestinoBE","codigo":"194","nombre":"UNQUILLO"}]}
            '''
            
            for d in data['d']:
                if d['__type'] == 'MiBondiEntidades.DestinoBE':  # SON ORIGENES TAMBIEN !!!
                    destino, created = Origen.objects.get_or_create(id_externo=d['codigo'], empresa=empresa, linea=linea)
                    if not created and destino.nombre != d['nombre']:
                        self.stdout.write(self.style.ERROR('Cambio el nombre {} - {}'.format(destino.nombre, d['nombre'])))    
                        sys.exit(1)
                    destino.nombre = d['nombre']
                    destino.linea = linea
                    destino.save()

                    if destino not in origen.destinos_posibles.all():
                        self.stdout.write(self.style.SUCCESS('Agregado {} como destino de {}'.format(destino.nombre, origen.nombre)))    
                        origen.destinos_posibles.add(destino)
                    else:
                        self.stdout.write(self.style.SUCCESS('Ya estaba {} como destino de {}'.format(destino.nombre, origen.nombre)))    
                else:
                    self.stdout.write(self.style.ERROR('Tipo desconocido {}'.format(d)))
                    sys.exit(1)
                
        self.stdout.write(self.style.SUCCESS('FIN'))
