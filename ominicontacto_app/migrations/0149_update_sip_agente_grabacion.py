# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2018-02-17 14:40
from __future__ import unicode_literals

from django.db import migrations


def update_sip_agente_grabacion(apps, schema_editor):
    """
    Actualiza el sip_extension en agenteprofile
    """

    Grabacion = apps.get_model("ominicontacto_app", "grabacion")
    AgenteProfile = apps.get_model("ominicontacto_app", "agenteprofile")

    for grabacion in Grabacion.objects_default.all():
        try:
            agente = AgenteProfile.objects.get(sip_extension=grabacion.sip_agente)
        except AgenteProfile.DoesNotExist:
            agente = None
        if agente:
            grabacion.sip_agente = 1000 + agente.user.id
            grabacion.save()


def rollback(apps, schema_editor):
    """
    Esta migración es para el reverse_code
    """
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0148_update_username_subscriber'),
    ]

    operations = [
        migrations.RunPython(update_sip_agente_grabacion, reverse_code=rollback),
    ]
