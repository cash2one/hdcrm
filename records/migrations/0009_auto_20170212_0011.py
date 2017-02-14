# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-02-11 16:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0008_ordercashflow'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='product_snap',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(b'PENDING', '\u8349\u7a3f'), (b'ACTIVE', '\u8fdb\u884c\u4e2d'), (b'DONE', '\u5b8c\u6210')], default=b'PENDING', max_length=20),
        ),
    ]