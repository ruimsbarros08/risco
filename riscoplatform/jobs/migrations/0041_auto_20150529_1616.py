# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0040_auto_20150529_0337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classical_psha_hazard_curves',
            name='weight',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
    ]
