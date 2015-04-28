# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0048_vulnerability_model_xml'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0022_auto_20150219_1830'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classical_PSHA_Hazard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name=b'date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True)),
                ('n_lt_samples', models.IntegerField()),
                ('rupture_mesh_spacing', models.FloatField()),
                ('width_of_mfd_bin', models.FloatField()),
                ('area_source_discretization', models.FloatField()),
                ('sites_type', models.CharField(default=b'DEFAULT_CONDITIONS', max_length=50, choices=[(b'VARIABLE_CONDITIONS', b'Site model'), (b'DEFAULT_CONDITIONS', b'Default conditions')])),
                ('vs30', models.FloatField(null=True, blank=True)),
                ('vs30type', models.CharField(default=b'MEASURED', max_length=10, null=True, blank=True, choices=[(b'MEASURED', b'measured'), (b'INFERRED', b'inferred')])),
                ('z1pt0', models.FloatField(null=True, blank=True)),
                ('z2pt5', models.FloatField(null=True, blank=True)),
                ('investigation_time', models.IntegerField()),
                ('truncation_level', models.FloatField()),
                ('max_distance', models.FloatField(default=200)),
                ('ini_file', models.FileField(null=True, upload_to=b'uploads/psha/hazard/', blank=True)),
                ('status', models.CharField(default=b'CREATED', max_length=50, choices=[(b'CREATED', b'Created'), (b'STARTED', b'Started'), (b'ERROR', b'Error'), (b'FINISHED', b'Finished')])),
                ('oq_id', models.IntegerField(null=True)),
                ('exposure_model', models.ForeignKey(to='eng_models.Exposure_Model')),
                ('logic_trees', models.ManyToManyField(to='eng_models.Logic_Tree')),
                ('site_model', models.ForeignKey(blank=True, to='eng_models.Site_Model', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('vulnerability_models', models.ManyToManyField(to='eng_models.Vulnerability_Model')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
