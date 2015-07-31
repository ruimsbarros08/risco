# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0067_event_based_hazard_ses_rupture_weight'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_based_hazard_ses_rupture',
            name='rupture_oq',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
