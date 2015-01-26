# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0009_auto_20150125_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario_hazard',
            name='rupture_model',
            field=models.ForeignKey(default=1, to='eng_models.Rupture_Model'),
            preserve_default=False,
        ),
    ]
