from django.db import models
from django.contrib.gis.db import models as models_geo
from lineas.models import Linea, Origen, Ramal, Parada

class Esperando(models.Model):
    ''' una espera que un usuario puede hacer normalmente (mas de una empresa) en una zona '''
    nombre = models.CharField(max_length=180)
    descripcion = models.TextField(null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)

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


class ResultadosEspera(models.Model):
    ''' cada uno de los colectivos como resultados de las búsquedas en espera '''
    opcion_espera = models.ForeignKey(OpcionesEspera, on_delete=models.CASCADE, related_name='resultados')
    momento = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True, help_text='Antes de que una opcion cargue lo nuevo desactiva todos los existentes de modo que solo se vea la última llamada')
    salida = models.CharField(max_length=300, null=True, blank=True)
    llegada = models.CharField(max_length=300, null=True, blank=True)
    info = models.CharField(max_length=300, null=True, blank=True)
    geo = models_geo.PointField(null=True, blank=True)