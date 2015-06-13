# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0010_adm_2_country_iso'),
    ]

    operations = [
        migrations.AddField(
            model_name='adm_2',
            name='repeated',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
    ]
