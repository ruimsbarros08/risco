# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0030_logic_tree_xml'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logic_tree_branch',
            name='source',
        ),
        migrations.AddField(
            model_name='logic_tree_branch',
            name='sources',
            field=models.ManyToManyField(to='eng_models.Source'),
            preserve_default=True,
        ),
    ]
