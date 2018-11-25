#!/usr/bin/python
from django.core.management.base import BaseCommand

from django.db import transaction
import sys
import datetime
import os
from datetime import date
from bondis.models import Esperando, OpcionesEspera, ResultadosEspera
import requests
from bs4 import BeautifulSoup
import re
from django.contrib.gis.geos import Point

class Command(BaseCommand):
    help = """Comando para traer las empresas desde MiBondiYa.cba.gov.ar """

    def add_arguments(self, parser):
        parser.add_argument('--espera_id', type=int, default=0, help='ejemplo')
        
    # @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Comenzando importacion ---'))
        espera_id = options['espera_id']
        if espera_id == 0:
            esperas = Esperando.objects.all()
        else:
            espera = Esperando.objects.get(pk=espera_id)
            esperas = [espera]
        
        for espera in esperas:
            self.stdout.write(self.style.SUCCESS(' **** ESPERA {}'.format(espera.nombre)))
            for opcion in espera.opciones.all():
                
                # desactivar todos los resultados anteriores
                opcion.resultados.filter(activo=True).update(activo=False)

                url = opcion.get_url()
                self.stdout.write(self.style.SUCCESS(' **** **** OPCION {} {}'.format(opcion.nombre, url)))
                page = requests.get(url)
                soup = BeautifulSoup(page.text, 'html.parser')
                self.stdout.write(self.style.SUCCESS('Sopeando HTML'))
                # soup = BeautifulSoup(open('bondis/management/commands/ejemplo resultados busqueda.html'), 'html.parser')

                select = soup.find(id='divHorarios')
                ul = select.find(id='itemContainer')
                options = ul.find_all('li')
                for op in options:
                    # tiene divs con clases para diferentes secciones: salida, llegada e info
                    salida = op.find("div", class_='salida')
                    text_salida = None
                    if salida is not None:
                        # tiene varios labels pero solo uno visible
                        labels = salida.find_all('label', style="display: initial")
                        textos = []
                        for label in labels:
                            # self.stdout.write(self.style.SUCCESS('SALIDA LBL {}'.format(label)))
                            cleaned = self.clean_text(label)
                            # self.stdout.write(self.style.SUCCESS('SALIDA CTN {}'.format(cleaned)))
                            textos.append(cleaned)
                            # self.stdout.write(self.style.SUCCESS('SALIDA {} {}'.format(len(textos), text_salida)))
                        text_salida = '. '.join(textos)
                    
                    self.stdout.write(self.style.SUCCESS('SALIDA {}'.format(text_salida)))
                    
                    llegada = op.find("div", class_='llegada')
                    text_llegada = None
                    if llegada is not None:
                        text_llegada = self.clean_text(llegada)
                    self.stdout.write(self.style.SUCCESS('LLEGADA {}'.format(text_llegada)))

                    info = op.find("div", class_='info')
                    text_info = None
                    if info is not None:
                        labels = info.find_all('div', style="display: initial")
                        textos = []
                        for label in labels:
                            cleaned = self.clean_text(label)
                            textos.append(cleaned)
                        text_info = '. '.join(textos)
                    self.stdout.write(self.style.SUCCESS('INFO {}'.format(text_info)))

                    latlong_a = info.find_all('a', style="display: initial") 
                    geo = None
                    if len(latlong_a) > 0:  # hay geolocalizacion
                        llh = latlong_a[0]['href']  # https://maps.google.com/?q=-31.163811,-64.321340
                        ll = llh.split("=")[1]
                        lat = float(ll.split(',')[0])
                        lng = float(ll.split(',')[1])
                        self.stdout.write(self.style.SUCCESS('GEO {} {}'.format(lat, lng)))
                        geo = Point(lng, lat, srid=4326)
                    else:
                        self.stdout.write(self.style.SUCCESS('SIN GEO'))
                    
                    # grabar todo a base
                    rese = ResultadosEspera.objects.create(opcion_espera=opcion, activo=True,
                                                    salida=text_salida,
                                                    llegada=text_llegada,
                                                    info=text_info,
                                                    geo=geo)

        self.stdout.write(self.style.SUCCESS('FIN'))
    
    def clean_text(self, lbl):
        res = []
        for txt in lbl.stripped_strings:
            txt = str(txt)
            txt = re.sub(' +',' ', txt)
            txt = txt.replace('\r', '')
            txt = txt.replace('\n', '')
            res.append(txt)
        
        return ' '.join(res)

