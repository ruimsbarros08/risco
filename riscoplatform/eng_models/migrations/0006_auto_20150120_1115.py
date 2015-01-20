# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0005_remove_fault_geom'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fault',
            old_name='geom2',
            new_name='geom',
        ),
    ]
