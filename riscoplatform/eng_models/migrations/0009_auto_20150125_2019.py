# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0008_rupture_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='rupture_model',
            name='input_type',
            field=models.CharField(default='CUSTOM_RUPTURE', max_length=50, choices=[('CUSTOM_RUPTURE', 'custom rupture'), ('UPLOAD_XML', 'upload xml')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='rupture_model',
            name='rupture_type',
            field=models.CharField(default='FAULT', max_length=50, choices=[('POINT', 'Point'), ('FAULT', 'Fault')]),
            preserve_default=True,
        ),
    ]
