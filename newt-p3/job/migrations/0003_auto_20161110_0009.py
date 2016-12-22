# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 06:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_auto_20161110_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hpcjob',
            name='jobid',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='time_create',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='time_end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='time_hold',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='time_limit',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='time_start',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='time_submit',
            field=models.DateTimeField(null=True),
        ),
    ]