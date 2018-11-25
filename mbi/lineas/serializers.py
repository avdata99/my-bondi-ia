from .models import Linea, Origen
from rest_framework import serializers
from empresas.serializers import EmpresaSerializer

class OrigenSerializer(serializers.ModelSerializer):
    empresa = EmpresaSerializer()
    
    class Meta:
        model = Origen
        fields = ('id', 'nombre', 'id_externo', 'empresa')