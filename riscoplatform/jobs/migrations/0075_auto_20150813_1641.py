# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0074_auto_20150813_0240'),
    ]

    operations = [
        migrations.AddField(
            model_name='classical_psha_risk_vulnerability',
            name='at_loss_rates_ooc',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk_vulnerability',
            name='it_loss_values_ooc',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk_vulnerability',
            name='periods_ooc',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
    ]
