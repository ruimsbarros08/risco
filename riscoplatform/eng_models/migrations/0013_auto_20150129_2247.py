# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0012_auto_20150129_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building_taxonomy',
            name='name',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
    ]
