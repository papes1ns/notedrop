# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_userprofile_notify_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='postdata',
            name='notifed',
            field=models.NullBooleanField(default=False),
        ),
    ]
