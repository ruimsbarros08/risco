# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0001_initial'),
        ('jobs', '0012_auto_20150127_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario_Hazard_Results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('imt', models.CharField(max_length=3)),
                ('sa_period', models.FloatField()),
                ('sa_damping', models.IntegerField()),
                ('gmvs', models.FloatField()),
                ('cell', models.ForeignKey(to='world.Fishnet')),
                ('job', models.ForeignKey(to='jobs.Scenario_Hazard')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
