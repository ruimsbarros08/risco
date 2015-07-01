# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0060_classical_psha_hazard_imt_l_test'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classical_psha_hazard',
            name='imt_l',
        ),
    ]
