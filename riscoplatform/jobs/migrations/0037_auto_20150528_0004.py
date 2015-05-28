# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0056_auto_20150528_0004'),
        ('jobs', '0036_auto_20150526_1808'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classical_psha_hazard',
            name='logic_trees',
        ),
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='gmpe_logic_trees',
            field=models.ForeignKey(null=True, to='eng_models.Logic_Tree_GMPE'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='sm_logic_tree',
            field=models.ForeignKey(null=True, to='eng_models.Logic_Tree_SM'),
            preserve_default=False,
        ),
    ]
