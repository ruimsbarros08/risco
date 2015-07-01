# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings
import djorm_pgarray.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eng_models', '0066_auto_20150622_2220'),
        ('jobs', '0057_classical_psha_risk_insured_losses'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event_Based_Hazard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name=b'date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True)),
                ('random_seed', models.IntegerField(default=3)),
                ('region', django.contrib.gis.db.models.fields.PolygonField(srid=4326)),
                ('grid_spacing', models.FloatField(default=1)),
                ('n_lt_samples', models.IntegerField()),
                ('rupture_mesh_spacing', models.FloatField()),
                ('width_of_mfd_bin', models.FloatField()),
                ('area_source_discretization', models.FloatField()),
                ('sites_type', models.CharField(default=b'DEFAULT_CONDITIONS', max_length=50, choices=[(b'VARIABLE_CONDITIONS', b'Site model'), (b'DEFAULT_CONDITIONS', b'Default conditions')])),
                ('vs30', models.FloatField(null=True, blank=True)),
                ('vs30type', models.CharField(default=b'measured', max_length=10, null=True, blank=True, choices=[(b'measured', b'measured'), (b'inferred', b'inferred')])),
                ('z1pt0', models.FloatField(null=True, blank=True)),
                ('z2pt5', models.FloatField(null=True, blank=True)),
                ('correlation_model', models.BooleanField(default=True)),
                ('vs30_clustering', models.BooleanField(default=False)),
                ('ses_per_logic_tree_path', models.IntegerField()),
                ('investigation_time', models.IntegerField()),
                ('imt_l', jsonfield.fields.JSONField()),
                ('truncation_level', models.FloatField()),
                ('max_distance', models.FloatField(default=200)),
                ('quantile_hazard_curves', djorm_pgarray.fields.FloatArrayField(dbtype='double precision')),
                ('poes', djorm_pgarray.fields.FloatArrayField(dbtype='double precision')),
                ('ini_file', models.FileField(null=True, upload_to=b'uploads/event_based/hazard/', blank=True)),
                ('status', models.CharField(default=b'CREATED', max_length=50, choices=[(b'CREATED', b'Created'), (b'STARTED', b'Started'), (b'ERROR', b'Error'), (b'FINISHED', b'Finished')])),
                ('oq_id', models.IntegerField(null=True)),
                ('gmpe_logic_tree', models.ForeignKey(to='eng_models.Logic_Tree_GMPE')),
                ('site_model', models.ForeignKey(blank=True, to='eng_models.Site_Model', null=True)),
                ('sm_logic_tree', models.ForeignKey(to='eng_models.Logic_Tree_SM')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
