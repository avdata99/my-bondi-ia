from .models import Empresa
from rest_framework import serializers


class EmpresaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Empresa
        fields = ('id', 'nombre', 'id_externo')