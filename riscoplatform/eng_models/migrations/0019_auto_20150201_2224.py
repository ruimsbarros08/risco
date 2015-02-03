# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0018_auto_20150131_1454'),
    ]

    operations = [
        migrations.AddField(
            model_name='fragility_model',
            name='format',
            field=models.CharField(default='continuous', max_length=10, choices=[('continuous', 'Continuous'), ('discrete', 'Discrete')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fragility_model',
            name='imt',
            field=models.CharField(default='PGA', max_length=3, choices=[('PGA', 'PGA'), ('PGV', 'PGV'), ('MMI', 'MMI'), ('SA', 'Sa')]),
            preserve_default=True,
        ),
    ]
