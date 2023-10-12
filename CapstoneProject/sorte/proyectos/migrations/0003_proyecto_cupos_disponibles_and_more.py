# Generated by Django 4.2.5 on 2023-09-29 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0002_solicitud'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='cupos_disponibles',
            field=models.PositiveIntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='cupo_maximo',
            field=models.PositiveIntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='cupo_minimo',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
