# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=255, null=True)),
                ('response', models.CharField(max_length=255, null=True)),
                ('duration', models.IntegerField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('direction', models.CharField(max_length=255, choices=[(b'inbound', b'Inbound'), (b'outbound', b'outbound')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session_id', models.CharField(max_length=255, verbose_name=b'Session Identifier')),
                ('from_addr', models.CharField(max_length=255, verbose_name=b'Subscriber address')),
                ('to_addr', models.CharField(max_length=255, verbose_name=b'Destination address')),
                ('tag_pool', models.CharField(max_length=255, null=True, verbose_name=b'Tag pool')),
                ('tag', models.CharField(max_length=255, null=True, verbose_name=b'Tag')),
                ('started_at', models.DateTimeField(null=True)),
                ('ended_at', models.DateTimeField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='message',
            name='session',
            field=models.ForeignKey(to='warehouse.Session'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='interaction',
            name='inbound',
            field=models.ForeignKey(related_name='inbound', to='warehouse.Message', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='interaction',
            name='outbound',
            field=models.ForeignKey(related_name='outbound', to='warehouse.Message', null=True),
            preserve_default=True,
        ),
    ]
