# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0029_auto_20150223_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='logic_tree',
            name='xml',
            field=models.FileField(null=True, upload_to='uploads/logic_tree/', blank=True),
            preserve_default=True,
        ),
    ]
