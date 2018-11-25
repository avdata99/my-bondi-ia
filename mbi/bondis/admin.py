from django.contrib import admin
from .models import Esperando, OpcionesEspera, ResultadosEspera

@admin.register(Esperando)
class EsperandoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre', 'descripcion']


@admin.register(OpcionesEspera)
class OpcionesEsperaAdmin(admin.ModelAdmin):
    def linea(self, obj):
        return obj.origen.linea
    list_display = ['nombre', 'espera', 'origen', 'destino', 'linea']
    search_fields = ['nombre']
    list_filter= ['origen__empresa', 'origen', 'destino']


@admin.register(ResultadosEspera)
class ResultadosEsperaAdmin(admin.ModelAdmin):
    list_display = ['opcion_espera', 'falta_minutos', 'momento', 'activo', 'salida', 'llegada', 'info', 'geo']
    search_fields = ['opcion']