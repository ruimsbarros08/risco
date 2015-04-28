# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0049_vulnerability_model_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vulnerability_model',
            name='sa_period',
            field=models.FloatField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
