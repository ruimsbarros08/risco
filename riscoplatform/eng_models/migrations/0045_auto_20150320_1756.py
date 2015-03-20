# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eng_models', '0044_auto_20150320_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consequence_Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(verbose_name='date created')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('limit_states', djorm_pgarray.fields.TextArrayField(dbtype='text')),
                ('values', djorm_pgarray.fields.FloatArrayField(dbtype='double precision')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Consequence_Model_Contributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(verbose_name='date joined')),
                ('contributor', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('model', models.ForeignKey(to='eng_models.Consequence_Model')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='consequence_model',
            name='contributors',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='eng_models.Consequence_Model_Contributor'),
            preserve_default=True,
        ),
    ]
