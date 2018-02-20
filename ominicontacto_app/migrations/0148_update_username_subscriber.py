# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-02-17 14:17
from __future__ import unicode_literals

from django.db import migrations
from django.db import connection


def update_username_alto_in_subscriber(apps, schema_editor):
    """
    Actualiza la tabla subscriber con un valor lo suficientemente alto
    para que no coincida con ningun valor de id de usuario
    """

    cursor = connection.cursor()
    sql = """update subscriber set username = (10000 +id)"""

    cursor.execute(sql)


def update_username_real_in_subscriber(apps, schema_editor):
    """
    Actualiza la tabla subscriber con un valor real
    """

    cursor = connection.cursor()
    sql = """update subscriber set username = (1000 + id)"""

    cursor.execute(sql)


def rollback(apps, schema_editor):
    """
    Esta migración es para el reverse_code
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0147_agregar_tipo_campana_queuelog'),
    ]

    operations = [
        migrations.RunPython(update_username_alto_in_subscriber, reverse_code=rollback),
        migrations.RunPython(update_username_real_in_subscriber, reverse_code=rollback),
    ]
