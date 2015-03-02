# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0037_auto_20150226_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logic_tree',
            name='source_models',
            field=models.ManyToManyField(to='eng_models.Source_Model', null=True, blank=True),
            preserve_default=True,
        ),
    ]
