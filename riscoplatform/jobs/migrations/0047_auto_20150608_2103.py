# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0062_auto_20150603_1911'),
        ('jobs', '0046_remove_classical_psha_risk_vulnerability_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classical_PSHA_Risk_Loss_Curves',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hazard_output_id', models.IntegerField()),
                ('statistics', models.CharField(max_length=20, null=True)),
                ('quantile', models.FloatField(null=True)),
                ('loss_ratios', djorm_pgarray.fields.FloatArrayField(dbtype='double precision')),
                ('poes', djorm_pgarray.fields.FloatArrayField(dbtype='double precision')),
                ('average_loss_ratio', djorm_pgarray.fields.FloatArrayField(dbtype='double precision')),
                ('stddev_loss_ratio', djorm_pgarray.fields.FloatArrayField(dbtype='double precision')),
                ('asset', models.ForeignKey(to='eng_models.Asset')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Classical_PSHA_Risk_Loss_Maps',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hazard_output_id', models.IntegerField()),
                ('poe', models.FloatField()),
                ('mean', models.FloatField()),
                ('stddev', models.FloatField()),
                ('insured_mean', models.FloatField(null=True)),
                ('insured_stddev', models.FloatField(null=True)),
                ('location', models.ForeignKey(to='jobs.Classical_PSHA_Risk_Loss_Curves')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Classical_PSHA_Risk_Vulnerability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job', models.ForeignKey(to='jobs.Classical_PSHA_Risk')),
                ('vulnerability_model', models.ForeignKey(to='eng_models.Vulnerability_Model')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='classical_psha_risk_loss_curves',
            name='vulnerability_model',
            field=models.ForeignKey(to='jobs.Classical_PSHA_Risk_Vulnerability'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk',
            name='vulnerability_models',
            field=models.ManyToManyField(to='eng_models.Vulnerability_Model', through='jobs.Classical_PSHA_Risk_Vulnerability'),
            preserve_default=True,
        ),
    ]
