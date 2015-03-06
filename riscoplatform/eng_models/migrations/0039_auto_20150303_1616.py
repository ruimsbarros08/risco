# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0038_auto_20150227_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fragility_model',
            name='taxonomy_source',
            field=models.ForeignKey(blank=True, to='eng_models.Building_Taxonomy_Source', null=True),
            preserve_default=True,
        ),
    ]
