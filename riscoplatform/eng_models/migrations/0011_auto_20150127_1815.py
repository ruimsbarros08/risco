# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0010_auto_20150125_2305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exposure_model',
            name='xml_string',
        ),
        migrations.RemoveField(
            model_name='fault_model',
            name='xml_string',
        ),
        migrations.RemoveField(
            model_name='rupture_model',
            name='xml_string',
        ),
        migrations.RemoveField(
            model_name='site_model',
            name='xml_string',
        ),
    ]
