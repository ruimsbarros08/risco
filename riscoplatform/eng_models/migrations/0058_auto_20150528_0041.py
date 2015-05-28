# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0057_auto_20150528_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='logic_tree_gmpe_branch',
            name='xml_id',
            field=models.CharField(max_length=10, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_gmpe_level',
            name='xml_id',
            field=models.CharField(max_length=10, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_sm_branch',
            name='xml_id',
            field=models.CharField(max_length=10, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_sm_branch_set',
            name='xml_id',
            field=models.CharField(max_length=10, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_sm_level',
            name='xml_id',
            field=models.CharField(max_length=10, null=True),
            preserve_default=True,
        ),
    ]
