# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scenario_hazard',
            old_name='repture_type',
            new_name='rupture_type',
        ),
    ]
