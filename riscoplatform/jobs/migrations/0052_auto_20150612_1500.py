# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0051_auto_20150612_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classical_psha_risk_loss_maps',
            name='insured_mean',
        ),
        migrations.RemoveField(
            model_name='classical_psha_risk_loss_maps',
            name='insured_stddev',
        ),
        migrations.AddField(
            model_name='classical_psha_risk_loss_maps',
            name='insured',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
