# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0018_auto_20150201_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario_damage',
            name='error',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scenario_damage',
            name='oq_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scenario_damage',
            name='ready',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scenario_damage',
            name='start',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
