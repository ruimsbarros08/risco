# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0043_auto_20150320_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fragility_model',
            name='limit_states',
            field=djorm_pgarray.fields.TextArrayField(dbtype='text'),
            preserve_default=True,
        ),
    ]
