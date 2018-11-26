from django.db import models
from django.contrib.gis.db import models as models_geo
from lineas.models import Linea, Origen, Ramal, Parada
import requests
from bs4 import BeautifulSoup
import re
from django.contrib.gis.geos import Point
from django.utils import timezone
import datetime


class Esperando(models.Model):
    ''' una espera que un usuario puede hacer normalmente (mas de una empresa) en una zona '''
    nombre = models.CharField(max_length=180)
    descripcion = models.TextField(null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    scraped = models.DateTimeField(default=timezone.now)
    scrape_cada_segundos = models.PositiveIntegerField(default=60)

    def scrape(self):
        if timezone.now() < self.scraped + datetime.timedelta(seconds=self.scrape_cada_segundos):
            return False

        self.scraped = timezone.now()
        self.save()

        for opcion in self.opciones.all():
            opcion.resultados.filter(activo=True).update(activo=False)
            opcion.scrape()
        
        return True

    def __str__(self):
        return self.nombre


class OpcionesEspera(models.Model):
    ''' cada una de las opciones compatibles que tiene un usuario '''
    espera = models.ForeignKey(Esperando, on_delete=models.CASCADE, related_name='opciones')
    nombre = models.CharField(max_length=180)
    descripcion = models.CharField(max_length=180, null=True, blank=True)
    origen = models.ForeignKey('lineas.Origen', null=True, blank=True,on_delete=models.PROTECT, related_name='esperas_como_origen')
    destino = models.ForeignKey('lineas.Origen', null=True, blank=True,on_delete=models.PROTECT, related_name='esperas_como_destino')
    parada = models.ForeignKey('lineas.Parada', null=True, blank=True, on_delete=models.PROTECT, related_name='esperas')
    
    def get_url(self):
        url = 'http://mibondiya.cba.gov.ar/Datos.aspx'
        empresa = '?pCodigoEmpresa={}'.format(self.origen.empresa.id_externo)
        linea = '&pCodigoLinea='  # al parecer no importa, se fija en origen y destino nada mas el buscador
        origen = '&pCodigoOrigen={}'.format(self.origen.id_externo)
        destino = '&pCodigoDestino={}'.format(self.destino.id_externo)
        servicio = '&pServicio={}%20A%20{}'.format(self.origen.nombre, self.destino.nombre)
        parada_str = '' if self.parada is None else self.parada.id_externo
        parada = '&pCodigoParada={}'.format(parada_str)
        proveedor = '&pProveedor={}'.format(self.origen.empresa.prop1)  # yv o cy

        return '{}{}{}{}{}{}{}{}'.format(url, empresa, linea, origen, destino, servicio, parada, proveedor)
    
    def __str__(self):
        return self.nombre
    
    def scrape(self):
        page = requests.get(self.get_url())
        soup = BeautifulSoup(page.text, 'html.parser')
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
                        
            llegada = op.find("div", class_='llegada')
            text_llegada = None
            if llegada is not None:
                text_llegada = self.clean_text(llegada)
            
            info = op.find("div", class_='info')
            text_info = None
            if info is not None:
                labels = info.find_all('div', style="display: initial")
                textos = []
                for label in labels:
                    cleaned = self.clean_text(label)
                    textos.append(cleaned)
                text_info = '. '.join(textos)
            
            latlong_a = info.find_all('a', style="display: initial") 
            geo = None
            if len(latlong_a) > 0:  # hay geolocalizacion
                llh = latlong_a[0]['href']  # https://maps.google.com/?q=-31.163811,-64.321340
                ll = llh.split("=")[1]
                lat = float(ll.split(',')[0])
                lng = float(ll.split(',')[1])
                geo = Point(lng, lat, srid=4326)
            
            # grabar todo a base
            if salida is not None and llegada is not None: 
                rese = ResultadosEspera.objects.create(opcion_espera=self, activo=True,
                                                salida=text_salida,
                                                llegada=text_llegada,
                                                info=text_info,
                                                geo=geo)
    def clean_text(self, lbl):
        res = []
        for txt in lbl.stripped_strings:
            txt = str(txt)
            txt = re.sub(' +',' ', txt)
            txt = txt.replace('\r', '')
            txt = txt.replace('\n', '')
            res.append(txt)

        return ' '.join(res)

class ResultadosEspera(models.Model):
    ''' cada uno de los colectivos como resultados de las búsquedas en espera '''
    opcion_espera = models.ForeignKey(OpcionesEspera, on_delete=models.CASCADE, related_name='resultados')
    momento = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True, help_text='Antes de que una opcion cargue lo nuevo desactiva todos los existentes de modo que solo se vea la última llamada')
    salida = models.CharField(max_length=300, null=True, blank=True)
    llegada = models.CharField(max_length=300, null=True, blank=True)
    info = models.CharField(max_length=300, null=True, blank=True)
    geo = models_geo.PointField(null=True, blank=True)

    # calculados por regex de los textos de mierda
    falta_minutos = models.PositiveIntegerField(null=True, blank=True)
    

    def save(self, *args, **kwargs):
        
        if self.salida is not None:
            # sacar del texto: En 00:17 hs. arriba a tu parada 
            tiempos = re.findall(r'En (\d{2}:\d{2}) hs. arriba', self.salida)  
            if len(tiempos) > 0:
                hs = int(tiempos[0].split(':')[0])
                mint = int(tiempos[0].split(':')[1])
                self.falta_minutos = (60 * hs) + mint
            else:
                # 
                tiempos = re.findall(r'arriba a tu parada a las (\d{2}:\d{2}) hs', self.salida)  
                if len(tiempos) > 0:  # FIXME en realidad no es tiempo faltante, es la hora de mañana a la que llega
                    hs = int(tiempos[0].split(':')[0])
                    mint = int(tiempos[0].split(':')[1])
                    self.falta_minutos = (60 * hs) + mint
        
        super().save(*args, **kwargs)

    def __str__(self):
        return '{} {}'.format(self.opcion_espera.nombre, self.info)