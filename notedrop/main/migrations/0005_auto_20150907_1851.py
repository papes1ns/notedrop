# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20150907_0001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postdata',
            name='downvote',
        ),
        migrations.RemoveField(
            model_name='postdata',
            name='upvote',
        ),
        migrations.AlterField(
            model_name='postdata',
            name='noted',
            field=models.NullBooleanField(default=False),
        ),
    ]
