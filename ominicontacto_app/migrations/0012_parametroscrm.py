# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2019-01-15 15:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0011_sitio_externo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ParametrosCrm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False,
                                        verbose_name='ID')),
                ('nombre', models.CharField(max_length=128)),
                ('valor', models.CharField(max_length=256)),
                ('tipo', models.PositiveIntegerField(
                    choices=[(1, 'Dato de Campa\xf1a'),
                             (2, 'Dato de Contacto'),
                             (3, 'Dato de Llamada'),
                             (4, 'Fijo')])),
                ('campana', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='parametros_crm',
                                              to='ominicontacto_app.Campana')),
            ],
        ),
        migrations.RemoveField(
            model_name='parametroextraparawebform',
            name='campana',
        ),
        migrations.DeleteModel(
            name='ParametroExtraParaWebform',
        ),
    ]