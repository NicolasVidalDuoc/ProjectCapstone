# Generated by Django 4.2.6 on 2023-10-08 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0006_remove_proyecto_cupos_disponibles_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='imagen',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
