# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-06 03:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20170106_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountactive',
            name='account_active',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_active', to='account.Account'),
        ),
    ]
