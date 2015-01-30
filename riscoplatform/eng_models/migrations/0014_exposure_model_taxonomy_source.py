# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0013_auto_20150129_2247'),
    ]

    operations = [
        migrations.AddField(
            model_name='exposure_model',
            name='taxonomy_source',
            field=models.ForeignKey(default=1, to='eng_models.Building_Taxonomy_Source'),
            preserve_default=False,
        ),
    ]
