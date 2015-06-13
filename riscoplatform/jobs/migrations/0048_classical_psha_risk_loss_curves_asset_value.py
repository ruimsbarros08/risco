# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0047_auto_20150608_2103'),
    ]

    operations = [
        migrations.AddField(
            model_name='classical_psha_risk_loss_curves',
            name='asset_value',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
