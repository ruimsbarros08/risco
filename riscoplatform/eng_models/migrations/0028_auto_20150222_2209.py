# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eng_models', '0027_auto_20150206_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logic_Tree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Logic_Tree_Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('model', models.CharField(max_length=25)),
                ('weight', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Logic_Tree_Branch_Set',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uncertainty_type', models.CharField(max_length=25, choices=[('gmpeModel', 'GMPE Model'), ('sourceModel', 'Source Model'), ('maxMagGRRelative', 'Max Mag GR Relative'), ('bGRRelative', 'b GR Relative'), ('abGRAbsolute', 'a/b GR Absolute'), ('maxMagGRAbsolute', 'max Mag GR Absolute')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Logic_Tree_Level',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('level', models.IntegerField()),
                ('logic_tree', models.ForeignKey(to='eng_models.Logic_Tree')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='logic_tree_branch_set',
            name='level',
            field=models.ForeignKey(to='eng_models.Logic_Tree_Level'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_branch_set',
            name='origin',
            field=models.ForeignKey(to='eng_models.Logic_Tree_Branch', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_branch',
            name='branch_set',
            field=models.ForeignKey(to='eng_models.Logic_Tree_Branch_Set'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fragility_function',
            name='limit_state',
            field=models.CharField(max_length=20, choices=[('no_damage', 'No damage'), ('slight', 'Slight'), ('moderate', 'Moderate'), ('extensive', 'Extensive'), ('complete', 'Complete')]),
            preserve_default=True,
        ),
    ]
