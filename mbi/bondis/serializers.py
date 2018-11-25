from .models import ResultadosEspera
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers


class ResultadosEsperaGeoSerializer(GeoFeatureModelSerializer):
    
    class Meta:
        model = ResultadosEspera
        geo_field = 'geo'
        fields = ('id', 'momento', 'salida', 'llegada', 'info')


class ResultadosEsperaSerializer(serializers.ModelSerializer):

    class Meta:
        model = ResultadosEspera
        fields = ('id', 'momento', 'salida', 'llegada', 'info')