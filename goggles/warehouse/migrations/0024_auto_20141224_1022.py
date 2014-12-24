# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0023_auto_20141224_1018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interaction',
            name='previous_outbound',
        ),
        migrations.AddField(
            model_name='interaction',
            name='previous_interaction',
            field=models.ForeignKey(to='warehouse.Interaction', null=True),
            preserve_default=True,
        ),
    ]
