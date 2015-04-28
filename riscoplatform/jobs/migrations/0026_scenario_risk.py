# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0048_vulnerability_model_xml'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0025_auto_20150406_2211'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario_Risk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name=b'date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True)),
                ('region', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('max_hazard_dist', models.FloatField()),
                ('master_seed', models.IntegerField()),
                ('vul_correlation_coefficient', models.FloatField()),
                ('insured_losses', models.BooleanField()),
                ('time_of_the_day', models.CharField(max_length=10, choices=[(b'day', b'Day'), (b'night', b'Night'), (b'transit', b'Transit')])),
                ('status', models.CharField(default=b'CREATED', max_length=50, choices=[(b'CREATED', b'Created'), (b'STARTED', b'Started'), (b'ERROR', b'Error'), (b'FINISHED', b'Finished')])),
                ('oq_id', models.IntegerField(null=True)),
                ('ini_file', models.FileField(null=True, upload_to=b'uploads/scenario/damage/', blank=True)),
                ('exposure_model', models.ForeignKey(to='eng_models.Exposure_Model')),
                ('hazard_job', models.ForeignKey(to='jobs.Scenario_Hazard')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('vulnerability_models', models.ManyToManyField(to='eng_models.Vulnerability_Model')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
