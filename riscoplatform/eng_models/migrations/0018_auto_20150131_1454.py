# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0017_auto_20150131_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='building_taxonomy',
            name='name',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
    ]
