# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0031_auto_20150224_1830'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logic_tree_branch',
            name='sources',
        ),
        migrations.AddField(
            model_name='logic_tree_branch_set',
            name='sources',
            field=models.ManyToManyField(to='eng_models.Source', null=True),
            preserve_default=True,
        ),
    ]
