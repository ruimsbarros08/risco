# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0015_auto_20150130_1643'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fragility_function',
            old_name='function',
            new_name='cdf',
        ),
        migrations.AddField(
            model_name='fragility_function',
            name='pdf',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision', dimension=2),
            preserve_default=True,
        ),
    ]
