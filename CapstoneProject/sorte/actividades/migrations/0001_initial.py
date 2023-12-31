# Generated by Django 4.2.5 on 2023-09-18 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Actividad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_actividad', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('direccion', models.CharField(max_length=200)),
                ('region', models.CharField(choices=[('RM', 'Región Metropolitana')], default='RM', max_length=100)),
                ('comuna', models.CharField(choices=[('Isla de Maipo', 'Isla de Maipo')], default='Isla de Maipo', max_length=100)),
                ('fecha_actividad', models.DateField()),
                ('hora_inicio', models.TimeField()),
                ('hora_termino', models.TimeField()),
                ('cupo_minimo', models.IntegerField()),
                ('cupo_maximo', models.IntegerField()),
            ],
            options={
                'verbose_name': 'actividad',
                'verbose_name_plural': 'actividades',
            },
        ),
    ]
