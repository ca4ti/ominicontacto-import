# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2019-03-20 19:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0014_renombra_uid_modelos_grabacion'),
    ]

    operations = [
        migrations.RenameModel('MetadataCliente', 'RespuestaFormularioGestion')
    ]