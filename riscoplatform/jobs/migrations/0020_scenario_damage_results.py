# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0023_exposure_model_oq_id'),
        ('jobs', '0019_auto_20150201_1801'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario_Damage_Results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('limit_state', models.CharField(max_length=20)),
                ('mean', models.FloatField()),
                ('stddev', models.FloatField()),
                ('asset', models.ForeignKey(to='eng_models.Asset')),
                ('job', models.ForeignKey(to='jobs.Scenario_Damage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
