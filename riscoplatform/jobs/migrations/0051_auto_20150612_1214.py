# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0063_asset_adm_2'),
        ('jobs', '0050_auto_20150611_1808'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classical_psha_risk_loss_maps',
            name='location',
        ),
        migrations.AddField(
            model_name='classical_psha_risk_loss_maps',
            name='asset',
            field=models.ForeignKey(default=1, to='eng_models.Asset'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classical_psha_risk_loss_maps',
            name='quantile',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk_loss_maps',
            name='statistics',
            field=models.CharField(max_length=20, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk_loss_maps',
            name='vulnerability_model',
            field=models.ForeignKey(default=1, to='jobs.Classical_PSHA_Risk_Vulnerability'),
            preserve_default=False,
        ),
    ]
