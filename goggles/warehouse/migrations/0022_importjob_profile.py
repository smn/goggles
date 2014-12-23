# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0021_importjob_conversation'),
    ]

    operations = [
        migrations.AddField(
            model_name='importjob',
            name='profile',
            field=models.ForeignKey(to='warehouse.Profile', null=True),
            preserve_default=True,
        ),
    ]
