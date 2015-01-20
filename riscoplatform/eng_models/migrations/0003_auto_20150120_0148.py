# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0002_auto_20150120_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fault',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326),
            preserve_default=True,
        ),
    ]
