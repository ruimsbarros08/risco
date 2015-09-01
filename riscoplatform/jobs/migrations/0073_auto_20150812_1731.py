# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0066_auto_20150622_2220'),
        ('jobs', '0072_auto_20150810_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='Loss',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ses_id', models.IntegerField()),
                ('loss_total', models.FloatField()),
                ('hazard_output_id', models.IntegerField()),
                ('weight', models.FloatField()),
                ('asset', models.ForeignKey(to='eng_models.Asset')),
                ('job_vulnerability', models.ForeignKey(to='jobs.Classical_PSHA_Risk_Vulnerability')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Risk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rupture_id', models.IntegerField()),
                ('loss', models.FloatField()),
                ('hazard_output_id', models.IntegerField()),
                ('asset', models.ForeignKey(to='eng_models.Asset')),
                ('job_vulnerability', models.ForeignKey(to='jobs.Classical_PSHA_Risk_Vulnerability')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ses_to_Risk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ses_collection_id', models.IntegerField()),
                ('ses_output_id', models.IntegerField()),
                ('gmf_id', models.IntegerField()),
                ('hzrdr_job_id', models.IntegerField()),
                ('riskr_job_id', models.IntegerField()),
                ('weight', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='event_loss_table',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='event_loss_table',
            name='job_vulnerability',
        ),
        migrations.RemoveField(
            model_name='event_loss_table',
            name='rupture',
        ),
        migrations.DeleteModel(
            name='Event_Loss_Table',
        ),
        migrations.RemoveField(
            model_name='event_based_hazard_ses_rupture',
            name='rupture_oq',
        ),
        migrations.RemoveField(
            model_name='event_based_hazard_ses_rupture',
            name='weight',
        ),
    ]
