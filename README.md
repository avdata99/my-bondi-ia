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

Traer los destinos desde los orígenes (con y sin lineas)
```
python manage.py importar_destinos_desde_origenes
python manage.py importar_destinos_desde_origenes_sin_lineas
```

Traer orígenes de empresas sin líneas
```
python manage.py importar_origenes_desde_empresas
```

Traer todas las paradas del sistema
```
python manage.py importar_paradas
```



