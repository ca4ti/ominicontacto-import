# Generated by Django 2.2.7 on 2021-07-08 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0079_adiciona_acceso_dashboard_agente_grupo'),
    ]

    operations = [
        migrations.AddField(
            model_name='opcioncalificacion',
            name='positiva',
            field=models.BooleanField(default=False, verbose_name='Positiva'),
        ),
    ]
