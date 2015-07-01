# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0061_remove_classical_psha_hazard_imt_l'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classical_psha_hazard',
            old_name='imt_l_test',
            new_name='imt_l',
        ),
    ]
