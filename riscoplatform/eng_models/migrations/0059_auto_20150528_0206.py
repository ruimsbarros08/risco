# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0058_auto_20150528_0041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logic_tree_sm_branch_set',
            name='origin',
        ),
        migrations.AddField(
            model_name='logic_tree_sm_branch_set',
            name='filter',
            field=models.CharField(max_length=20, null=True, choices=[('branch', 'Branch'), ('source', 'Source')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_sm_branch_set',
            name='origins',
            field=models.ManyToManyField(to='eng_models.Logic_Tree_SM_Branch', null=True),
            preserve_default=True,
        ),
    ]
