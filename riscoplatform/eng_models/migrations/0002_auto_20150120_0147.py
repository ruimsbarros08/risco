# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fault',
            name='geom',
            field=django.contrib.gis.db.models.fields.LineStringField(srid=4326),
            preserve_default=True,
        ),
    ]
