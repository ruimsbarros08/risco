# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0077_auto_20150813_1858'),
    ]

    operations = [
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scenario_damage',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scenario_hazard',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scenario_risk',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
