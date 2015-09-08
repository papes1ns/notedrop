# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20150907_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='postdata',
            name='downvote',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AddField(
            model_name='postdata',
            name='upvote',
            field=models.NullBooleanField(default=False),
        ),
    ]
