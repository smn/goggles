# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0008_message_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='interaction',
            name='import_job',
            field=models.ForeignKey(to='warehouse.ImportJob', null=True),
            preserve_default=True,
        ),
    ]
