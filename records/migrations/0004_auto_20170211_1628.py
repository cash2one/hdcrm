# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-11 08:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_auto_20170211_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderaccount',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]