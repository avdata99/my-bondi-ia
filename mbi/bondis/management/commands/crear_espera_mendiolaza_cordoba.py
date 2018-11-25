#!/usr/bin/python
from django.core.management.base import BaseCommand

from django.db import transaction
import sys
from bondis.models import Esperando, OpcionesEspera
from lineas.models import Origen
from empresas.models import Empresa


class Command(BaseCommand):
    help = """Crar esperas para mendiolaza - cordoba """

    # @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Comenzando creación ---'))
        espera, created = Esperando.objects.get_or_create(nombre = 'Mendiolaza - Córdoba')

        """
        inter_mendio_cba          = 'http://mibondiya.cba.gov.ar/Datos.aspx?pCodigoEmpresa=300&pCodigoLinea=&pCodigoOrigen=3&pCodigoDestino=1&pServicio=MENDIOLAZA%20A%20CORDOBA&pCodigoParada=MD16&pProveedor=yv'
        inter_mendio_cba_KM16     = 'http://mibondiya.cba.gov.ar/Datos.aspx?pCodigoEmpresa=300&pCodigoLinea=&pCodigoOrigen=3&pCodigoDestino=1&pServicio=MENDIOLAZA%20A%20CORDOBA&pCodigoParada=&pProveedor=yv'
        samiento_mendio_cba_talar = 'http://mibondiya.cba.gov.ar/Datos.aspx?pCodigoEmpresa=401&pCodigoLinea=3&pCodigoOrigen=193&pCodigoDestino=1&pServicio=MENDIOLAZA%20A%20CORDOBA%20CAPITAL&pCodigoParada=&pProveedor=yv'
        samiento_mendio_cba_valla = 'http://mibondiya.cba.gov.ar/Datos.aspx?pCodigoEmpresa=401&pCodigoLinea=6&pCodigoOrigen=193&pCodigoDestino=1&pServicio=MENDIOLAZA%20A%20CORDOBA%20CAPITAL&pCodigoParada=&pProveedor=yv'
        // si le saco la linea a los de arriba muestra a los dos juntos
        fonobus_mendio_cba        = 'http://mibondiya.cba.gov.ar/Datos.aspx?pCodigoEmpresa=3300&pCodigoLinea=G3&pCodigoOrigen=127&pCodigoDestino=1&pServicio=MENDIOLAZA%20A%20CORDOBA%20CAPITAL&pCodigoParada=&pProveedor=yv'
        """

        empresa = Empresa.objects.get(id_externo='300')  # intercordoba
        origen = Origen.objects.get(empresa=empresa, id_externo='3')  # Mendiolaza (segun esta empresa)
        destino = Origen.objects.get(empresa=empresa, id_externo='1')  # Cordoba (segun esta empresa)
        opcion, created = OpcionesEspera.objects.get_or_create(espera=espera, nombre='con InterCordoba', origen=origen, destino=destino)

        empresa = Empresa.objects.get(id_externo='401')  # sarmiento
        # Tiene varias lineas pero no las necesitamos
        origen = Origen.objects.get(empresa=empresa, id_externo='193', linea__id_externo='3')  # Mendiolaza (segun esta empresa)
        destino = Origen.objects.filter(empresa=empresa, id_externo='1', linea__id_externo='3').first()  # Cordoba (segun esta empresa)
        opcion, created = OpcionesEspera.objects.get_or_create(espera=espera, nombre='con Sarmiento', origen=origen, destino=destino)

        empresa = Empresa.objects.get(id_externo='3300')  # fonobus
        origen = Origen.objects.filter(empresa=empresa, id_externo='127', linea__id_externo='G3').first()  # Mendiolaza (segun esta empresa)
        destino = Origen.objects.filter(empresa=empresa, id_externo='1', linea__id_externo='G3').first()  # Cordoba (segun esta empresa)
        opcion, created = OpcionesEspera.objects.get_or_create(espera=espera, nombre='con Fonobus', origen=origen, destino=destino)


        self.stdout.write(self.style.SUCCESS('FIN'))
