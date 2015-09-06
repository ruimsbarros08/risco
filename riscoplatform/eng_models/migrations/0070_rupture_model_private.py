# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0069_auto_20150904_2354'),
    ]

    operations = [
        migrations.AddField(
            model_name='rupture_model',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
