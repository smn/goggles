# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0013_auto_20141223_0824'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('timestamp',)},
        ),
        migrations.AddField(
            model_name='message',
            name='in_reply_to',
            field=models.CharField(max_length=255, null=True),
            preserve_default=True,
        ),
    ]
