# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0053_auto_20150429_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='hypo_depth_dist',
            field=djorm_pgarray.fields.ArrayField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='nodal_plane_dist',
            field=djorm_pgarray.fields.ArrayField(),
            preserve_default=True,
        ),
    ]
