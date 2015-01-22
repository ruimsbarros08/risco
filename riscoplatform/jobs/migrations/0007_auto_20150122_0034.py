# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0006_remove_scenario_hazard_region'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scenario_hazard',
            old_name='region2',
            new_name='region',
        ),
    ]
