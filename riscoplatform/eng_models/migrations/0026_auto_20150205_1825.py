# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields
import django.contrib.gis.db.models.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eng_models', '0025_auto_20150203_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('tectonic_region', models.CharField(max_length=50, choices=[('Active Shallow Crust', 'Active Shallow Crust'), ('Stable Shallow Crust', 'Stable Shallow Crust'), ('Subduction Interface', 'Subduction Interface'), ('Active Interslab', 'Active Interslab'), ('Volcanic', 'Volcanic')])),
                ('mag_scale_rel', models.CharField(default='WC1994', max_length=50, choices=[('WC1994', 'Wells and Coopersmith 1994'), ('WC1994', 'Thomas et al. 2012 (PEER)')])),
                ('rupt_aspect_ratio', models.FloatField()),
                ('mag_freq_dist_type', models.CharField(max_length=10, choices=[('WC1994', 'Wells and Coopersmith 1994'), ('WC1994', 'Thomas et al. 2012 (PEER)')])),
                ('a', models.FloatField(null=True)),
                ('b', models.FloatField(null=True)),
                ('min_mag', models.FloatField(null=True)),
                ('max_mag', models.FloatField(null=True)),
                ('bin_width', models.FloatField(null=True)),
                ('occur_rates', djorm_pgarray.fields.FloatArrayField(dbtype='double precision')),
                ('source_type', models.CharField(max_length=20, choices=[('POINT', 'Point'), ('AREA', 'Area'), ('SIMPLE_FAULT', 'Simple Fault')])),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True)),
                ('upper_depth', models.FloatField(null=True)),
                ('lower_depth', models.FloatField(null=True)),
                ('nodal_plane_dist', djorm_pgarray.fields.FloatArrayField(dbtype='double precision', dimension=4)),
                ('hypo_depth_dist', djorm_pgarray.fields.FloatArrayField(dbtype='double precision', dimension=2)),
                ('area', django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True)),
                ('fault', django.contrib.gis.db.models.fields.LineStringField(srid=4326, null=True)),
                ('dip', models.IntegerField()),
                ('rake', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source_Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('xml', models.FileField(null=True, upload_to='uploads/source/', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Source_Model_Contributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(verbose_name='date joined')),
                ('contributor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('model', models.ForeignKey(to='eng_models.Source_Model')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='fault',
            name='model',
        ),
        migrations.DeleteModel(
            name='Fault',
        ),
        migrations.RemoveField(
            model_name='fault_model',
            name='contributors',
        ),
        migrations.RemoveField(
            model_name='fault_model_contributor',
            name='contributor',
        ),
        migrations.RemoveField(
            model_name='fault_model_contributor',
            name='model',
        ),
        migrations.DeleteModel(
            name='Fault_Model',
        ),
        migrations.DeleteModel(
            name='Fault_Model_Contributor',
        ),
        migrations.AddField(
            model_name='source_model',
            name='contributors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='eng_models.Source_Model_Contributor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='source',
            name='model',
            field=models.ForeignKey(to='eng_models.Source_Model'),
            preserve_default=True,
        ),
    ]
