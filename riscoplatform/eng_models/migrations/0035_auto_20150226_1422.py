# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0034_auto_20150225_0328'),
    ]

    operations = [
        migrations.AddField(
            model_name='logic_tree',
            name='source_models',
            field=models.ManyToManyField(to='eng_models.Source_Model', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree',
            name='type',
            field=models.CharField(max_length=25, null=True),
            preserve_default=True,
        ),
    ]
