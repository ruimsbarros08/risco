# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0003_auto_20150413_1800'),
        ('eng_models', '0052_auto_20150423_1733'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='adm_1',
            field=models.ForeignKey(to='world.Adm_1', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='aggregation',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area'), ('per_asset', 'Per asset')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='business_int_cost_type',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area'), ('per_asset', 'Per asset')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='contents_cost_type',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area'), ('per_asset', 'Per asset')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='non_struct_cost_type',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area'), ('per_asset', 'Per asset')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='struct_cost_type',
            field=models.CharField(blank=True, max_length=20, null=True, choices=[('aggregated', 'Aggregated'), ('per_unit', 'Per unit'), ('per_area', 'Per area'), ('per_asset', 'Per asset')]),
            preserve_default=True,
        ),
    ]
