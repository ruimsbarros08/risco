# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0015_auto_20150128_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario_hazard_results',
            name='cell',
            field=models.ForeignKey(to='world.Fishnet', null=True),
            preserve_default=True,
        ),
    ]
