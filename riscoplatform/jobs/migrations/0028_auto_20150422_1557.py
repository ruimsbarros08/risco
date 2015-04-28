# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0050_auto_20150413_1800'),
        ('jobs', '0027_auto_20150413_1800'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario_Risk_Results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mean', models.FloatField()),
                ('stddev', models.FloatField()),
                ('asset', models.ForeignKey(to='eng_models.Asset')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Scenario_Risk_Vulnerability_Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job', models.ForeignKey(to='jobs.Scenario_Risk')),
                ('vulnerability_model', models.ForeignKey(to='eng_models.Vulnerability_Model')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='scenario_risk_results',
            name='job_vul',
            field=models.ForeignKey(to='jobs.Scenario_Risk_Vulnerability_Model'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='scenario_risk',
            name='vulnerability_models',
        ),
        migrations.AddField(
            model_name='scenario_risk',
            name='vulnerability',
            field=models.ManyToManyField(to='eng_models.Vulnerability_Model', through='jobs.Scenario_Risk_Vulnerability_Model'),
            preserve_default=True,
        ),
    ]
