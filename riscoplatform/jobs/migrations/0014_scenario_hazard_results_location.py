# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0013_scenario_hazard_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario_hazard_results',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default='POINT(-8 40)', srid=4326),
            preserve_default=False,
        ),
    ]
