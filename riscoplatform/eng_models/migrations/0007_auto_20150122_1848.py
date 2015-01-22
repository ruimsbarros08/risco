# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0006_auto_20150120_1115'),
    ]

    operations = [
        migrations.AddField(
            model_name='exposure_model',
            name='xml_string',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fault_model',
            name='xml_string',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='site_model',
            name='xml_string',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
