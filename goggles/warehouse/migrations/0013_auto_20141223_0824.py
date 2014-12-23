# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0012_auto_20141223_0746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='from_addr',
        ),
        migrations.RemoveField(
            model_name='session',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='session',
            name='tag_pool',
        ),
        migrations.RemoveField(
            model_name='session',
            name='to_addr',
        ),
        migrations.AddField(
            model_name='message',
            name='from_addr',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Subscriber address'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='tag',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='tag_pool',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Tag pool'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='message',
            name='to_addr',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Destination address'),
            preserve_default=True,
        ),
    ]
