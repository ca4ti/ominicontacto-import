# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-02 20:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0040_auto_20170102_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='campana',
            name='formulario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='ominicontacto_app.Formulario'),
            preserve_default=False,
        ),
    ]
