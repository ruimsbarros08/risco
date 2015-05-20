# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0031_auto_20150512_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classical_psha_hazard',
            name='pga',
        ),
        migrations.RemoveField(
            model_name='classical_psha_hazard',
            name='sa_periods',
        ),
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='poes',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='quantile_hazard_curves',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
    ]
