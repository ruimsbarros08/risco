# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0008_rupture_model'),
        ('jobs', '0008_auto_20150122_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='depth',
        ),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='dip',
        ),
        #migrations.RemoveField(
        #    model_name='scenario_hazard',
        #    name='fault',
        #),
        #migrations.RemoveField(
        #    model_name='scenario_hazard',
        #    name='fault_model',
        #),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='location',
        ),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='lower_depth',
        ),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='magnitude',
        ),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='rake',
        ),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='rupture_geom',
        ),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='rupture_type',
        ),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='rupture_xml',
        ),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='rupture_xml_string',
        ),
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='upper_depth',
        ),
        migrations.AddField(
            model_name='scenario_hazard',
            name='rupture_model',
            field=models.ForeignKey(to='eng_models.Rupture_Model', null=True),
            preserve_default=True,
        ),
    ]
