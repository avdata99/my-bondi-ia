from rest_framework import viewsets
from .serializers import ResultadosEsperaGeoSerializer, ResultadosEsperaSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .pagination import DefaultPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ResultadosEspera
import logging
logger = logging.getLogger(__name__)
import json
from django.utils import timezone
import datetime


class ResultadosEsperaViewSet(viewsets.ModelViewSet):
    """ Colectivos """

    serializer_class = ResultadosEsperaGeoSerializer
    permission_classes = [AllowAny]
    pagination_class = DefaultPagination
    
    def get_queryset(self):
        espera_id = self.request.query_params['espera']
        return ResultadosEspera.objects.filter(opcion_espera__espera__id=espera_id, activo=True).order_by('id')  # primero los primeros resultados