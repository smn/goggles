# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0005_auto_20141217_0454'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_id',
            field=models.CharField(max_length=255, unique=True, null=True),
            preserve_default=True,
        ),
    ]
