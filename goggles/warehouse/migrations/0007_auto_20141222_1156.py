# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0006_message_message_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='import_job',
            field=models.ForeignKey(to='warehouse.ImportJob', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='session',
            name='status',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Session status', choices=[(b'started', b'Started'), (b'completed', b'Completed'), (b'failed', b'Failed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='message',
            name='session',
            field=models.ForeignKey(to='warehouse.Session', null=True),
            preserve_default=True,
        ),
    ]
