# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0059_auto_20150528_0206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='logic_tree_gmpe_branch',
            old_name='branch_set',
            new_name='level',
        ),
    ]
