# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0066_auto_20150622_2220'),
        ('jobs', '0069_auto_20150803_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='exposure_model',
            field=models.ForeignKey(to='eng_models.Exposure_Model', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='locations',
            field=django.contrib.gis.db.models.fields.MultiPointField(srid=4326, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='classical_psha_hazard',
            name='grid_spacing',
            field=models.FloatField(default=1, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='classical_psha_hazard',
            name='region',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True),
            preserve_default=True,
        ),
    ]
