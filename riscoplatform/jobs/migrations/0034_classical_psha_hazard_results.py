# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0005_country_simp'),
        ('jobs', '0033_auto_20150520_0156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classical_PSHA_Hazard_Results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('imt', models.CharField(max_length=3)),
                ('sa_period', models.FloatField(null=True)),
                ('sa_damping', models.IntegerField(null=True)),
                ('weight', models.FloatField()),
                ('statistics', models.CharField(max_length=20, null=True)),
                ('quantile', models.FloatField(null=True)),
                ('sm_lt_path', djorm_pgarray.fields.ArrayField()),
                ('gsim_lt_path', djorm_pgarray.fields.ArrayField()),
                ('poes', djorm_pgarray.fields.ArrayField()),
                ('cell', models.ForeignKey(to='world.Fishnet', null=True)),
                ('job', models.ForeignKey(to='jobs.Classical_PSHA_Hazard')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
