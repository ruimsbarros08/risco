# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0075_auto_20150813_1641'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classical_psha_risk_vulnerability',
            old_name='at_loss_rates_ooc',
            new_name='at_loss_rates_occ',
        ),
        migrations.RenameField(
            model_name='classical_psha_risk_vulnerability',
            old_name='it_loss_values_ooc',
            new_name='it_loss_values_occ',
        ),
        migrations.RenameField(
            model_name='classical_psha_risk_vulnerability',
            old_name='periods_ooc',
            new_name='periods_occ',
        ),
    ]
