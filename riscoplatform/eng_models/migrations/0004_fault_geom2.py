# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0003_auto_20150120_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='fault',
            name='geom2',
            field=django.contrib.gis.db.models.fields.LineStringField(srid=4326, null=True),
            preserve_default=True,
        ),
    ]
