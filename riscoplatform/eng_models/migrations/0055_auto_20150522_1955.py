# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0054_auto_20150522_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source',
            name='hypo_depth_dist',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='nodal_plane_dist',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
    ]
