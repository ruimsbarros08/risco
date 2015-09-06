# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eng_models', '0067_auto_20150904_1110'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='building_taxonomy_source_contributor',
            name='author',
        ),
        migrations.RemoveField(
            model_name='consequence_model_contributor',
            name='author',
        ),
        migrations.RemoveField(
            model_name='exposure_model_contributor',
            name='author',
        ),
        migrations.RemoveField(
            model_name='fragility_model_contributor',
            name='author',
        ),
        migrations.RemoveField(
            model_name='site_model_contributor',
            name='author',
        ),
        migrations.RemoveField(
            model_name='vulnerability_model_contributor',
            name='author',
        ),
        migrations.AddField(
            model_name='building_taxonomy_source',
            name='author',
            field=models.ForeignKey(related_name='building_taxonomy_source_author', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='consequence_model',
            name='author',
            field=models.ForeignKey(related_name='consequence_model_author', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exposure_model',
            name='author',
            field=models.ForeignKey(related_name='exposure_model_author', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fragility_model',
            name='author',
            field=models.ForeignKey(related_name='fragility_model_author', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='site_model',
            name='author',
            field=models.ForeignKey(related_name='site_model_author', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vulnerability_model',
            name='author',
            field=models.ForeignKey(related_name='vulnerability_model_author', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='building_taxonomy_source',
            name='contributors',
            field=models.ManyToManyField(related_name='building_taxonomy_source_contributors', through='eng_models.Building_Taxonomy_Source_Contributor', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='consequence_model',
            name='contributors',
            field=models.ManyToManyField(related_name='consequence_model_contributors', through='eng_models.Consequence_Model_Contributor', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='exposure_model',
            name='contributors',
            field=models.ManyToManyField(related_name='exposure_model_contributors', through='eng_models.Exposure_Model_Contributor', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='fragility_model',
            name='contributors',
            field=models.ManyToManyField(related_name='fragility_model_contributors', through='eng_models.Fragility_Model_Contributor', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='site_model',
            name='contributors',
            field=models.ManyToManyField(related_name='site_model_contributors', through='eng_models.Site_Model_Contributor', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source_model',
            name='author',
            field=models.ForeignKey(related_name='source_model_author', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source_model',
            name='contributors',
            field=models.ManyToManyField(related_name='source_model_contributors', through='eng_models.Source_Model_Contributor', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='vulnerability_model',
            name='contributors',
            field=models.ManyToManyField(related_name='vulnerability_model_contributors', through='eng_models.Vulnerability_Model_Contributor', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
