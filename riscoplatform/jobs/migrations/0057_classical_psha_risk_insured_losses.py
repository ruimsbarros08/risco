# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0056_classical_psha_risk_loss_curves_insured'),
    ]

    operations = [
        migrations.AddField(
            model_name='classical_psha_risk',
            name='insured_losses',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
