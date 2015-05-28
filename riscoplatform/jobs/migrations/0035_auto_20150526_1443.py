# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0034_classical_psha_hazard_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='classical_psha_hazard_results',
            name='imls',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='classical_psha_hazard_results',
            name='poes',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
    ]
