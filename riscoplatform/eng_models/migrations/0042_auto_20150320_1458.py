# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eng_models', '0041_auto_20150316_1534'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vulnerability_Function',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('probabilistic_distribution', models.CharField(max_length=2, choices=[('LN', 'Lognormal'), ('BT', 'Beta')])),
                ('loss_ratio', djorm_pgarray.fields.FloatArrayField(dbtype='double precision')),
                ('coefficients_variation', djorm_pgarray.fields.FloatArrayField(dbtype='double precision')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vulnerability_Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('asset_category', models.CharField(max_length=20, choices=[('buildings', 'Buildings'), ('contents', 'Contents'), ('population', 'Population')])),
                ('loss_category', models.CharField(max_length=20, choices=[('economic_loss', 'Economic loss'), ('fatalities', 'Fatalities')])),
                ('imt', models.CharField(max_length=3, choices=[('PGA', 'PGA'), ('PGV', 'PGV'), ('MMI', 'MMI'), ('SA', 'Sa')])),
                ('sa_period', models.FloatField(null=True)),
                ('iml', djorm_pgarray.fields.FloatArrayField(dbtype='double precision')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vulnerability_Model_Contributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(verbose_name='date joined')),
                ('contributor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('model', models.ForeignKey(to='eng_models.Vulnerability_Model')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='vulnerability_model',
            name='contributors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='eng_models.Vulnerability_Model_Contributor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vulnerability_model',
            name='fragility_model',
            field=models.ForeignKey(to='eng_models.Fragility_Model', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vulnerability_model',
            name='taxonomy_source',
            field=models.ForeignKey(to='eng_models.Building_Taxonomy_Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vulnerability_function',
            name='model',
            field=models.ForeignKey(to='eng_models.Vulnerability_Model'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vulnerability_function',
            name='taxonomy',
            field=models.ForeignKey(to='eng_models.Building_Taxonomy'),
            preserve_default=True,
        ),
    ]
