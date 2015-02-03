# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0019_auto_20150201_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fragility_function',
            name='mean',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fragility_function',
            name='sa_period',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fragility_function',
            name='stddev',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
