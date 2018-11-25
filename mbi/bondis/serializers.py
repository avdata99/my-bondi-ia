from .models import ResultadosEspera, Esperando, OpcionesEspera
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from lineas.serializers import OrigenSerializer


class EsperandoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Esperando
        fields = ('id', 'nombre', 'descripcion', 'scraped')


class OpcionesEsperaSerializer(serializers.ModelSerializer):
    espera = EsperandoSerializer()
    origen = OrigenSerializer()
    destino = OrigenSerializer()
    class Meta:
        model = OpcionesEspera
        fields = ('id', 'nombre', 'descripcion', 'espera', 'origen', 'destino')


class ResultadosEsperaGeoSerializer(GeoFeatureModelSerializer):
    opcion_espera = OpcionesEsperaSerializer()

    class Meta:
        model = ResultadosEspera
        geo_field = 'geo'
        fields = ('id', 'falta_minutos', 'momento', 'salida', 'llegada', 'info', 'opcion_espera')


