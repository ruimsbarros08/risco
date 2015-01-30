# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eng_models', '0011_auto_20150127_1815'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fragility_Function',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dist_type', models.CharField(default='lognormal', max_length=10, choices=[('lognormal', 'Lognormal')])),
                ('limit_state', models.CharField(max_length=10, choices=[('slight', 'Slight'), ('moderate', 'Moderate'), ('extensive', 'Extensive'), ('complete', 'Complete')])),
                ('sa_period', models.FloatField()),
                ('unit', models.CharField(max_length=3)),
                ('min_iml', models.FloatField()),
                ('max_iml', models.FloatField()),
                ('mean', models.FloatField()),
                ('stddev', models.FloatField()),
                ('function', djorm_pgarray.fields.FloatArrayField(dbtype='double precision', dimension=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fragility_Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('xml', models.FileField(null=True, upload_to='uploads/fragility/', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Fragility_Model_Contributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(verbose_name='date joined')),
                ('contributor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('model', models.ForeignKey(to='eng_models.Fragility_Model')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='fragility_model',
            name='contributors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='eng_models.Fragility_Model_Contributor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fragility_model',
            name='taxonomy_source',
            field=models.ForeignKey(to='eng_models.Building_Taxonomy_Source'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fragility_function',
            name='model',
            field=models.ForeignKey(to='eng_models.Fragility_Model'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='fragility_function',
            name='taxonomy',
            field=models.ForeignKey(to='eng_models.Building_Taxonomy'),
            preserve_default=True,
        ),
    ]
