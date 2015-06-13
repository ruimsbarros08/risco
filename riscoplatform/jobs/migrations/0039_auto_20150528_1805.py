# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0038_auto_20150528_0023'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classical_psha_hazard',
            old_name='gmpe_logic_trees',
            new_name='gmpe_logic_tree',
        ),
    ]
