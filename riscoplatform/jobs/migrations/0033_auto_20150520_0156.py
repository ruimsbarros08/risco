# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0032_auto_20150520_0147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario_risk',
            name='insured_losses',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
