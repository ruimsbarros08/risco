# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0048_vulnerability_model_xml'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0024_auto_20150402_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classical_PSHA_Risk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name=b'date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True)),
                ('random_seed', models.IntegerField(default=3)),
                ('asset_hazard_distance', models.FloatField()),
                ('lrem_steps_per_interval', models.FloatField()),
                ('region', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('ini_file', models.FileField(null=True, upload_to=b'uploads/psha/hazard/', blank=True)),
                ('status', models.CharField(default=b'CREATED', max_length=50, choices=[(b'CREATED', b'Created'), (b'STARTED', b'Started'), (b'ERROR', b'Error'), (b'FINISHED', b'Finished')])),
                ('oq_id', models.IntegerField(null=True)),
                ('hazard', models.ForeignKey(to='jobs.Classical_PSHA_Hazard')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('vulnerability_models', models.ManyToManyField(to='eng_models.Vulnerability_Model')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='classical_psha_hazard',
            name='vulnerability_models',
        ),
    ]
