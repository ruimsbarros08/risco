# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0014_exposure_model_taxonomy_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exposure_model',
            name='taxonomy_source',
            field=models.ForeignKey(blank=True, to='eng_models.Building_Taxonomy_Source', null=True),
            preserve_default=True,
        ),
    ]
