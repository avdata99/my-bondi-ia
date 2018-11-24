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
    '''
    {"d":[
        {"__type":"MiBondiEntidades.ParadaBE","codigo":"","nombre":"TERMINAL","id":"","descripcion":"TERMINAL"}
        {"__type":"MiBondiEntidades.ParadaBE","codigo":"147","nombre":"PARADA 147 ND - UNQ","id":"147","descripcion":"PARADA 147 ND - UNQ"}]}
    
    {"d":[
        {"__type":"MiBondiEntidades.ParadaBE","codigo":"","nombre":"TERMINAL","id":"","descripcion":"TERMINAL"}
        {"__type":"MiBondiEntidades.ParadaBE","codigo":"MD14","nombre":"PARADA MD14 MUNICIPALIDAD MENDIOLAZA","id":"MD14","descripcion":"PARADA MD14 MUNICIPALIDAD MENDIOLAZA"}
        {"__type":"MiBondiEntidades.ParadaBE","codigo":"MD15","nombre":"PARADA MD15 PUENTE TALAR","id":"MD15","descripcion":"PARADA MD15 PUENTE TALAR"}
        {"__type":"MiBondiEntidades.ParadaBE","codigo":"MD16","nombre":"PARADA MD16 KILOMETRO 16","id":"MD16","descripcion":"PARADA MD16 KILOMETRO 16"}
        {"__type":"MiBondiEntidades.ParadaBE","codigo":"MD18","nombre":"PARADA MD18 CALLE 6","id":"MD18","descripcion":"PARADA MD18 CALLE 6"}]}
    '''