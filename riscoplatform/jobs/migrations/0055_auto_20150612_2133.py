# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0054_auto_20150612_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classical_psha_risk_loss_maps',
            name='insured',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
    ]
