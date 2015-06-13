# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0011_adm_2_repeated'),
        ('eng_models', '0062_auto_20150603_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='adm_2',
            field=models.ForeignKey(to='world.Adm_2', null=True),
            preserve_default=True,
        ),
    ]
