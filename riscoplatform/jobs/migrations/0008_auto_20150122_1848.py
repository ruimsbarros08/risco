# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0007_auto_20150122_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='scenario_hazard',
            name='ini_file_string',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scenario_hazard',
            name='rupture_xml_string',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
