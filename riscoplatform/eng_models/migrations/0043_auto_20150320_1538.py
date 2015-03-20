# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0042_auto_20150320_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='fragility_model',
            name='limit_states',
            field=djorm_pgarray.fields.ArrayField(dimension=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fragility_function',
            name='limit_state',
            field=models.CharField(max_length=20),
            preserve_default=True,
        ),
    ]
