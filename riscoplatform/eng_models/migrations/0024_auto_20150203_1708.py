# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0023_exposure_model_oq_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Taxonomy_Fragility_Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dist_type', models.CharField(default='lognormal', max_length=20, choices=[('lognormal', 'Lognormal')])),
                ('imt', models.CharField(default='PGA', max_length=3, choices=[('PGA', 'PGA'), ('PGV', 'PGV'), ('MMI', 'MMI'), ('SA', 'Sa')])),
                ('sa_period', models.FloatField(null=True)),
                ('unit', models.CharField(max_length=3)),
                ('min_iml', models.FloatField(null=True)),
                ('max_iml', models.FloatField(null=True)),
                ('no_dmg_limit', models.FloatField(null=True)),
                ('model', models.ForeignKey(to='eng_models.Fragility_Model')),
                ('taxonomy', models.ForeignKey(to='eng_models.Building_Taxonomy')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='fragility_function',
            name='dist_type',
        ),
        migrations.RemoveField(
            model_name='fragility_function',
            name='imt',
        ),
        migrations.RemoveField(
            model_name='fragility_function',
            name='max_iml',
        ),
        migrations.RemoveField(
            model_name='fragility_function',
            name='min_iml',
        ),
        migrations.RemoveField(
            model_name='fragility_function',
            name='model',
        ),
        migrations.RemoveField(
            model_name='fragility_function',
            name='sa_period',
        ),
        migrations.RemoveField(
            model_name='fragility_function',
            name='taxonomy',
        ),
        migrations.RemoveField(
            model_name='fragility_function',
            name='unit',
        ),
        migrations.AddField(
            model_name='fragility_function',
            name='tax_frag',
            field=models.ForeignKey(default=None, null=True, to='eng_models.Taxonomy_Fragility_Model'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fragility_function',
            name='limit_state',
            field=models.CharField(max_length=20, choices=[('no_damage', 'no_damage'), ('slight', 'Slight'), ('moderate', 'Moderate'), ('extensive', 'Extensive'), ('complete', 'Complete')]),
            preserve_default=True,
        ),
    ]
