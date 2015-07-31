# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0062_auto_20150630_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event_Based_Risk',
            fields=[
                ('classical_psha_risk_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='jobs.Classical_PSHA_Risk')),
                ('loss_curve_resolution', models.IntegerField()),
                ('hazard_event_based', models.ForeignKey(to='jobs.Event_Based_Hazard')),
            ],
            options={
            },
            bases=('jobs.classical_psha_risk',),
        ),
        migrations.AlterField(
            model_name='classical_psha_risk',
            name='hazard',
            field=models.ForeignKey(to='jobs.Classical_PSHA_Hazard', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='classical_psha_risk',
            name='lrem_steps_per_interval',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
