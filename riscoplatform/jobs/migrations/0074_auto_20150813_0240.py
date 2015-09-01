# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0073_auto_20150812_1731'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loss',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='loss',
            name='job_vulnerability',
        ),
        migrations.DeleteModel(
            name='Loss',
        ),
        migrations.RemoveField(
            model_name='risk',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='risk',
            name='job_vulnerability',
        ),
        migrations.DeleteModel(
            name='Risk',
        ),
        migrations.DeleteModel(
            name='Ses_to_Risk',
        ),
        migrations.AddField(
            model_name='event_based_hazard_ses_rupture',
            name='weight',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
