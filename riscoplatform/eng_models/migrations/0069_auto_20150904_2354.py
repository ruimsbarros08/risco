# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0068_auto_20150904_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='building_taxonomy_source',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='consequence_model',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exposure_model',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fragility_model',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_gmpe',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_sm',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='site_model',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source_model',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vulnerability_model',
            name='private',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
