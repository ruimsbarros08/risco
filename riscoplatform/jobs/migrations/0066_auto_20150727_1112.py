# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0066_auto_20150622_2220'),
        ('jobs', '0065_event_based_hazard_ses_rupture_output_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event_Loss_Table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('loss', models.FloatField()),
                ('asset', models.ForeignKey(to='eng_models.Asset')),
                ('job_vulnerability', models.ForeignKey(to='jobs.Classical_PSHA_Risk_Vulnerability')),
                ('rupture', models.ForeignKey(to='jobs.Event_Based_Hazard_SES_Rupture')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='classical_psha_risk',
            name='hazard',
            field=models.ForeignKey(blank=True, to='jobs.Classical_PSHA_Hazard', null=True),
            preserve_default=True,
        ),
    ]
