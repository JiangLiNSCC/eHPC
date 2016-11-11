# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 03:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HPCJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobfile', models.FileField(upload_to='')),
                ('jobfile_args', models.CharField(max_length=128)),
                ('machine', models.CharField(max_length=10)),
                ('jobid', models.IntegerField()),
                ('status', models.CharField(max_length=10)),
                ('time_create', models.DateTimeField()),
                ('time_submit', models.DateTimeField()),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('time_hold', models.TimeField()),
                ('time_limit', models.TimeField()),
                ('partition', models.CharField(max_length=16)),
                ('scale_cores', models.IntegerField()),
                ('scale_memGB', models.IntegerField()),
                ('scale_Nodes', models.IntegerField()),
                ('info', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
