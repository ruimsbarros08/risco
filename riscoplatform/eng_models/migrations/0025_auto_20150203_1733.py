# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0024_auto_20150203_1708'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fragility_function',
            name='tax_frag',
            field=models.ForeignKey(to='eng_models.Taxonomy_Fragility_Model', null=True),
            preserve_default=True,
        ),
    ]
