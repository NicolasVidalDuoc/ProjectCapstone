# Generated by Django 4.2.5 on 2023-10-01 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0004_remove_proyecto_cupo_maximo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='cupos_disponibles',
            field=models.PositiveIntegerField(default=30),
        ),
    ]
