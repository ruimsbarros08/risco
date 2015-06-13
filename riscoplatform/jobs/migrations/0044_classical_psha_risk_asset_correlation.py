# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0043_auto_20150604_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='classical_psha_risk',
            name='asset_correlation',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
