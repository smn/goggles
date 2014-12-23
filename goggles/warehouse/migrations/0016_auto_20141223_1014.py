# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0015_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='session_id',
            new_name='session_value',
        ),
        migrations.AddField(
            model_name='profile',
            name='session_name',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
    ]
