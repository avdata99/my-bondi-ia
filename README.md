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

Agregar los origenes que tienen algunas líneas y directo desde las empresas
```
python manage.py importar_origenes_desde_lineas
python manage.py importar_origenes_desde_empresas
```

Traer los destinos desde los orígenes (con y sin lineas)
```
python manage.py importar_destinos_desde_origenes
python manage.py importar_destinos_desde_origenes_sin_linea
```

Traer todas las paradas del sistema
```
python manage.py importar_paradas
```

Crear conjunto de lineas y origenes a gusto, el mío es mendiolaza-cordoba
```
python manage.py crear_espera_mendiolaza_cordoba
```

Buscar colectivos de las esperas activas (hacer cada 1 minuto aprox para mantener datos actualizados en mapa)
```
python manage.py buscar_bondis
```



### Instalar la base de datos 

Dar de alta la base con postgis
```
sudo su - postgres
psql
```

``` sql
CREATE USER mbi WITH PASSWORD 'mbi';
ALTER ROLE mbi SUPERUSER;
CREATE EXTENSION postgis;

CREATE DATABASE mbi OWNER mbi;
```
