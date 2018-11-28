from django.contrib import admin
from .models import Empresa

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'nombre_corto', 'color', 'id_externo', 'prop1', 'prop2']
    search_fields = ['nombre', 'id_externo']
    list_filter= ['prop1', 'prop2']