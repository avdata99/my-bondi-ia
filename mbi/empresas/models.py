from django.db import models


class Empresa(models.Model):
    ''' empresas de transporte '''
    nombre = models.CharField(max_length=180)
    id_externo = models.CharField(max_length=10, unique=True)
    # viendo el JS de la página se entiende que YV = Ya Viene
    prop1 = models.CharField(max_length=10, null=True, blank=True, help_text='No se que es todavía (YV o CV)')
    prop2 = models.CharField(max_length=10, null=True, blank=True, help_text='No se que es todavía (0 1 o nulo)')

    def __str__(self):
        return '{} {}'.format(self.nombre, self.id_externo)
