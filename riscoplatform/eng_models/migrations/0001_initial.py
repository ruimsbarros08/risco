# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('world', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True)),
                ('name', models.CharField(max_length=10)),
                ('n_buildings', models.IntegerField()),
                ('area', models.FloatField()),
                ('struct_cost', models.FloatField(null=True)),
                ('struct_deductible', models.FloatField(null=True)),
                ('struct_insurance_limit', models.FloatField(null=True)),
                ('retrofitting_cost', models.FloatField(null=True)),
                ('non_struct_cost', models.FloatField(null=True)),
                ('non_struct_deductible', models.FloatField(null=True)),
                ('non_struct_insurance_limit', models.FloatField(null=True)),
                ('contents_cost', models.FloatField(null=True)),
                ('contents_deductible', models.FloatField(null=True)),
                ('contents_insurance_limit', models.FloatField(null=True)),
                ('business_int_cost', models.FloatField(null=True)),
                ('business_int_deductible', models.FloatField(null=True)),
                ('business_int_insurance_limit', models.FloatField(null=True)),
                ('oc_day', models.FloatField(null=True)),
                ('oc_night', models.FloatField(null=True)),
                ('oc_transit', models.FloatField(null=True)),
            ],
            options={
                'db_table': 'eng_models_asset',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Building_Taxonomy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=10)),
                ('description', models.CharField(max_length=200, null=True)),
                ('material', models.CharField(max_length=10, null=True)),
                ('nstoreys', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'eng_models_building_taxonomy',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Building_Taxonomy_Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True)),
            ],
            options={
                'db_table': 'eng_models_building_taxonomy_source',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Building_Taxonomy_Source_Contributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(verbose_name='date joined')),
                ('contributor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('source', models.ForeignKey(to='eng_models.Building_Taxonomy_Source')),
            ],
            options={
                'db_table': 'eng_models_building_taxonomy_source_contributor',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Exposure_Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('area_type', models.CharField(default='aggregated', max_length=20, null=True, choices=[('aggregated', 'aggregated'), ('per_unit', 'per_unit')])),
                ('area_unit', models.CharField(default='squared_meters', max_length=20, null=True, choices=[('squared_meters', 'squared meters'), ('hectare', 'hectare')])),
                ('struct_cost_type', models.CharField(default='aggregated', max_length=20, null=True, choices=[('aggregated', 'aggregated'), ('per_unit', 'per_unit')])),
                ('struct_cost_currency', models.CharField(default='EUR', max_length=5, null=True, choices=[('EUR', 'eur'), ('DOL', 'dol')])),
                ('non_struct_cost_type', models.CharField(default='aggregated', max_length=20, null=True, choices=[('aggregated', 'aggregated'), ('per_unit', 'per_unit')])),
                ('non_struct_cost_currency', models.CharField(default='EUR', max_length=5, null=True, choices=[('EUR', 'eur'), ('DOL', 'dol')])),
                ('contents_cost_type', models.CharField(default='aggregated', max_length=20, null=True, choices=[('aggregated', 'aggregated'), ('per_unit', 'per_unit')])),
                ('contents_cost_currency', models.CharField(default='EUR', max_length=5, null=True, choices=[('EUR', 'eur'), ('DOL', 'dol')])),
                ('business_int_cost_type', models.CharField(default='aggregated', max_length=20, null=True, choices=[('aggregated', 'aggregated'), ('per_unit', 'per_unit')])),
                ('business_int_cost_currency', models.CharField(default='EUR', max_length=5, null=True, choices=[('EUR', 'eur'), ('DOL', 'dol')])),
                ('deductible', models.CharField(default='absolute', max_length=20, null=True, choices=[('absolute', 'absolute'), ('relative', 'relative')])),
                ('insurance_limit', models.CharField(default='absolute', max_length=20, null=True, choices=[('absolute', 'absolute'), ('relative', 'relative')])),
                ('xml', models.FileField(null=True, upload_to='uploads/exposure/', blank=True)),
            ],
            options={
                'db_table': 'eng_models_exposure_model',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Exposure_Model_Contributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(verbose_name='date joined')),
                ('contributor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('model', models.ForeignKey(to='eng_models.Exposure_Model')),
            ],
            options={
                'db_table': 'eng_models_exposure_model_contributor',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fault',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('mindepth', models.FloatField()),
                ('maxdepth', models.FloatField()),
                ('strike', models.IntegerField()),
                ('dip', models.IntegerField()),
                ('rake', models.IntegerField()),
                ('sr', models.FloatField()),
                ('maxmag', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(srid=4326)),
            ],
            options={
                'db_table': 'eng_models_fault',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fault_Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('xml', models.FileField(null=True, upload_to='uploads/fault/', blank=True)),
            ],
            options={
                'db_table': 'eng_models_fault_model',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fault_Model_Contributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(verbose_name='date joined')),
                ('contributor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('model', models.ForeignKey(to='eng_models.Fault_Model')),
            ],
            options={
                'db_table': 'eng_models_fault_model_contributor',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('vs30', models.FloatField()),
                ('vs30type', models.CharField(default='measured', max_length=10, choices=[('measured', 'measured'), ('inferred', 'inferred')])),
                ('z1pt0', models.FloatField()),
                ('z2pt5', models.FloatField()),
                ('lat', models.FloatField(null=True)),
                ('lon', models.FloatField(null=True)),
                ('cell', models.ForeignKey(to='world.Fishnet', null=True)),
            ],
            options={
                'db_table': 'eng_models_site',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Site_Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('xml', models.FileField(null=True, upload_to='uploads/site/', blank=True)),
            ],
            options={
                'db_table': 'eng_models_site_model',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Site_Model_Contributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(verbose_name='date joined')),
                ('contributor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('model', models.ForeignKey(to='eng_models.Site_Model')),
            ],
            options={
                'db_table': 'eng_models_site_model_contributor',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='site_model',
            name='contributors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='eng_models.Site_Model_Contributor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='site',
            name='model',
            field=models.ForeignKey(to='eng_models.Site_Model'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fault_model',
            name='contributors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='eng_models.Fault_Model_Contributor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fault',
            name='model',
            field=models.ForeignKey(to='eng_models.Site_Model'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='exposure_model',
            name='contributors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='eng_models.Exposure_Model_Contributor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='building_taxonomy_source',
            name='contributors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='eng_models.Building_Taxonomy_Source_Contributor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='building_taxonomy',
            name='source',
            field=models.ForeignKey(to='eng_models.Building_Taxonomy_Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='model',
            field=models.ForeignKey(to='eng_models.Exposure_Model'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='parish',
            field=models.ForeignKey(to='world.World', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='asset',
            name='taxonomy',
            field=models.ForeignKey(to='eng_models.Building_Taxonomy'),
            preserve_default=True,
        ),
    ]
