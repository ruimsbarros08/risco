# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0007_auto_20150609_1436'),
    ]

    operations = [
        migrations.AddField(
            model_name='adm_1',
            name='country_iso',
            field=models.CharField(max_length=3, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='adm_1',
            name='country_name',
            field=models.CharField(max_length=75, null=True),
            preserve_default=True,
        ),
    ]
