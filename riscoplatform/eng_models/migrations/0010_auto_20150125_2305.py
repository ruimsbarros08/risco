# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0009_auto_20150125_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rupture_model',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default='POINT(-10 40)', srid=4326),
            preserve_default=False,
        ),
    ]
