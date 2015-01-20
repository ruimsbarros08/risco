# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0004_fault_geom2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fault',
            name='geom',
        ),
    ]
