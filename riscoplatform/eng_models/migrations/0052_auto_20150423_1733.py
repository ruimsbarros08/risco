# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0051_auto_20150423_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vulnerability_model',
            name='imt',
        ),
        migrations.RemoveField(
            model_name='vulnerability_model',
            name='sa_period',
        ),
        migrations.AddField(
            model_name='vulnerability_function',
            name='imt',
            field=models.CharField(default='SA', max_length=3, choices=[('PGA', 'PGA'), ('PGV', 'PGV'), ('MMI', 'MMI'), ('SA', 'Sa')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vulnerability_function',
            name='sa_period',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
