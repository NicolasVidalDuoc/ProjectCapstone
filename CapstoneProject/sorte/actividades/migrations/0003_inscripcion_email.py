# Generated by Django 4.2.5 on 2023-10-01 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('actividades', '0002_remove_actividad_cupo_maximo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscripcion',
            name='email',
            field=models.EmailField(default='', max_length=254, unique=True),
        ),
    ]
