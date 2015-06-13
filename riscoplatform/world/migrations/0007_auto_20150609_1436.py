# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0006_adm_1_new'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adm_1',
            name='new',
            field=models.NullBooleanField(default=True),
            preserve_default=True,
        ),
    ]
