# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0003_auto_20150413_1800'),
        ('jobs', '0029_auto_20150422_1558'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario_Hazard_Results_By_Cell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imt', models.CharField(max_length=3)),
                ('sa_period', models.FloatField(null=True)),
                ('gmvs_mean', models.FloatField()),
                ('cell', models.ForeignKey(to='world.Fishnet')),
                ('job', models.ForeignKey(to='jobs.Scenario_Hazard')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
