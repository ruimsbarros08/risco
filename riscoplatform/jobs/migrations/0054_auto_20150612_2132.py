# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0053_auto_20150612_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classical_psha_risk_loss_maps',
            name='stddev',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
