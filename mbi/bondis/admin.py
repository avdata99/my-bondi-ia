from django.contrib import admin
from .models import Esperando, OpcionesEspera

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