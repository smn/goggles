# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0020_conversation_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='importjob',
            name='conversation',
            field=models.ForeignKey(to='warehouse.Conversation', null=True),
            preserve_default=True,
        ),
    ]
