# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0021_auto_20150203_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenario_damage',
            name='error',
        ),
        migrations.RemoveField(
            model_name='scenario_damage',
            name='ready',
        ),
        migrations.RemoveField(
            model_name='scenario_damage',
            name='start',
        ),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='error',
        ),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='ready',
        ),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='start',
        ),
        migrations.AddField(
            model_name='scenario_damage',
            name='status',
            field=models.CharField(default=b'CREATED', max_length=50, choices=[(b'CREATED', b'Created'), (b'STARTED', b'Started'), (b'ERROR', b'Error'), (b'FINISHED', b'Finished')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scenario_hazard',
            name='status',
            field=models.CharField(default=b'CREATED', max_length=50, choices=[(b'CREATED', b'Created'), (b'STARTED', b'Started'), (b'ERROR', b'Error'), (b'FINISHED', b'Finished')]),
            preserve_default=True,
        ),
    ]
