# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0063_auto_20150706_1312'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event_Based_Hazard_SES_Rupture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rake', models.FloatField()),
                ('magnitude', models.FloatField()),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('depth', models.FloatField()),
                ('ses_id', models.IntegerField()),
                ('rupture_id', models.IntegerField()),
                ('job', models.ForeignKey(to='jobs.Event_Based_Hazard')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
