# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0018_profile_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('conversation_key', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('profile', models.ForeignKey(to='warehouse.Profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(max_length=255, null=True, choices=[(b'disconnected', b'Disconnected'), (b'connecting', b'Connecting'), (b'connected', b'Connected'), (b'failed', b'Failed'), (b'expired', b'Expired')]),
            preserve_default=True,
        ),
    ]
