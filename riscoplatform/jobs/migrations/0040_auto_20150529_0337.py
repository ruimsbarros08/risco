# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0039_auto_20150528_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classical_psha_hazard_curves',
            name='gsim_lt_path',
            field=djorm_pgarray.fields.TextArrayField(dbtype='text'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='classical_psha_hazard_curves',
            name='sm_lt_path',
            field=djorm_pgarray.fields.TextArrayField(dbtype='text'),
            preserve_default=True,
        ),
    ]
