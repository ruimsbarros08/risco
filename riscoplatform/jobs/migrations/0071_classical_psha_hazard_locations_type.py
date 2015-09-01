# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0070_auto_20150805_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='locations_type',
            field=models.CharField(default=b'EXPOSURE', max_length=20, choices=[(b'EXPOSURE', b'Exposure model'), (b'GRID', b'Grid'), (b'LOCATIONS', b'Locations')]),
            preserve_default=True,
        ),
    ]
