# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0022_auto_20150202_1532'),
    ]

    operations = [
        migrations.AddField(
            model_name='exposure_model',
            name='oq_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
