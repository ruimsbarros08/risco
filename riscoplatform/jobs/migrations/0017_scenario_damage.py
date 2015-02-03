# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eng_models', '0018_auto_20150131_1454'),
        ('jobs', '0016_auto_20150128_1600'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario_Damage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name=b'date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True)),
                ('ini_file', models.FileField(null=True, upload_to=b'uploads/scenario/damage/', blank=True)),
                ('exposure_model', models.ForeignKey(to='eng_models.Exposure_Model')),
                ('fragility_model', models.ForeignKey(to='eng_models.Fragility_Model')),
                ('hazard_job', models.ForeignKey(to='jobs.Scenario_Hazard')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
