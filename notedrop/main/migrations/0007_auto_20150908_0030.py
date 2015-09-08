# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150908_0021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postdata',
            name='downvote',
        ),
        migrations.AlterField(
            model_name='postdata',
            name='upvote',
            field=models.NullBooleanField(default=None),
        ),
    ]
