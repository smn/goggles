# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0025_message_session_event'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interaction',
            options={'ordering': ('inbound__timestamp',)},
        ),
        migrations.RemoveField(
            model_name='interaction',
            name='previous_interaction',
        ),
        migrations.AlterField(
            model_name='interaction',
            name='question',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interaction',
            name='response',
            field=models.TextField(null=True),
            preserve_default=True,
        ),
    ]
