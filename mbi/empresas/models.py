from django.db import models


class Empresa(models.Model):
    ''' empresas de transporte '''
    nombre = models.CharField(max_length=180)
    id_externo = models.CharField(max_length=10, unique=True)
    # viendo el JS de la página se entiende que YV = Ya Viene
    prop1 = models.CharField(max_length=10, null=True, blank=True, help_text='No se que es todavía (YV o CV)')
    prop2 = models.CharField(max_length=10, null=True, blank=True, help_text='No se que es todavía (0 1 o nulo)')

    # cosas mias aparte para complementar
    nombre_corto = models.CharField(max_length=30, null=True, blank=True, help_text='Nombre con el que se lo conoce en la práctica')
    color = models.CharField(max_length=10, help_text='Color que representa a la empresa')

    def __str__(self):
        return '{} {}'.format(self.nombre, self.id_externo)
