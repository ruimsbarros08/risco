# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0037_auto_20150528_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classical_psha_hazard',
            name='gmpe_logic_trees',
            field=models.ForeignKey(default=1, to='eng_models.Logic_Tree_GMPE'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='classical_psha_hazard',
            name='sm_logic_tree',
            field=models.ForeignKey(default=1, to='eng_models.Logic_Tree_SM'),
            preserve_default=False,
        ),
    ]
