# Generated by Django 2.2.7 on 2020-11-13 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0067_delete_grabacion'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='queue',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='campana',
            name='videocall_habilitada',
            field=models.BooleanField(default=False),
        ),
    ]