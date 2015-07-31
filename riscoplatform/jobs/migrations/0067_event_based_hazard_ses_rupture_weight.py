# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0066_auto_20150727_1112'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_based_hazard_ses_rupture',
            name='weight',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
