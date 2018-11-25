#!/usr/bin/python
from django.core.management.base import BaseCommand

from django.db import transaction
import sys
import datetime
import os
from datetime import date
from bondis.models import Esperando, OpcionesEspera
import requests
from bs4 import BeautifulSoup
import re

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
                    text_salida = 'Sin datos de la salida'
                    if salida is not None:
                        # tiene varios labels pero solo uno visible
                        labels = salida.find_all('label', style="display: initial")
                        textos = []
                        for label in labels:
                            self.stdout.write(self.style.SUCCESS('SALIDA LBL {}'.format(label)))
                            lst = label.string
                            self.stdout.write(self.style.SUCCESS('SALIDA CTN {}'.format(lst)))
                            cleaned = self.clean_text(lst)
                            self.stdout.write(self.style.SUCCESS(cleaned))
                            textos.append(cleaned)
                        text_salida = '. '.join(textos)
                    
                    self.stdout.write(self.style.SUCCESS('SALIDA {}'.format(text_salida)))
                    
                    llegada = op.find("div", class_='llegada')
                    text_llegada = 'Sin datos de llegada'
                    if llegada is not None:
                        text_llegada = self.clean_text(llegada.string)
                    self.stdout.write(self.style.SUCCESS('LLEGADA {}'.format(text_llegada)))

                    info = op.find("div", class_='info')
                    text_info = 'Sin informacion adicional en {}'.format(op)
                    if info is not None:
                        labels = info.find_all('div', style="display: initial")
                        textos = []
                        for label in labels:
                            textos.append(self.clean_text(label.contents[0]))
                        text_info = '. '.join(textos)
                    self.stdout.write(self.style.SUCCESS('INFO {}'.format(text_info)))

                    latlong_a = info.find_all('a', style="display: initial") 
                    if len(latlong_a) > 0:  # hay geolocalizacion
                        llh = latlong_a[0]['href']  # https://maps.google.com/?q=-31.163811,-64.321340
                        ll = llh.split("=")[1]
                        lat = ll.split(',')[0]
                        lng = ll.split(',')[1]
                        self.stdout.write(self.style.SUCCESS('GEO {} {}'.format(lat, lng)))
                    else:
                        self.stdout.write(self.style.SUCCESS('SIN GEO'))
            
        self.stdout.write(self.style.SUCCESS('FIN'))
    
    def clean_text(self, txt):
        # txt = str(txt)
        txt = txt.replace('\n', '').strip()
        txt = txt.replace('\t', '')
        txt = re.sub(' +',' ', txt)
        return txt

