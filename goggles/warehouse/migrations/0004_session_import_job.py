# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_auto_20141216_2052'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='import_job',
            field=models.ForeignKey(to='warehouse.ImportJob', null=True),
            preserve_default=True,
        ),
    ]
