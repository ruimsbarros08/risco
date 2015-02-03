# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0021_auto_20150201_2256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exposure_model',
            name='area_type',
            field=models.CharField(max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='area_unit',
            field=models.CharField(max_length=20, null=True, choices=[('squared meters', 'Squared meters'), ('hectare', 'Hectare')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='business_int_cost_currency',
            field=models.CharField(max_length=5, null=True, choices=[('EUR', 'Euro'), ('DOL', 'Dollar')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='business_int_cost_type',
            field=models.CharField(max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='contents_cost_currency',
            field=models.CharField(max_length=5, null=True, choices=[('EUR', 'Euro'), ('DOL', 'Dollar')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='contents_cost_type',
            field=models.CharField(max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='deductible',
            field=models.CharField(max_length=20, null=True, choices=[('absolute', 'absolute'), ('relative', 'relative')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='insurance_limit',
            field=models.CharField(max_length=20, null=True, choices=[('absolute', 'absolute'), ('relative', 'relative')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='non_struct_cost_currency',
            field=models.CharField(max_length=5, null=True, choices=[('EUR', 'Euro'), ('DOL', 'Dollar')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='non_struct_cost_type',
            field=models.CharField(max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='struct_cost_currency',
            field=models.CharField(max_length=5, null=True, choices=[('EUR', 'Euro'), ('DOL', 'Dollar')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='struct_cost_type',
            field=models.CharField(max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area')]),
            preserve_default=True,
        ),
    ]
