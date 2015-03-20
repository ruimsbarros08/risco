# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0040_auto_20150310_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exposure_model',
            name='area_type',
            field=models.CharField(max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_asset', 'Per asset')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='deductible',
            field=models.CharField(default='absolute', max_length=20, null=True, choices=[('absolute', 'Absolute'), ('relative', 'Relative')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='insurance_limit',
            field=models.CharField(default='absolute', max_length=20, null=True, choices=[('absolute', 'Absolute'), ('relative', 'Relative')]),
            preserve_default=True,
        ),
    ]
