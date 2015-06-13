# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0005_country_simp'),
    ]

    operations = [
        migrations.AddField(
            model_name='adm_1',
            name='new',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
    ]
