# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0002_auto_20150330_1833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adm_3',
            name='adm_2',
        ),
        migrations.RemoveField(
            model_name='adm_4',
            name='adm_3',
        ),
        migrations.DeleteModel(
            name='Adm_3',
        ),
        migrations.RemoveField(
            model_name='adm_5',
            name='adm_4',
        ),
        migrations.DeleteModel(
            name='Adm_4',
        ),
        migrations.DeleteModel(
            name='Adm_5',
        ),
        migrations.AlterField(
            model_name='adm_1',
            name='country',
            field=models.ForeignKey(to='world.Country', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='adm_1',
            name='id_1',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='adm_1',
            name='type',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='adm_2',
            name='adm_1',
            field=models.ForeignKey(to='world.Adm_1', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='adm_2',
            name='id_2',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='adm_2',
            name='type',
            field=models.CharField(max_length=50, null=True),
            preserve_default=True,
        ),
    ]
