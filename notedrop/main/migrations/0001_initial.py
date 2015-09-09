# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('designator', models.CharField(max_length=3)),
                ('number', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('archived', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(to='main.Course')),
            ],
        ),
        migrations.CreateModel(
            name='PostData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('upvote', models.NullBooleanField(default=None)),
                ('noted', models.NullBooleanField(default=False)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(to='main.Post')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=25)),
                ('city', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('courses', models.ManyToManyField(to='main.Course', db_table=b'enrolled_courses')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='school',
            field=models.ForeignKey(to='main.School'),
        ),
    ]
