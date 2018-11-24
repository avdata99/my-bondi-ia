# My Bondi Ia
Scrape a MiBondiYa.cba.gov.ar, servicio de transporte interurbano de la provincia de Córdoba

## Uso

Instalar y coso

### Importar datos

Traer las empresas de la home del sitio
```
python manage.py importar_empresas
```

Traer las líneas, orígenes y ramales que tienen las empresas asignadas directamente
```
python manage.py importar_generales
```

Agregar los origenes que tienen algunas líneas
```
python manage.py importar_origenes_desde_lineas
```

Traer los destinos desde los orígenes con lineas
```
python manage.py importar_destinos_desde_origenes
```

Traer orígenes de empresas sin líneas
```
python manage.py importar_origenes_desde_empresas
```