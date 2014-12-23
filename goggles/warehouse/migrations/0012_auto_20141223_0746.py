# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0011_auto_20141223_0744'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='importjob',
            options={'ordering': ('-created_at',)},
        ),
        migrations.RemoveField(
            model_name='session',
            name='status',
        ),
        migrations.AddField(
            model_name='importjob',
            name='status',
            field=models.CharField(max_length=255, null=True, choices=[(b'started', b'Started'), (b'completed', b'Completed'), (b'failed', b'Failed')]),
            preserve_default=True,
        ),
    ]
