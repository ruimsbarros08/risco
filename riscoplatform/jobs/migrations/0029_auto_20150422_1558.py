# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0028_auto_20150422_1557'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scenario_risk',
            old_name='vulnerability',
            new_name='vulnerability_models',
        ),
    ]
