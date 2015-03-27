# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eng_models', '0046_vulnerability_model_consequnce_model'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vulnerability_model',
            old_name='consequnce_model',
            new_name='consequence_model',
        ),
    ]
