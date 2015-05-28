# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0037_auto_20150528_0004'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eng_models', '0056_auto_20150528_0004'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Logic_Tree',
        ),
        migrations.DeleteModel(
            name='Logic_Tree_Level',
        ),
        migrations.AddField(
            model_name='logic_tree_sm_level',
            name='logic_tree',
            field=models.ForeignKey(to='eng_models.Logic_Tree_SM'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_sm_branch_set',
            name='level',
            field=models.ForeignKey(to='eng_models.Logic_Tree_SM_Level'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_sm_branch_set',
            name='origin',
            field=models.ForeignKey(to='eng_models.Logic_Tree_SM_Branch', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_sm_branch_set',
            name='sources',
            field=models.ManyToManyField(to='eng_models.Source', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_sm_branch',
            name='branch_set',
            field=models.ForeignKey(to='eng_models.Logic_Tree_SM_Branch_Set'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_sm_branch',
            name='source_model',
            field=models.ForeignKey(to='eng_models.Source_Model', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_sm',
            name='source_models',
            field=models.ManyToManyField(to='eng_models.Source_Model', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_sm',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_gmpe_level',
            name='logic_tree',
            field=models.ForeignKey(to='eng_models.Logic_Tree_GMPE'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_gmpe_branch',
            name='branch_set',
            field=models.ForeignKey(to='eng_models.Logic_Tree_GMPE_Level'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_gmpe',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
