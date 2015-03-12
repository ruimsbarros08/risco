# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0039_auto_20150303_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='exposure_model',
            name='aggregation',
            field=models.CharField(max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exposure_model',
            name='currency',
            field=models.CharField(max_length=5, null=True, choices=[('EUR', 'Euro'), ('DOL', 'Dollar')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='deductible',
            field=models.CharField(default='absolute', max_length=20, null=True, choices=[('absolute', 'absolute'), ('relative', 'relative')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='insurance_limit',
            field=models.CharField(default='absolute', max_length=20, null=True, choices=[('absolute', 'absolute'), ('relative', 'relative')]),
            preserve_default=True,
        ),
    ]
