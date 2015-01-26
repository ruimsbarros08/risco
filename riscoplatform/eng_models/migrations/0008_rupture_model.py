# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eng_models', '0007_auto_20150122_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rupture_Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True)),
                ('rupture_type', models.CharField(default='CUSTOM_RUPTURE', max_length=50, choices=[('CUSTOM_RUPTURE', 'custom rupture'), ('UPLOAD_XML', 'upload xml')])),
                ('magnitude', models.FloatField(null=True, blank=True)),
                ('depth', models.FloatField(null=True, blank=True)),
                ('rake', models.FloatField(null=True, blank=True)),
                ('upper_depth', models.FloatField(null=True, blank=True)),
                ('lower_depth', models.FloatField(null=True, blank=True)),
                ('dip', models.FloatField(null=True, blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('rupture_geom', django.contrib.gis.db.models.fields.LineStringField(srid=4326, null=True, blank=True)),
                ('xml', models.FileField(null=True, upload_to='uploads/rupture/', blank=True)),
                ('xml_string', models.TextField(null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
