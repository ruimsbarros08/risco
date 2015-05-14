# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0030_scenario_hazard_results_by_cell'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario_risk_results',
            name='insured_mean',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scenario_risk_results',
            name='insured_stddev',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
