# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0055_auto_20150522_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logic_Tree_GMPE',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True)),
                ('xml', models.FileField(null=True, upload_to='uploads/logic_tree/gmpe/', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Logic_Tree_GMPE_Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gmpe', models.CharField(max_length=50, null=True, choices=[(b'AbrahamsonSilva2008', b'Abrahamson and Silva 2008'), (b'AkkarBommer2010', b'Akkar and Boomer 2010'), (b'AkkarCagnan2010', b'Akkar and Cagnan 2010'), (b'BooreAtkinson2008', b'Boore and Atkinson 2008'), (b'CauzziFaccioli2008', b'Cauzzi and Faccioli 2008'), (b'ChiouYoungs2008', b'Chiou and Youngs 2008'), (b'FaccioliEtAl2010', b'Faccioli et al. 2010'), (b'SadighEtAl1997', b'Sadigh et al. 1997'), (b'ZhaoEtAl2006Asc', b'Zhao et al. 2006 (ASC)'), (b'AtkinsonBoore2003SInter', b'Atkinson and Boore 2003 (Inter)'), (b'AtkinsonBoore2003SSlab', b'Atkinson and Boore 2003 (In-slab)'), (b'LinLee2008SInter', b'Lin and Lee 2008 (Inter)'), (b'LinLee2008SSlab', b'Lin and Lee 2008 (In-slab)'), (b'YoungsEtAl1997SInter', b'Youngs et al. 1997 (Inter)'), (b'YoungsEtAl1997SSlab', b'Youngs et al. 1997 (In-slab)'), (b'ZhaoEtAl2006SInter', b'Zhao et al. 2006 (Inter)'), (b'ZhaoEtAl2006SSlab', b'Zhao et al. 2006 (In-slab)'), (b'AtkinsonBoore2006', b'Atkinson and Boore 2006'), (b'Campbell2003', b'Campbell 2003'), (b'ToroEtAl2002', b'Toro et al. 2002')])),
                ('weight', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Logic_Tree_GMPE_Level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField()),
                ('tectonic_region', models.CharField(default=b'Active Shallow Crust', max_length=50, choices=[(b'Active Shallow Crust', b'Active Shallow Crust'), (b'Stable Shallow Crust', b'Stable Shallow Crust'), (b'Subduction Interface', b'Subduction Interface'), (b'Active Interslab', b'Active Interslab'), (b'Volcanic', b'Volcanic')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Logic_Tree_SM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True)),
                ('xml', models.FileField(null=True, upload_to='uploads/logic_tree/source_models/', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Logic_Tree_SM_Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('max_mag_inc', models.FloatField(null=True)),
                ('b_inc', models.FloatField(null=True)),
                ('a_b', djorm_pgarray.fields.FloatArrayField(dbtype='double precision')),
                ('max_mag', models.FloatField(null=True)),
                ('weight', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Logic_Tree_SM_Branch_Set',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uncertainty_type', models.CharField(max_length=25, null=True, choices=[('sourceModel', 'Source Model'), ('maxMagGRRelative', 'Max Mag GR Relative'), ('bGRRelative', 'b GR Relative'), ('abGRAbsolute', 'a/b GR Absolute'), ('maxMagGRAbsolute', 'max Mag GR Absolute')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Logic_Tree_SM_Level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='logic_tree',
            name='source_models',
        ),
        migrations.RemoveField(
            model_name='logic_tree',
            name='user',
        ),
        migrations.RemoveField(
            model_name='logic_tree_branch',
            name='branch_set',
        ),
        migrations.RemoveField(
            model_name='logic_tree_branch',
            name='source_model',
        ),
        migrations.RemoveField(
            model_name='logic_tree_branch_set',
            name='level',
        ),
        migrations.RemoveField(
            model_name='logic_tree_branch_set',
            name='origin',
        ),
        migrations.DeleteModel(
            name='Logic_Tree_Branch',
        ),
        migrations.RemoveField(
            model_name='logic_tree_branch_set',
            name='sources',
        ),
        migrations.DeleteModel(
            name='Logic_Tree_Branch_Set',
        ),
        migrations.RemoveField(
            model_name='logic_tree_level',
            name='logic_tree',
        ),
    ]
