# Generated by Django 4.2.5 on 2023-10-01 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('actividades', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actividad',
            name='cupo_maximo',
        ),
        migrations.RemoveField(
            model_name='actividad',
            name='cupo_minimo',
        ),
        migrations.AddField(
            model_name='actividad',
            name='cupos_disponibles',
            field=models.PositiveIntegerField(default=20),
        ),
        migrations.CreateModel(
            name='Inscripcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12)),
                ('nombre_usuario', models.CharField(max_length=50)),
                ('apellido_usuario', models.CharField(max_length=50)),
                ('comentarios', models.TextField(max_length=200)),
                ('confirmada', models.BooleanField(default=False)),
                ('rechazada', models.BooleanField(default=False)),
                ('estado', models.CharField(default='Pendiente', max_length=20)),
                ('actividad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actividades.actividad')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
