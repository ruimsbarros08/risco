# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0026_auto_20150205_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='a',
            field=models.FloatField(default=-3.5, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='area',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='b',
            field=models.FloatField(default=-1.0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='bin_width',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='dip',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='fault',
            field=django.contrib.gis.db.models.fields.LineStringField(srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='mag_freq_dist_type',
            field=models.CharField(default='TRUNC', max_length=10, choices=[('TRUNC', 'Truncated Guttenberg Richer'), ('INC', 'Incremental MFD')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='max_mag',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='rake',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='rupt_aspect_ratio',
            field=models.FloatField(default=2.0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='source_type',
            field=models.CharField(default='POINT', max_length=20, choices=[('POINT', 'Point'), ('AREA', 'Area'), ('SIMPLE_FAULT', 'Simple Fault')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='tectonic_region',
            field=models.CharField(default='Active Shallow Crust', max_length=50, choices=[('Active Shallow Crust', 'Active Shallow Crust'), ('Stable Shallow Crust', 'Stable Shallow Crust'), ('Subduction Interface', 'Subduction Interface'), ('Active Interslab', 'Active Interslab'), ('Volcanic', 'Volcanic')]),
            preserve_default=True,
        ),
    ]
