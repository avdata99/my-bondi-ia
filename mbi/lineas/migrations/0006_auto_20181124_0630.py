# Generated by Django 2.1.3 on 2018-11-24 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('empresas', '0001_initial'),
        ('lineas', '0005_origen_destinos_posibles'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='origen',
            unique_together={('empresa', 'linea', 'id_externo')},
        ),
    ]
