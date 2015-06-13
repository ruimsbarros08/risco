# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0060_auto_20150528_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logic_tree_gmpe_level',
            name='tectonic_region',
            field=models.CharField(default=b'Active Shallow Crust', max_length=50, choices=[(b'Active Shallow Crust', b'Active Shallow Crust'), (b'Stable Continental Crust', b'Stable Continental Crust'), (b'Subduction Interface', b'Subduction Interface'), (b'Active Interslab', b'Active Interslab'), (b'Volcanic', b'Volcanic')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='source',
            name='tectonic_region',
            field=models.CharField(default=b'Active Shallow Crust', max_length=50, choices=[(b'Active Shallow Crust', b'Active Shallow Crust'), (b'Stable Continental Crust', b'Stable Continental Crust'), (b'Subduction Interface', b'Subduction Interface'), (b'Active Interslab', b'Active Interslab'), (b'Volcanic', b'Volcanic')]),
            preserve_default=True,
        ),
    ]
