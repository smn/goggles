# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0002_gogglesjob'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='GogglesJob',
            new_name='ImportJob',
        ),
    ]
