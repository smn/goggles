# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0022_importjob_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message_id', models.CharField(max_length=255)),
                ('event_id', models.CharField(max_length=255)),
                ('event_type', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField()),
                ('import_job', models.ForeignKey(to='warehouse.ImportJob', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='interaction',
            name='previous_outbound',
            field=models.ForeignKey(related_name='previous_outbound', to='warehouse.Message', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='importjob',
            name='status',
            field=models.CharField(max_length=255, null=True, choices=[(b'started', b'Started'), (b'in_progress', b'In progress'), (b'completed', b'Completed'), (b'failed', b'Failed')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='interaction',
            name='inbound',
            field=models.ForeignKey(related_name='inbound', null=True, to='warehouse.Message', unique=True),
            preserve_default=True,
        ),
    ]
