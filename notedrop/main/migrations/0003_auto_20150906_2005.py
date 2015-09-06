# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_remove_userprofile_discipline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='number',
            field=models.CharField(max_length=3),
        ),
    ]
