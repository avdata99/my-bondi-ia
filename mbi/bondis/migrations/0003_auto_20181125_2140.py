# Generated by Django 2.1.3 on 2018-11-25 21:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bondis', '0002_resultadosespera'),
    ]

    operations = [
        migrations.AddField(
            model_name='esperando',
            name='scrape_cada_segundos',
            field=models.PositiveIntegerField(default=60),
        ),
        migrations.AddField(
            model_name='esperando',
            name='scraped',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
