# Generated by Django 2.2.7 on 2022-03-10 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0087_grupo_menu_de_opciones'),
    ]

    operations = [
        migrations.AddField(
            model_name='opcioncalificacion',
            name='interaccion_crm',
            field=models.BooleanField(default=False, verbose_name='Interacción CRM'),
        ),
        migrations.AlterField(
            model_name='campana',
            name='tipo_interaccion',
            field=models.PositiveIntegerField(choices=[(1, 'Formulario'), (2, 'Url externa'), (3, 'Formulario y Url externa')], default=1),
        ),
        migrations.AlterField(
            model_name='parametroscrm',
            name='tipo',
            field=models.PositiveIntegerField(choices=[(1, 'Dato de Campaña'), (2, 'Dato de Contacto'), (3, 'Dato de Llamada'), (4, 'Fijo'), (5, 'Dato de Dialplan'), (6, 'Dato de Calificación ')]),
        ),
        migrations.AlterField(
            model_name='sitioexterno',
            name='disparador',
            field=models.PositiveIntegerField(choices=[(1, 'Agente'), (2, 'Automático'), (3, 'Servidor'), (4, 'Calificación')], default=3),
        ),
    ]
