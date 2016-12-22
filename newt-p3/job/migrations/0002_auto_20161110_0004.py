# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hpcjob',
            name='jobid',
            field=models.IntegerField(default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='scale_Nodes',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='scale_cores',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='scale_memGB',
            field=models.IntegerField(default=1, null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='time_create',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='time_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='time_hold',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='time_limit',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='time_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='hpcjob',
            name='time_submit',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]