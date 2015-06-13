# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0063_asset_adm_2'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exposure_model',
            options={},
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='deductible',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('absolute', 'Absolute'), ('relative', 'Relative')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='insurance_limit',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('absolute', 'Absolute'), ('relative', 'Relative')]),
            preserve_default=True,
        ),
        migrations.AlterModelTable(
            name='exposure_model',
            table=None,
        ),
    ]
