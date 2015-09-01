# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0076_auto_20150813_1644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classical_psha_risk_vulnerability',
            old_name='at_loss_rates',
            new_name='at_loss_rates_agg',
        ),
        migrations.RenameField(
            model_name='classical_psha_risk_vulnerability',
            old_name='it_loss_values',
            new_name='default_periods_agg',
        ),
        migrations.RenameField(
            model_name='classical_psha_risk_vulnerability',
            old_name='periods',
            new_name='default_periods_occ',
        ),
        migrations.AddField(
            model_name='classical_psha_risk_vulnerability',
            name='aal_agg',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk_vulnerability',
            name='aal_occ',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk_vulnerability',
            name='it_loss_values_agg',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk_vulnerability',
            name='it_loss_values_table_agg',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk_vulnerability',
            name='it_loss_values_table_occ',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk_vulnerability',
            name='periods_agg',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk_vulnerability',
            name='tce_agg',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classical_psha_risk_vulnerability',
            name='tce_occ',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
    ]
