# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_session_import_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importjob',
            name='username_token',
            field=models.CharField(unique=True, max_length=255, verbose_name=b'Username token.'),
            preserve_default=True,
        ),
    ]
