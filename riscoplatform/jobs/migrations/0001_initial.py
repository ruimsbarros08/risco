# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Scenario_Hazard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name=b'date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True)),
                ('region', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('grid_spacing', models.FloatField(default=1)),
                ('sites_type', models.CharField(default=b'DEFAULT_CONDITIONS', max_length=50, choices=[(b'VARIABLE_CONDITIONS', b'Site model'), (b'DEFAULT_CONDITIONS', b'Default conditions')])),
                ('vs30', models.FloatField(null=True, blank=True)),
                ('vs30type', models.CharField(default=b'MEASURED', max_length=10, null=True, blank=True, choices=[(b'MEASURED', b'measured'), (b'INFERRED', b'inferred')])),
                ('z1pt0', models.FloatField(null=True, blank=True)),
                ('z2pt5', models.FloatField(null=True, blank=True)),
                ('random_seed', models.IntegerField(default=3)),
                ('rupture_mesh_spacing', models.IntegerField(default=5)),
                ('repture_type', models.CharField(default=b'CUSTOM_RUPTURE', max_length=50, choices=[(b'CLOSEST_FAULT', b'closest fault'), (b'CUSTOM_RUPTURE', b'custom rupture'), (b'UPLOAD_XML', b'upload xml')])),
                ('magnitude', models.FloatField(null=True, blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('depth', models.FloatField(null=True, blank=True)),
                ('rake', models.FloatField(null=True, blank=True)),
                ('upper_depth', models.FloatField(null=True, blank=True)),
                ('lower_depth', models.FloatField(null=True, blank=True)),
                ('dip', models.FloatField(null=True, blank=True)),
                ('rupture_geom', django.contrib.gis.db.models.fields.LineStringField(srid=4326, null=True, blank=True)),
                ('rupture_xml', models.FileField(null=True, upload_to=b'uploads/rupture/', blank=True)),
                ('pga', models.BooleanField(default=True)),
                ('sa1_period', models.FloatField(null=True, blank=True)),
                ('sa2_period', models.FloatField(null=True, blank=True)),
                ('sa3_period', models.FloatField(null=True, blank=True)),
                ('truncation_level', models.FloatField(default=3)),
                ('max_distance', models.FloatField(default=200)),
                ('gmpe', models.CharField(max_length=50, choices=[(b'ABRAHAMSON_AND_SILVA_2008', b'Abrahamson and Silva 2008'), (b'AKKAR_AND_BOMMER_2010', b'Akkar and Boomer 2010'), (b'AKKAR_AND_CAGNAN_2010', b'Akkar and Cagnan 2010'), (b'BOORE_AND_ATKINSON_2008', b'Boore and Atkinson 2008'), (b'CAUZZI_AND_FACCIOLI_2008', b'Cauzzi and Faccioli 2008'), (b'CHIOU_AND_YOUNGS_2008', b'Chiou and Youngs 2008'), (b'FACCIOLI_ET_AL_2010', b'Faccioli et al. 2010'), (b'SADIGH_ET_AL_1997', b'Sadigh et al. 1997'), (b'ZHAO_ET_AL_2006_ASC', b'Zhao et al. 2006 (ASC)'), (b'ATKINSON_AND_BOORE_2003_INTER', b'Atkinson and Boore 2003 (Inter)'), (b'ATKINSON_AND_BOORE_2003_IN_SLAB', b'Atkinson and Boore 2003 (In-slab)'), (b'LIN_AND_LEE_2008_INTER', b'Lin and Lee 2008 (Inter)'), (b'LIN_AND_LEE_2008_IN_SLAB', b'Lin and Lee 2008 (In-slab)'), (b'YOUNGS_ET_AL_1997_INTER', b'Youngs et al. 1997 (Inter)'), (b'YOUNGS_ET_AL_1997_IN_SLAB', b'Youngs et al. 1997 (In-slab)'), (b'ZHAO_ET_AL_2006_INTER', b'Zhao et al. 2006 (Inter)'), (b'ZHAO_ET_AL_2006_IN_SLAB', b'Zhao et al. 2006 (In-slab)'), (b'ATKINSON_AND_BOORE_2006', b'Atkinson and Boore 2006'), (b'CAMPBELL_2003', b'Campbell 2003'), (b'TORO_ET_AL_2002', b'Toro et al. 2002')])),
                ('correlation_model', models.BooleanField(default=True)),
                ('vs30_clustering', models.BooleanField(default=False)),
                ('n_gmf', models.IntegerField(default=50)),
                ('ini_file', models.FileField(null=True, upload_to=b'uploads/scenario/hazard/', blank=True)),
                ('error', models.BooleanField(default=False)),
                ('ready', models.BooleanField(default=False)),
                ('fault', models.ForeignKey(blank=True, to='eng_models.Fault', null=True)),
                ('fault_model', models.ForeignKey(blank=True, to='eng_models.Fault_Model', null=True)),
                ('site_model', models.ForeignKey(blank=True, to='eng_models.Site_Model', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'jobs_scenario_hazard',
                'managed': True,
            },
            bases=(models.Model,),
        ),
    ]
