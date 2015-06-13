# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0055_auto_20150612_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='classical_psha_risk_loss_curves',
            name='insured',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
    ]
