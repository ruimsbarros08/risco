# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0063_asset_adm_2'),
        ('jobs', '0049_auto_20150611_1747'),
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
                ('average_loss_ratio', models.FloatField()),
                ('stddev_loss_ratio', models.FloatField(null=True)),
                ('asset_value', models.FloatField()),
                ('asset', models.ForeignKey(to='eng_models.Asset')),
                ('vulnerability_model', models.ForeignKey(to='jobs.Classical_PSHA_Risk_Vulnerability')),
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
        migrations.RemoveField(
            model_name='classical_psha_risk_loss_results',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='classical_psha_risk_loss_results',
            name='vulnerability_model',
        ),
        migrations.DeleteModel(
            name='Classical_PSHA_Risk_Loss_Results',
        ),
    ]
