# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0014_scenario_hazard_results_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario_hazard_results',
            name='sa_damping',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scenario_hazard_results',
            name='sa_period',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
