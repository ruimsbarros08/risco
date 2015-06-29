# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0064_auto_20150612_2125'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='asset',
            name='adm_1',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='parish',
        ),
    ]
