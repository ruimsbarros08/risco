# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0008_auto_20150609_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='adm_2',
            name='adm_1_name',
            field=models.CharField(max_length=75, null=True),
            preserve_default=True,
        ),
    ]
