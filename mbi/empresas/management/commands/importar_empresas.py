#!/usr/bin/python
from django.core.management.base import BaseCommand

from django.db import transaction
import sys
import datetime
import os
from datetime import date
from empresas.models import Empresa
import requests
from bs4 import BeautifulSoup


class Command(BaseCommand):
    help = """Comando para traer las empresas desde MiBondiYa.cba.gov.ar """

    """
    def add_arguments(self, parser):
        parser.add_argument('--algo', type=str, help='ejemplo')
    """
        
    # @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Comenzando importacion ---'))
        url = 'http://mibondiya.cba.gov.ar/'
        page = requests.get(url)

        self.stdout.write(self.style.SUCCESS('Sopeando HTML'))
        soup = BeautifulSoup(page.text, 'html.parser')
        self.stdout.write(self.style.SUCCESS('Select "select"'))
        select = soup.find_all(id='ddlEmpresa')[0]
        options = select.find_all('option')
        for op in options:
            self.stdout.write(self.style.SUCCESS('{}'.format(op)))
            value = op['value']
            txt = op.text
            
            if value == "":
                self.stdout.write(self.style.SUCCESS('Ignorando select {}'.format(op)))
                continue

            values = value.split('|')
            
            id_externo = values[1]
            prop1 = values[0]  # viendo el JS de la página se entiende que YV = Ya Viene
            prop2 = None if len(values) == 2 else values[2]

            empresa, created = Empresa.objects.get_or_create(id_externo=id_externo)
            empresa.nombre = txt
            empresa.prop1 = prop1
            empresa.prop2 = prop2
            empresa.save()

            if created:
                self.stdout.write(self.style.SUCCESS('Empresa creada: {} {}'.format(id_externo, txt)))
            else:
                self.stdout.write(self.style.SUCCESS('Empresa recargada: {} {}'.format(id_externo, txt)))
            
        self.stdout.write(self.style.SUCCESS('FIN'))
