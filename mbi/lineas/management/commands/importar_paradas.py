#!/usr/bin/python
from django.core.management.base import BaseCommand

from django.db import transaction
import sys
import datetime
import os
from datetime import date
from empresas.models import Empresa
from lineas.models import Linea, Origen, Ramal, Parada
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = """Comando para traer paradas desde origenes con o sin lineas de MiBondiYa.cba.gov.ar. Es un caos """

    def add_arguments(self, parser):
        parser.add_argument('--empresa_id_externo', type=str, default='NO', help='Id externo de la empresa')
        parser.add_argument('--linea_id_externo', type=str, default='NO', help='Id externo de la linea')
        parser.add_argument('--origen_id_externo', type=str, default='NO', help='Id externo del origen')
        
    # @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Comenzando importacion ---'))
        
        linea_id_externo = options['linea_id_externo']
        empresa_id_externo = options['empresa_id_externo']
        origen_id_externo = options['origen_id_externo']

        if origen_id_externo == 'NO':
            origenes = Origen.objects.all()
        else:
            empresa = Empresa.objects.get(id_externo=empresa_id_externo)
            linea = None if linea_id_externo == 'NO' else Linea.objects.get(id_externo=linea_id_externo, empresa=empresa)
            origen = Origen.objects.get(id_externo=origen_id_externo, empresa=empresa, linea=linea)            
            origenes = [origen]
            self.stdout.write(self.style.SUCCESS('Encontrados {} {} {}'.format(empresa.nombre, linea, origen.nombre)))
        
        for origen in origenes:
            empresa = origen.empresa
            linea = origen.linea
            self.stdout.write(self.style.SUCCESS(' **** ORIGEN {}'.format(origen.nombre)))
            for destino in origen.destinos_posibles.all():
                self.stdout.write(self.style.SUCCESS(' ********* DESTINO {}'.format(destino.nombre)))
                params = {"pCodigoEmpresa": empresa.id_externo,
                            'pCodigoLinea': "" if linea is None else linea.id_externo,
                            'pCodigoOrigen': origen.id_externo,
                            'pCodigoDestino': destino.id_externo}
                headers = {'Content-Type': 'application/json; charset=UTF-8'}
                
                url = 'http://mibondiya.cba.gov.ar/MiBondi.asmx/GetParada'
                        
                
                self.stdout.write(self.style.WARNING('Buscando {} {} {} {} {} {} {}'.format(url, params, origen.nombre, destino.nombre, empresa.nombre, empresa.prop1, empresa.prop2)))
                destinos = requests.post(url, headers=headers, json=params)

                data = destinos.json()
                self.stdout.write(self.style.SUCCESS('Lineas: {}'.format(data)))
                
                ''' ejemplo 
                    {"__type":"MiBondiEntidades.ParadaBE","codigo":"","nombre":"TERMINAL","id":"","descripcion":"TERMINAL"}
                    {"__type":"MiBondiEntidades.ParadaBE","codigo":"MD14","nombre":"PARADA MD14 MUNICIPALIDAD MENDIOLAZA","id":"MD14","descripcion":"PARADA MD14 MUNICIPALIDAD MENDIOLAZA"}
                    {"__type":"MiBondiEntidades.ParadaBE","codigo":"MD15","nombre":"PARADA MD15 PUENTE TALAR","id":"MD15","descripcion":"PARADA MD15 PUENTE TALAR"}
                    {"__type":"MiBondiEntidades.ParadaBE","codigo":"MD16","nombre":"PARADA MD16 KILOMETRO 16","id":"MD16","descripcion":"PARADA MD16 KILOMETRO 16"}
                    {"__type":"MiBondiEntidades.ParadaBE","codigo":"MD18","nombre":"PARADA MD18 CALLE 6","id":"MD18","descripcion":"PARADA MD18 CALLE 6"}]}
                '''
                
                for d in data['d']:
                    if d['__type'] == 'MiBondiEntidades.ParadaBE':
                        parada, created = Parada.objects.get_or_create(id_externo=d['codigo'], 
                                                                        origen=origen, 
                                                                        destino=destino)
                        if not created and parada.nombre != d['nombre']:
                            self.stdout.write(self.style.ERROR('Cambio el nombre {} - {}'.format(parada.nombre, d['nombre'])))    
                            sys.exit(1)
                        parada.nombre = d['nombre']
                        parada.descripcion = d['descripcion']
                        parada.save()
                    else:
                        self.stdout.write(self.style.ERROR('Tipo desconocido {}'.format(d)))
                        sys.exit(1)
                
        self.stdout.write(self.style.SUCCESS('FIN'))
