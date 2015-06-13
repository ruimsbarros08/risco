# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0061_auto_20150528_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='a',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='b',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
