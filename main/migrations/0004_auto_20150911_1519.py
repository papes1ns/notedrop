# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_postdata_notifed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postdata',
            old_name='notifed',
            new_name='notified',
        ),
    ]
