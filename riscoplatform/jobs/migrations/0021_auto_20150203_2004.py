# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0020_scenario_damage_results'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='sa1_period',
        ),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='sa2_period',
        ),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='sa3_period',
        ),
        migrations.AddField(
            model_name='scenario_hazard',
            name='sa_periods',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
    ]
