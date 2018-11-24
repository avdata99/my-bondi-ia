from django.contrib import admin
from .models import Linea, Origen, Ramal


@admin.register(Linea)
class LineaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'id_externo', 'empresa']
    search_fields = ['nombre', 'id_externo']
    list_filter = ['empresa']


@admin.register(Origen)
class OrigenAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'id_externo', 'empresa', 'linea']
    search_fields = ['nombre', 'id_externo']
    list_filter= ['empresa', 'linea']


@admin.register(Ramal)
class RamalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'id_externo', 'id_externo2', 'empresa']
    search_fields = ['nombre', 'id_externo', 'id_externo2']
    list_filter = ['empresa']
