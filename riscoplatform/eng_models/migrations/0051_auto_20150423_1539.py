# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0050_auto_20150413_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='area',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='asset',
            name='n_buildings',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='aggregation',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='area_type',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_asset', 'Per asset')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='area_unit',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('squared meters', 'Squared meters'), ('hectare', 'Hectare')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='business_int_cost_currency',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[('EUR', 'Euro'), ('USD', 'US Dollar')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='business_int_cost_type',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='contents_cost_currency',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[('EUR', 'Euro'), ('USD', 'US Dollar')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='contents_cost_type',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='currency',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[('EUR', 'Euro'), ('USD', 'US Dollar')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='non_struct_cost_currency',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[('EUR', 'Euro'), ('USD', 'US Dollar')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='non_struct_cost_type',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='struct_cost_currency',
            field=models.CharField(blank=True, max_length=5, null=True, choices=[('EUR', 'Euro'), ('USD', 'US Dollar')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='struct_cost_type',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area')]),
            preserve_default=True,
        ),
    ]
