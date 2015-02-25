# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0033_auto_20150225_0055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logic_tree_branch_set',
            name='uncertainty_type',
            field=models.CharField(max_length=25, null=True, choices=[('gmpeModel', 'GMPE Model'), ('sourceModel', 'Source Model'), ('maxMagGRRelative', 'Max Mag GR Relative'), ('bGRRelative', 'b GR Relative'), ('abGRAbsolute', 'a/b GR Absolute'), ('maxMagGRAbsolute', 'max Mag GR Absolute')]),
            preserve_default=True,
        ),
    ]
