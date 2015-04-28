# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import djorm_pgarray.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0023_classical_psha_hazard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classical_psha_hazard',
            name='exposure_model',
        ),
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='grid_spacing',
            field=models.FloatField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='imt_l',
            field=jsonfield.fields.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='pga',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='random_seed',
            field=models.IntegerField(default=3),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='region',
            field=django.contrib.gis.db.models.fields.PolygonField(default='POLYGON((-21.423339843749996 43.24520272203356,-14.655761718749998 43.34116005412307,-15.57861328125 38.35888785866677,-23.04931640625 38.324420427006515,-21.423339843749996 43.24520272203356))', srid=4326),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='sa_periods',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
    ]
