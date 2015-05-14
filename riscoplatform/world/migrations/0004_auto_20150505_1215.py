# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0003_auto_20150413_1800'),
    ]

    operations = [
        migrations.AddField(
            model_name='adm_1',
            name='geom_simp',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='adm_2',
            name='geom_simp',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='country',
            name='geom_simp',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326, null=True),
            preserve_default=True,
        ),
    ]
