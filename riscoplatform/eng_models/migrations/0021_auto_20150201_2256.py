# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0020_auto_20150201_2225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fragility_model',
            name='imt',
        ),
        migrations.AddField(
            model_name='fragility_function',
            name='imt',
            field=models.CharField(default='PGA', max_length=3, choices=[('PGA', 'PGA'), ('PGV', 'PGV'), ('MMI', 'MMI'), ('SA', 'Sa')]),
            preserve_default=True,
        ),
    ]
