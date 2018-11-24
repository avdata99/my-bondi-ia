from django.db import models


class Linea(models.Model):
    ''' linea de colectivo '''
    empresa = models.ForeignKey('empresas.Empresa', on_delete=models.PROTECT)
    nombre = models.CharField(max_length=180)
    id_externo = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        unique_together = (('empresa', 'id_externo'))


class Origen(models.Model):
    ''' origen de viaje, algunas empresas van directo a origen sin pasar por línea '''
    empresa = models.ForeignKey('empresas.Empresa', on_delete=models.PROTECT, null=True, blank=True)
    linea = models.ForeignKey(Linea, on_delete=models.PROTECT, null=True, blank=True)
    nombre = models.CharField(max_length=180)
    id_externo = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)

    destinos_posibles = models.ManyToManyField('self', blank=True, related_name='origenes')

    def __str__(self):
        return self.nombre

    class Meta:
        unique_together = (('empresa', 'linea', 'id_externo'))


class Ramal(models.Model):
    ''' linea de colectivo '''
    empresa = models.ForeignKey('empresas.Empresa', on_delete=models.PROTECT, null=True, blank=True)
    nombre = models.CharField(max_length=180)
    descripcion = models.CharField(max_length=180, null=True, blank=True)
    id_externo = models.CharField(max_length=40, help_text='codigo se llama al traerlo')
    id_externo2 = models.CharField(max_length=40, help_text='id se llama al traerlo')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        unique_together = (('empresa', 'id_externo'))


class Parada(models.Model):
    ''' puntos de detencion de los colectivos '''
    origen = models.ForeignKey(Origen, on_delete=models.PROTECT, related_name='paradas_origen')
    destino = models.ForeignKey(Origen, on_delete=models.PROTECT, related_name='paradas_destino')
    nombre = models.CharField(max_length=180)
    descripcion = models.CharField(max_length=180, null=True, blank=True)
    id_externo = models.CharField(max_length=40, help_text='codigo se llama al traerlo, hay vacios!')

    class Meta:
        unique_together = (('origen', 'id_externo'))
    
    