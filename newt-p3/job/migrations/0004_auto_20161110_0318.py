# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 09:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0003_auto_20161110_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hpcjob',
            name='jobfile',
            field=models.FilePathField(),
        ),
    ]
