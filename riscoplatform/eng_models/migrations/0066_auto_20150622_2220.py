# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0065_auto_20150617_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exposure_model',
            name='aggregation',
        ),
        migrations.RemoveField(
            model_name='exposure_model',
            name='currency',
        ),
    ]
