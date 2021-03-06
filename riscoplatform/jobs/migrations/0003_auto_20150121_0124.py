# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0002_auto_20150120_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scenario_hazard',
            name='vs30type',
            field=models.CharField(default=b'MEASURED', max_length=10, blank=True, choices=[(b'MEASURED', b'measured'), (b'INFERRED', b'inferred')]),
            preserve_default=True,
        ),
    ]
