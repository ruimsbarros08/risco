# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_auto_20150121_0125'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario_hazard',
            name='region2',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scenario_hazard',
            name='rupture_type',
            field=models.CharField(default=b'CLOSEST_FAULT', max_length=50, choices=[(b'CLOSEST_FAULT', b'closest fault'), (b'CUSTOM_RUPTURE', b'custom rupture'), (b'UPLOAD_XML', b'upload xml')]),
            preserve_default=True,
        ),
    ]
