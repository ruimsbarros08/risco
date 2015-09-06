# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('eng_models', '0066_auto_20150622_2220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source_model_contributor',
            name='author',
        ),
        migrations.AddField(
            model_name='source_model',
            name='author',
            field=models.ForeignKey(related_name='author', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='source_model',
            name='contributors',
            field=models.ManyToManyField(related_name='contributors', through='eng_models.Source_Model_Contributor', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
