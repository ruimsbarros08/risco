# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0059_auto_20150629_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='classical_psha_hazard',
            name='imt_l_test',
            field=django_pgjson.fields.JsonField(default=1),
            preserve_default=False,
        ),
    ]
