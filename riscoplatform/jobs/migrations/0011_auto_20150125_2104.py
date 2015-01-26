# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0010_auto_20150125_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario_hazard',
            name='region',
            field=django.contrib.gis.db.models.fields.PolygonField(default='', srid=4326),
            preserve_default=False,
        ),
    ]
