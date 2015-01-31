# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0016_auto_20150131_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fragility_function',
            name='dist_type',
            field=models.CharField(default='lognormal', max_length=20, choices=[('lognormal', 'Lognormal')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fragility_function',
            name='limit_state',
            field=models.CharField(max_length=20, choices=[('slight', 'Slight'), ('moderate', 'Moderate'), ('extensive', 'Extensive'), ('complete', 'Complete')]),
            preserve_default=True,
        ),
    ]
