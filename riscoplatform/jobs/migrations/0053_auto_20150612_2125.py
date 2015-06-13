# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0052_auto_20150612_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classical_psha_risk_loss_curves',
            name='hazard_output_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='classical_psha_risk_loss_maps',
            name='hazard_output_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
