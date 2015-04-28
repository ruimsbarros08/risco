# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0026_scenario_risk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classical_psha_hazard',
            name='vs30type',
            field=models.CharField(default=b'measured', max_length=10, null=True, blank=True, choices=[(b'measured', b'measured'), (b'inferred', b'inferred')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scenario_hazard',
            name='vs30type',
            field=models.CharField(default=b'measured', max_length=10, null=True, blank=True, choices=[(b'measured', b'measured'), (b'inferred', b'inferred')]),
            preserve_default=True,
        ),
    ]
