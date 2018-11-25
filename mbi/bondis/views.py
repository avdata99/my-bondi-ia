from rest_framework import viewsets
from .serializers import ResultadosEsperaGeoSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .pagination import DefaultPagination
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ResultadosEspera, Esperando
import logging
logger = logging.getLogger(__name__)
import json
from django.utils import timezone
import datetime
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.clickjacking import xframe_options_exempt


class ResultadosEsperaViewSet(viewsets.ModelViewSet):
    """ Colectivos """

    serializer_class = ResultadosEsperaGeoSerializer
    permission_classes = [AllowAny]
    pagination_class = DefaultPagination
    
    def get_queryset(self):
        espera_id = self.request.query_params['espera']
        esperando = Esperando.objects.get(pk=espera_id)
        ret = esperando.scrape()
        logger.info('Re-Scrape: {}'.format(ret))
        return ResultadosEspera.objects.filter(opcion_espera__espera__id=espera_id, activo=True).order_by('falta_minutos')  # primero los primeros resultados


class MapaDeColectivosView(TemplateView):
    template_name = "bondis/mapa-de-colectivos.html"

    @method_decorator(xframe_options_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['algo'] = 1
        
        return context
