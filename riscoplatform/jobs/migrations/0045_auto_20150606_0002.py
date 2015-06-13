# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0044_classical_psha_risk_asset_correlation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classical_psha_risk',
            name='lrem_steps_per_interval',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
