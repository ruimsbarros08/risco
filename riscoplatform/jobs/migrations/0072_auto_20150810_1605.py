# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0071_classical_psha_hazard_locations_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='classical_psha_risk_vulnerability',
            name='at_loss_rates',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk_vulnerability',
            name='it_loss_values',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk_vulnerability',
            name='periods',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='classical_psha_hazard',
            name='exposure_model',
            field=models.ForeignKey(blank=True, to='eng_models.Exposure_Model', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='classical_psha_hazard',
            name='grid_spacing',
            field=models.FloatField(default=1, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='classical_psha_hazard',
            name='locations',
            field=django.contrib.gis.db.models.fields.MultiPointField(srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='classical_psha_hazard',
            name='region',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='classical_psha_risk',
            name='lrem_steps_per_interval',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
