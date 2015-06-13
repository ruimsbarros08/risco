# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0062_auto_20150603_1911'),
        ('jobs', '0041_auto_20150529_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='classical_psha_risk',
            name='exposure_model',
            field=models.ForeignKey(default=1, to='eng_models.Exposure_Model'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='classical_psha_risk',
            name='ini_file',
            field=models.FileField(null=True, upload_to=b'uploads/psha/risk/', blank=True),
            preserve_default=True,
        ),
    ]
