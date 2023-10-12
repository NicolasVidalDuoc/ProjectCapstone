# Generated by Django 4.2.6 on 2023-10-08 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyectos', '0007_proyecto_imagen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proyecto',
            name='imagen',
        ),
        migrations.AddField(
            model_name='proyecto',
            name='imagen_proyecto',
            field=models.ImageField(blank=True, null=True, upload_to='proyectos'),
        ),
    ]
