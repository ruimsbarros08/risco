# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0017_scenario_damage'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario_damage',
            name='max_hazard_dist',
            field=models.FloatField(default=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scenario_damage',
            name='region',
            field=django.contrib.gis.db.models.fields.PolygonField(default='POLYGON((-11.3818359375 42.6985858916984,-4.5263671875 42.5368920078732,-5.80078125 36.1201275897815,-10.1953125 36.1556178338186,-11.3818359375 42.6985858916984))', srid=4326),
            preserve_default=False,
        ),
    ]
