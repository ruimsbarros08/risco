# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0068_event_based_hazard_ses_rupture_rupture_oq'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classical_psha_risk_loss_curves',
            name='insured',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='classical_psha_risk_loss_maps',
            name='insured',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
