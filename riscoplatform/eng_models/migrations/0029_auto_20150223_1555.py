# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import djorm_pgarray.fields


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0028_auto_20150222_2209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logic_tree_branch',
            name='model',
        ),
        migrations.AddField(
            model_name='logic_tree_branch',
            name='a_b',
            field=djorm_pgarray.fields.FloatArrayField(dbtype='double precision'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_branch',
            name='b_inc',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_branch',
            name='gmpe',
            field=models.CharField(max_length=50, null=True, choices=[('AbrahamsonSilva2008', 'Abrahamson and Silva 2008'), ('AkkarBommer2010', 'Akkar and Boomer 2010'), ('AkkarCagnan2010', 'Akkar and Cagnan 2010'), ('BooreAtkinson2008', 'Boore and Atkinson 2008'), ('CauzziFaccioli2008', 'Cauzzi and Faccioli 2008'), ('ChiouYoungs2008', 'Chiou and Youngs 2008'), ('FaccioliEtAl2010', 'Faccioli et al. 2010'), ('SadighEtAl1997', 'Sadigh et al. 1997'), ('ZhaoEtAl2006Asc', 'Zhao et al. 2006 (ASC)'), ('AtkinsonBoore2003SInter', 'Atkinson and Boore 2003 (Inter)'), ('AtkinsonBoore2003SSlab', 'Atkinson and Boore 2003 (In-slab)'), ('LinLee2008SInter', 'Lin and Lee 2008 (Inter)'), ('LinLee2008SSlab', 'Lin and Lee 2008 (In-slab)'), ('YoungsEtAl1997SInter', 'Youngs et al. 1997 (Inter)'), ('YoungsEtAl1997SSlab', 'Youngs et al. 1997 (In-slab)'), ('ZhaoEtAl2006SInter', 'Zhao et al. 2006 (Inter)'), ('ZhaoEtAl2006SSlab', 'Zhao et al. 2006 (In-slab)'), ('AtkinsonBoore2006', 'Atkinson and Boore 2006'), ('Campbell2003', 'Campbell 2003'), ('ToroEtAl2002', 'Toro et al. 2002')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_branch',
            name='max_mag',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_branch',
            name='max_mag_inc',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_branch',
            name='source',
            field=models.ForeignKey(to='eng_models.Source', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logic_tree_branch',
            name='source_model',
            field=models.ForeignKey(to='eng_models.Source_Model', null=True),
            preserve_default=True,
        ),
    ]
