# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0036_auto_20150226_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logic_tree',
            name='type',
            field=models.CharField(default='source', max_length=25, choices=[('source', 'Source'), ('gmpe', 'GMPE')]),
            preserve_default=True,
        ),
    ]
