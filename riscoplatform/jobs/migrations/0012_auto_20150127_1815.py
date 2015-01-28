# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0011_auto_20150125_2104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scenario_hazard',
            name='ini_file_string',
        ),
        migrations.AddField(
            model_name='scenario_hazard',
            name='oq_id',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='scenario_hazard',
            name='start',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='scenario_hazard',
            name='gmpe',
            field=models.CharField(max_length=50, choices=[(b'AbrahamsonSilva2008', b'Abrahamson and Silva 2008'), (b'AkkarBommer2010', b'Akkar and Boomer 2010'), (b'AkkarCagnan2010', b'Akkar and Cagnan 2010'), (b'BooreAtkinson2008', b'Boore and Atkinson 2008'), (b'CauzziFaccioli2008', b'Cauzzi and Faccioli 2008'), (b'ChiouYoungs2008', b'Chiou and Youngs 2008'), (b'FaccioliEtAl2010', b'Faccioli et al. 2010'), (b'SadighEtAl1997', b'Sadigh et al. 1997'), (b'ZhaoEtAl2006Asc', b'Zhao et al. 2006 (ASC)'), (b'AtkinsonBoore2003SInter', b'Atkinson and Boore 2003 (Inter)'), (b'AtkinsonBoore2003SSlab', b'Atkinson and Boore 2003 (In-slab)'), (b'LinLee2008SInter', b'Lin and Lee 2008 (Inter)'), (b'LinLee2008SSlab', b'Lin and Lee 2008 (In-slab)'), (b'YoungsEtAl1997SInter', b'Youngs et al. 1997 (Inter)'), (b'YoungsEtAl1997SSlab', b'Youngs et al. 1997 (In-slab)'), (b'ZhaoEtAl2006SInter', b'Zhao et al. 2006 (Inter)'), (b'ZhaoEtAl2006SSlab', b'Zhao et al. 2006 (In-slab)'), (b'AtkinsonBoore2006', b'Atkinson and Boore 2006'), (b'Campbell2003', b'Campbell 2003'), (b'ToroEtAl2002', b'Toro et al. 2002')]),
            preserve_default=True,
        ),
    ]
