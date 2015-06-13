# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0009_adm_2_adm_1_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='adm_2',
            name='country_iso',
            field=models.CharField(max_length=3, null=True),
            preserve_default=True,
        ),
    ]
