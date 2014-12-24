# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0024_auto_20141224_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='session_event',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
    ]
